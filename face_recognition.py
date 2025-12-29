import cv2
import os
import numpy as np

# Settings
DATABASE_DIR = "database"
FACE_SIZE = (200, 200)
MAX_DISTANCE = 60 # If confidence is below this, we consider it a match

# Init
os.makedirs(DATABASE_DIR, exist_ok=True)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

model = cv2.face.LBPHFaceRecognizer_create()
label_map = {}

# Util
def extract_label(filename):
    return os.path.splitext(filename)[0].split("-")[0].lower()

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]
    return cv2.resize(face, FACE_SIZE)

# Training the database
def train_database():
    faces = []
    labels = []
    label_id = 0
    label_map.clear()

    person_dir = os.path.join(DATABASE_DIR, "persons")

    for person_name in os.listdir(person_dir):
        person_path = os.path.join(person_dir, person_name)

        if not os.path.isdir(person_path):
            continue

        label_map[person_name.lower()] = label_id
        current_label = label_id
        label_id += 1

        for file in os.listdir(person_path):
            if not file.lower().endswith((".jpg", ".png")):
                continue

            img_path = os.path.join(person_path, file)
            img = cv2.imread(img_path)
            if img is None:
                continue

            face = detect_face(img)
            if face is None:
                print(f"Face not found: {person_name}/{file}")
                continue

            faces.append(face)
            labels.append(current_label)

    if len(faces) == 0:
        raise RuntimeError(" Database is empty or no faces found")

    model.train(faces, np.array(labels))
    print(f"✔ Database trained ({len(label_map)} people)")

# Recognition
def recognize_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "NO_IMAGE", None

    face = detect_face(img)
    if face is None:
        return "NO_FACE", None

    label, distance = model.predict(face)
    
    print(f"DEBUG -> predicted_label={label}, distance={distance:.2f}")

    # Threshold check
    if distance > MAX_DISTANCE:
        # If confidence is below this value, the face is considered a match.
        # Lower confidence means better similarity.
        return "UNKNOWN", distance
    
    
    for name, lbl in label_map.items():
        if lbl == label:
                return name, distance

    return "UNKNOWN", distance
