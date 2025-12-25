from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    img: str | None

    class Config:
        from_attributes = True
