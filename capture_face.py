import requests
import time
import os
from datetime import datetime


esp32cam_ıp = "10.246.64.144"  
URL = f"http://{esp32cam_ıp}/capture"
save_folder = "snapshots"
interval = 2 # delay in seconds

if not os.path.exists(save_folder):
    os.makedirs(save_folder)
    print(f"'{save_folder}' created.")

print(f"Recording started... Folder: {os.path.abspath(save_folder)}")

try:
    while True:
        try:
            response = requests.get(URL, timeout=5)
            
            if response.status_code == 200:
                # Create the filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"snapshot_{timestamp}.jpg"
                
                # Use os.path.join to avoid directory confusion
                filepath = os.path.join(save_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"Saved: {filepath}")
            else:
                print(f"Server error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")

        time.sleep(interval)

except KeyboardInterrupt:
    print("\nStopped by the user.")
