from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth
from app.routers import showUsers
from fastapi.middleware.cors import CORSMiddleware
from app.create_admin import create_admin
from app.routers import admin

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

