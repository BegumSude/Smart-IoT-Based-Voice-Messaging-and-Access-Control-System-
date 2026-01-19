from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from .database import Base
import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # admin / user
    is_admin = Column(Boolean, default=False)
    image_path = Column(String)
