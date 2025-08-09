from src.api.contacts import router as contacts_router
from src.api.chat import chat_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Contact Management API",
    version="1.0.0",
    description="API for managing contacts with CRUD operations",
)

app.include_router(contacts_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
