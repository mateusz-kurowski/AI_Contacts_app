# src/main.py
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.db.db import create_tables, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_tables()
    yield

app = FastAPI(title="Contacts API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Contacts API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    return {"contacts": []}
