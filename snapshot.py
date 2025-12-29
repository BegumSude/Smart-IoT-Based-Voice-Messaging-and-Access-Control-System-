import requests # For making HTTP requests
import os
from datetime import datetime

ESP32_IP = "192.168.1.43:81"
URL = f"http://{ESP32_IP}/capture"
SAVE_FOLDER = "snapshots"

os.makedirs(SAVE_FOLDER, exist_ok=True)

def take_snapshot():
    print("Taking snapshot...")
    start_time = datetime.now()  
    try:  
       response = requests.get(URL, timeout=5)
    except requests.RequestException as e: 
        print(f"Error taking snapshot: {e}")
        return None
    
    if response.status_code != 200:
        print(f"Failed to take snapshot, status code: {response.status_code}")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"snapshot_{timestamp}.jpg"
    path = os.path.join(SAVE_FOLDER, filename)

    with open(path, "wb") as f:
        f.write(response.content)

    elapsed = (datetime.now() - start_time).total_seconds() * 1000
    size_kb = len(response.content) / 1024   

    print(f"Snapshot saved: {path} ")
    print(f"time: {elapsed:.2f} ms | size: {size_kb:.2f} KB") 

    return path

if __name__ == "__main__":
    result = take_snapshot()
    if result is None:
        print("Snapshot failed.")
