import os
import shutil
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CreateUser
from ..dependencies import admin_required
from ..create_admin import create_user_as_admin
from ..camera import take_snapshot

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create-user")
def create_user(
    user: CreateUser,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    image_path = user.photo_path

    # Eğer frontend'den bir fotoğraf yolu gelmediyse, şu an çek
    if not image_path:
        image_path = take_snapshot()
        if not image_path:
            raise HTTPException(500, "Failed to capture image")

    try:
        # --- DOSYA ADINI DÜZELTME VE TAŞIMA İŞLEMİ ---
        # snapshots içindeki snapshot_2026...jpg dosyasını kullanıcı_adi.jpg yapar
        extension = os.path.splitext(image_path)[1]   
        new_filename = f"{user.username}{extension}"
        
        # Dosyayı projenin ana dizinine (ipek.jpg'nin olduğu yer) taşıyoruz
        final_path = os.path.join(new_filename)

        if os.path.exists(image_path):
            shutil.move(image_path, final_path)
            image_path = final_path  # Veritabanına yeni temiz yolu kaydetmek için
        # --------------------------------------------

        new_user = create_user_as_admin(
            db=db,
            username=user.username,
            password=user.password,
            image_path=image_path
        )

        return {
            "message": "User created",
            "user_id": new_user.id,
            "saved_path": image_path
        }

    except Exception as e:
        print("🔥 CREATE USER EXCEPTION:", repr(e))
        raise HTTPException(500, f"Kullanıcı oluşturulurken hata: {str(e)}")

@router.post("/capture-photo")
def capture_photo(admin=Depends(admin_required)):
    print("📸 Capture endpoint hit")
    try:
        photo_path = take_snapshot()
        print("📂 Photo path:", photo_path)

        if not photo_path:
            print("❌ Snapshot returned None")
            raise HTTPException(500, "Snapshot returned None")

        return {"photo_path": photo_path}

    except Exception as e:
        print("🔥 CAPTURE EXCEPTION:", repr(e))
        raise HTTPException(500, str(e))