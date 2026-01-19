import cv2
import os
import numpy as np
import sqlite3
import json
import requests


ESP32_IP = "10.118.163.154"

def send_esp32_command(command):
    try:
        url = f"http://{ESP32_IP}/{command}"
        requests.post(url, timeout=2) # 2 saniye bekle, donmasın
    except Exception as e:
        print(f"ESP32 connection error: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    raise RuntimeError(f"Haarcascade dosyası bulunamadı! Yol: {CASCADE_PATH}")

def get_embedding(face_img):
    # Eğer renkliyse griye çevir
    if len(face_img.shape) == 3:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    
    # BURASI ÖNEMLİ: Hizalama if bloğunun dışında olmalı!
    resized = cv2.resize(face_img, (100, 100))
    normalized = resized / 255.0
    return normalized.flatten()

def recognize_from_snapshot(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return "NO_IMAGE", None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        embedding = get_embedding(face_roi)
        
        best_match = "UNKNOWN"
        min_distance = 28.0 # Eşiği biraz artırdım, tanıması daha kolay olsun

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, embedding FROM users WHERE embedding IS NOT NULL")
        rows = cursor.fetchall() 

        for username, db_embedding_json in rows:
            try:
                db_embedding = np.array(json.loads(db_embedding_json))
                distance = np.linalg.norm(embedding - db_embedding)
                
                # Terminal takibi için:
                print(f"Kıyaslanan: {username} | Mesafe: {distance:.4f}") 

                if distance < min_distance:
                    min_distance = distance
                    best_match = username
            except Exception as e:
                print(f"Hata: {e}")
        
        conn.close()

        if best_match != "UNKNOWN":
          print(f"Kapı açılıyor: {best_match}")
          send_esp32_command("open-door")
        else:
          print("Yabancı kişi, kapı kapalı.")
          send_esp32_command("close-door")
        return best_match, min_distance
        
    return "NO_FACE", None

def train_database_from_db():
    print("Bilgi: Veritabanı eğitimi başladı...")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, image_path FROM users")
    users = cursor.fetchall()

    for user_record in users:
        user_id, username, img_path = user_record[0], user_record[1], user_record[2]

        if not img_path or not os.path.exists(str(img_path)):
            print(f"Atlanıyor: {username} için dosya bulunamadı.")
            continue

        img = cv2.imread(str(img_path))
        if img is None: continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            embedding = get_embedding(gray[y:y+h, x:x+w])
            
            if embedding is not None:
                embedding_json = json.dumps(embedding.tolist())
                cursor.execute("UPDATE users SET embedding = ? WHERE id = ?", (embedding_json, user_id))
                print(f"Başarılı: {username} eğitildi.")
    
    conn.commit()
    conn.close()
    print("Eğitim işlemi başarıyla tamamlandı.")