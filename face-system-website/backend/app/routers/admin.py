from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateUser
from app.dependencies import admin_required
from app.utils.create_admin import create_user_as_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create-user")
def create_user(
    user: CreateUser,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    new_user = create_user_as_admin(user, db)
    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }
