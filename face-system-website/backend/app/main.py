from fastapi import FastAPI 
from .database import engine          
from . import models          
from .routers import auth             
from .routers import showUsers          
from fastapi.middleware.cors import CORSMiddleware 
from .create_admin import create_admin  
from .routers import admin             

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/")
def root():
    return {"status": "Backend running"}

