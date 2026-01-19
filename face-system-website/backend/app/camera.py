import requests
import os
from datetime import datetime
from .database import SessionLocal
from app.services.face_rec_service import recognize_from_snapshot


ESP32_IP = "10.118.163.108"
URL = f"http://{ESP32_IP}/capture"
SAVE_FOLDER = "snapshots"

os.makedirs(SAVE_FOLDER, exist_ok=True)

def take_snapshot():
    print("Taking snapshot...")
    start_time = datetime.now()

    try:
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print("ESP32 request failed:", e)
        return None

    # 🔴 CRITICAL CHECK
    if not response.content or len(response.content) < 1000:
        print("Invalid image received (empty or too small)")
        return None

    # 🔴 Optional but STRONGLY recommended
    content_type = response.headers.get("Content-Type", "")
    if "image" not in content_type:
        print("Invalid content type:", content_type)
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SAVE_FOLDER, f"snapshot_{timestamp}.jpg")


    try:
        with open(path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print("File write failed:", e)
        return None

    elapsed = (datetime.now() - start_time).total_seconds() * 1000
    size_kb = len(response.content) / 1024

    print(f"Snapshot saved: {path}")
    print(f"time: {elapsed:.2f} ms | size: {size_kb:.2f} KB")

    return path


if __name__ == "__main__":
    # snapshot_path =# take_snapshot()

  '''  if snapshot_path:
        db = SessionLocal()
        user, result = recognize_from_snapshot(db, snapshot_path)
        db.close()

        if user:
            print("✅ Tanındı:", user.username, "| confidence:", result)
        else:
            print("❌ Tanınmadı:", result)
'''