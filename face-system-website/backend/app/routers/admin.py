from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db                      # 'app.' yerine '..'
from ..schemas import CreateUser                  # 'app.' yerine '..'
from ..dependencies import admin_required         # 'app.' yerine '..'
from ..create_admin import create_user_as_admin

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
