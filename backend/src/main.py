# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat import router as chat_router
from src.api.contacts import router as contacts_router


app = FastAPI(
    title="Contacts API",
    prefix="/api",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.openapi_version = "3.0.2"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts_router)
app.include_router(chat_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
