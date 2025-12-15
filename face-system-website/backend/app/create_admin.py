from app.database import SessionLocal, engine, Base
from app.models import User
from app.utils.security import hash_password

def create_admin():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        print("Admin already exists")
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

if __name__ == "__main__":
    create_admin()
