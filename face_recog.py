import cv2
import os
import threading
import time
from deepface import DeepFace


# ESP32-CAM Stream URL'si veya Webcam indeksi
CAM_SOURCE = 0

# Performans ayarı: Tanıma işlemini her N frame'de bir yap
PROCESS_EVERY_N_FRAMES = 15 

# Renk Tanımları (BGR Formatında: (B, G, R))
COLOR_KNOWN = (0, 255, 0)      # Yeşil
COLOR_UNKNOWN = (0, 0, 255)    # Kırmızı
COLOR_TEXT = (255, 255, 255)   # Beyaz

# =======================================================
# 2️⃣ GLOBAL DEĞİŞKENLER
# =======================================================
frame_global = None 
last_faces = [] 
label_map = {} 

# =======================================================
# 3️⃣ YÜZ VERİSİ YÜKLEME
# =======================================================
def load_face_data():
    """
    'faces' klasöründeki alt klasörleri tarar ve DeepFace için harita oluşturur.
    """
    global label_map
    faces_folder = "faces" 

    if not os.path.exists(faces_folder):
        print(f"❌ Error: '{faces_folder}' folder not found. Please capture faces first.")
        return False
        
    for person_name in os.listdir(faces_folder):
        person_dir = os.path.join(faces_folder, person_name)
        if os.path.isdir(person_dir):
            image_files = [f for f in os.listdir(person_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
            if image_files:
                label_map[person_name] = os.path.join(person_dir, image_files[0])
                
    print(f"📁 Loaded recognition data for {len(label_map)} people.")
    print(f"People to Recognize: {', '.join(label_map.keys())}")
    return True

# =======================================================
# 4️⃣ KAMERA AKIŞI THREAD'İ
# =======================================================
def camera_thread():
    """Kameradan/ESP32-CAM'den sürekli kareleri okur."""
    global frame_global
    print(f"📷 Connecting to camera stream: {CAM_SOURCE}") 
    for i in range(10):
        cap = cv2.VideoCapture(CAM_SOURCE)
        if cap.isOpened():
            print("✅ Camera connection successful.")
            break
        time.sleep(1)
    else:
        print("❌ ERROR: Failed to connect to camera after retries!")
        return    
    if not cap.isOpened():
        print("❌ ERROR: Failed to connect to camera!")
        return

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    while True:
        ret, frame = cap.read() 
        if not ret:
            continue
            
        frame = cv2.flip(frame, 1) 
        frame_global = frame
        time.sleep(0.01)

# =======================================================
# 5️⃣ YÜZ TANIMA İŞLEMİ
# =======================================================
def recognize_faces(frame):
    """
    Karedeki yüzleri DeepFace ile tanır.
    """
    recognized_faces_data = []
    
    try:
        detected_faces = DeepFace.extract_faces(frame, enforce_detection=False, detector_backend='opencv')
        
        for face_data in detected_faces:
            area = face_data['facial_area']
            x, y, w, h = int(area['x']), int(area['y']), int(area['w']), int(area['h'])
            face_img = frame[y:y+h, x:x+w]
            
            name = "Unknown"
            color = COLOR_UNKNOWN 
            
            best_distance = float('inf')
            best_match = None
            
            for person_name, person_path in label_map.items():
                try:
                    result = DeepFace.verify(face_img, person_path, enforce_detection=False, model_name="VGG-Face")
                                             
                    if result['verified'] and result['distance'] < best_distance:
                        best_distance = result['distance']
                        best_match = person_name
                            
                except:
                    continue

            if best_match:
                name = best_match.upper() 
                color = COLOR_KNOWN 

            recognized_faces_data.append({
                'x': x, 'y': y, 'w': w, 'h': h, 
                'name': name, 'color': color
            })
            
    except:
        pass 

    return recognized_faces_data

# =======================================================
# 6️⃣ ANA PROGRAM AKIŞI (Düzeltilen Kısım)
# =======================================================
if __name__ == "__main__":
    
    if not load_face_data():
        exit()
        
    t_camera = threading.Thread(target=camera_thread, daemon=True)
    t_camera.start()

    print("\n⏳ Waiting for the camera connection...")
    time.sleep(3) 

    print("\n▶️ Face Recognition Started. Press 'q' or close the window to exit.")
    
    frame_counter = 0
    window_name = "Real-time Face Recognition" # Pencere adını tanımlıyoruz

    while True:
        if frame_global is None:
            time.sleep(0.1)
            continue
        
        frame = frame_global.copy()
        frame_counter += 1
        
        # Sadece belirli aralıklarla tanıma yap (performans için)
        if frame_counter % PROCESS_EVERY_N_FRAMES == 0:
            last_faces = recognize_faces(frame) 
        
        # Görüntü üzerine çizim yap
        for face in last_faces:
            x, y, w, h, name, color = face['x'], face['y'], face['w'], face['h'], face['name'], face['color']
            
            # Ana kutu (Tanındıysa Yeşil, Tanınmadıysa Kırmızı)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # İsim etiketi için arka plan
            cv2.rectangle(frame, (x, y + h - 35), (x + w, y + h), color, cv2.FILLED)
            
            # İsim metni
            cv2.putText(frame, name, (x + 6, y + h - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, COLOR_TEXT, 2)
        
        cv2.imshow(window_name, frame) # Tanımlanan pencere adı kullanılıyor
        
        # Çıkış kontrolü (Hem 'q' tuşu hem de Pencere Kapatma (X) butonu)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or \
           (cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1): # 👈 X Kapatma Kontrolü
            break

    cv2.destroyAllWindows()
    print("\n👋 Application is closing.")