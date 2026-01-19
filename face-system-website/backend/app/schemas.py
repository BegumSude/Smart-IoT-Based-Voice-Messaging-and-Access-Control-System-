from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUser(BaseModel):
    username: str
    password: str
    photo_path: str | None = None
    role: Optional[str] = "user"  # Add this field!