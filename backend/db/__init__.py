from .db import Base, engine, SessionLocal, get_db
from .Contact import Contact
from .schema import ContactCreate, ContactUpdate, ContactOut
from . import crud

# Create tables
Base.metadata.create_all(bind=engine)

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "Contact",
    "ContactCreate",
    "ContactUpdate",
    "ContactOut",
    "crud",
]
