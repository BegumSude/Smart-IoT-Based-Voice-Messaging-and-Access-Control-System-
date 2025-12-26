from .database import SessionLocal, engine, Base
from .models import User
from .security import hash_password  

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
        password_hash=hash_password("1234"),
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.close()
    print("Admin user created")

# ADMIN PANELİNDEN KULLANICI EKLEMEK İÇİN GEREKLİ OLAN FONKSİYON:
def create_user_as_admin(user_data, db):
    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

if __name__ == "__main__":
    create_admin()