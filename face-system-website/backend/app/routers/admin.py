from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db                      # 'app.' yerine '..'
from ..schemas import CreateUser                  # 'app.' yerine '..'
from ..dependencies import admin_required         # 'app.' yerine '..'
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

    # If frontend didn't send photo_path → take it now
    if not image_path:
        image_path = take_snapshot()
        if not image_path:
            raise HTTPException(500, "Failed to capture image")

    new_user = create_user_as_admin(
        db=db,
        username=user.username,
        password=user.password,
        image_path=image_path
    )

    return {
        "message": "User created",
        "user_id": new_user.id
    }

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
