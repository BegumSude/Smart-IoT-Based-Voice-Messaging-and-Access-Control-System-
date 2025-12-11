import cv2
import os
import time


OUTPUT_FOLDER = "faces" 
# ESP32-CAM Stream URL'si veya Webcam indeksi
CAM_SOURCE = 0 # 0 = Webcam, veya "http://192.168.1.100:81/stream"

# =======================================================
# HAZIRLIK
# =======================================================
# Yüz algılama için Haar Cascade sınıflandırıcısını yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Çıktı klasörünü oluştur
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"✅ Folder created: {OUTPUT_FOLDER}")

# Kullanıcıdan isim al
person_name = input("Enter the name of the person to save (e.g., ali): ").strip().lower()

if not person_name:
    print("❌ Name cannot be empty. Exiting the program.")
    exit()

# Kişiye ait resimlerin kaydedileceği tam yol
person_folder = os.path.join(OUTPUT_FOLDER, person_name)

if not os.path.exists(person_folder):
    os.makedirs(person_folder)
    print(f"✅ Person folder created: {person_folder}")

# =======================================================
# CAMERA AND FACE RECORDING LOOP
# =======================================================
cap = cv2.VideoCapture(CAM_SOURCE)

if not cap.isOpened():
    print("❌ ERROR: Failed to open camera.")
    exit()

print("\n▶️ Face recording started. Look at the camera.")
print("ℹ️ When a face is detected, 10 images will be automatically saved.")
print("Press 'q' to exit.")

count = 0
MAX_IMAGES = 10 # Maximum number of images to save

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    frame = cv2.flip(frame, 1) # Ayna görüntüsü
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Yüzleri algıla
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
    
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face (Blue)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Eğer henüz 10 resim kaydetmediysek
        if count < MAX_IMAGES:
            # Yüz bölgesini kırp
            face_crop = frame[y:y+h, x:x+w]
            
            # Kaydedilecek dosya adı
            image_name = f"{person_name}_{count}.jpg"
            save_path = os.path.join(person_folder, image_name)
            
            # Resmi kaydet
            cv2.imwrite(save_path, face_crop)
            print(f"📸 Saved: {save_path} ({count + 1}/{MAX_IMAGES})")
            
            count += 1
            # Resim çekimleri arasında kısa bir bekleme (farklı pozlar için)
            time.sleep(0.3)
            
            
    # Bilgilendirme metni
    cv2.putText(frame, f"RECORDING: {person_name.upper()} ({count}/{MAX_IMAGES})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    cv2.imshow('Face Capture', frame)
    
    # Tüm resimler kaydedildiyse veya 'q' basıldıysa çık
    if count >= MAX_IMAGES or (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
print("\n✅ Face recording completed.")