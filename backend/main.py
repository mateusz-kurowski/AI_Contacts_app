from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv

from db.db import get_db
from db import crud
from db.schema import ContactCreate, ContactUpdate, ContactOut

load_dotenv()

app = FastAPI(title="Contact Management API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + uv!"}


@app.post("/contacts/", response_model=ContactOut)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Create a new contact."""
    # Check if phone number already exists
    db_contact = crud.get_contact_by_phone(db, phone=contact.phone)
    if db_contact:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_contact(db=db, contact=contact)


@app.get("/contacts/", response_model=List[ContactOut])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all contacts with pagination."""
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific contact by ID."""
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)
):
    """Update an existing contact."""
    # Check if phone number already exists for a different contact
    db_contact_by_phone = crud.get_contact_by_phone(db, phone=contact.phone)
    if db_contact_by_phone and db_contact_by_phone.id != contact_id:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact."""
    success = crud.delete_contact(db, contact_id=contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}
