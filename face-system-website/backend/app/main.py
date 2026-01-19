from fastapi import FastAPI 
from app.database import engine    
from app.database import Base      
from . import models          
from .routers import auth             
from .routers import showUsers          
from fastapi.middleware.cors import CORSMiddleware 
from .create_admin import create_admin  
from .routers import admin     
from .routers import face_recognition   
from .services.face_rec_service import train_database_from_db

# import httpx
# from fastapi.responses import StreamingResponse

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(face_recognition.router)
app.include_router(auth.router)
app.include_router(showUsers.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def startup_event():
    create_admin()
    train_database_from_db()  

@app.get("/")
def root():
    return {"status": "Backend running"}
