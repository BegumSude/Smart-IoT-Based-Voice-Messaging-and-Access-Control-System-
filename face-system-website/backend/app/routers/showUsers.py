from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db  # 'app.' silindi, '..' eklendi
from ..models import User      # 'app.' silindi, '..' eklendi

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def show_users(db: Session = Depends(get_db)):
    return db.query(User).all()
