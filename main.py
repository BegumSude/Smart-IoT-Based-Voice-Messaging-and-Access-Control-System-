from snapshot import take_snapshot
from face_recognition import train_database, recognize_from_image
import time
from collections import deque

REQUIRED_MATCH = 3
CAPTURE_DELAY = 1  # seconds

print("System started")
print("Training database...")
train_database()

results = deque(maxlen=REQUIRED_MATCH)

print("Waiting for a known face...")

while True:
    img_path = take_snapshot()
    if img_path is None:
        time.sleep(CAPTURE_DELAY)
        continue

    name, distance = recognize_from_image(img_path)

    if name in ("NO_FACE", "UNKNOWN"):
        results.clear()
        print("❌ Not reliable, counter reset")
    else:
        results.append(name)
        print(f"✔ Candidate: {name} ({distance:.1f}) [{len(results)}/{REQUIRED_MATCH}]")

    if len(results) == REQUIRED_MATCH and len(set(results)) == 1:
        print(f"\n✅ Certain recognition: {name.upper()}")
        break

    time.sleep(CAPTURE_DELAY)
