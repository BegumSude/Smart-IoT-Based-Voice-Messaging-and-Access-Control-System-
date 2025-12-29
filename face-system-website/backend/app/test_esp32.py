import requests

URL = "http://192.168.1.43:81/capture"

try:
    r = requests.get(URL, timeout=5)
    print("Status:", r.status_code)
    print("Length:", len(r.content))
    print("Type:", r.headers.get("Content-Type"))
except Exception as e:
    print("ERROR:", e)
