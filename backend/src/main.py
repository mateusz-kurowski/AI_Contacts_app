# src/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat import router as chat_router
from src.api.contacts import router as contacts_router
from src.db.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_tables()
    yield

app = FastAPI(title="Contacts API", lifespan=lifespan, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts_router)
app.include_router(chat_router)


@app.get("/")
def read_root():
    return {"message": "Contacts API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
