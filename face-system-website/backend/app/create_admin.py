from .database import SessionLocal, engine, Base
from .models import User
from .security import hash_password  
from passlib.context import CryptContext

def create_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        print("Admin already exists")
        db.close()
        return

    admin = User(
        username="admin",
        hashed_password=hash_password("1234"),
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.close()
    print("Admin user created")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


# ADMIN PANELİNDEN KULLANICI EKLEMEK İÇİN GEREKLİ OLAN FONKSİYON:
from sqlalchemy.orm import Session
from .models import User
from .security import hash_password

def create_user_as_admin(db, username, password, image_path):
    user = User(
        username=username,
        hashed_password=hash_password(password),  # ✅
        image_path=image_path,
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
