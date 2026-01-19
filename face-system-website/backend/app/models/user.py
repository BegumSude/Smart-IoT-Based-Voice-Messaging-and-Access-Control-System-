from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) 
    role = Column(String)
    is_admin = Column(Boolean, default=False)
    
    image_path = Column(String, nullable=True)
    embedding = Column(LargeBinary, nullable=True)