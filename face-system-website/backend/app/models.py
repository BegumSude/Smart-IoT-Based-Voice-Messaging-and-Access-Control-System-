from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # admin / user
    is_admin = Column(Boolean, default=False)
    img = Column(String)

# class Recording(Base):
#     __tablename__ = "recordings"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     file_path = Column(String)