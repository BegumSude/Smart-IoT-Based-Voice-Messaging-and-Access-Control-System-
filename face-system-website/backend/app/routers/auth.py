from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal      # 'app.' silindi, '..' eklendi
from ..models import User                # 'app.' silindi, '..' eklendi
from ..security import verify_password
from ..auth import create_access_token   # 'app.' silindi, '..' eklendi
from ..schemas import LoginRequest       # 'app.' silindi, '..' eklendi
router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.username,  
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": token,
        "role": user.role
    }
