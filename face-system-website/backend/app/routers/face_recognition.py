# routers/face_recognition.py
from fastapi import APIRouter, UploadFile
from ..services.face_rec_service import recognize_from_snapshot

router = APIRouter(
    prefix="/face",
    tags=["Face Recognition"]
)

@router.post("/recognize")
async def recognize_face(snapshot: UploadFile):
    print("--- Yeni bir tanıma isteği geldi! ---") # Bunu ekle
    image_bytes = await snapshot.read()

    username, distance = recognize_from_snapshot(image_bytes)
    
    if username == "UNKNOWN" or username in ("NO_IMAGE", "NO_FACE") or username is None:
        return {"status": "unrecognized", "user": "UNKNOWN"}
    else:
        return {"status": "recognized", "user": username}
