from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.db import get_db
from src.db.schemas import ContactCreate, ContactOut, ContactUpdate
from src.services.contact_service import ContactService, get_contact_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactOut)
@router.post("", response_model=ContactOut)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    """Create a new contact."""
    # Check if phone number already exists
    db_contact = svc.get_contact_by_phone(db, phone=contact.phone)
    if db_contact:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return svc.create_contact(db=db, contact=contact)


@router.get("/", response_model=List[ContactOut])
@router.get("", response_model=List[ContactOut])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    """Retrieve all contacts with pagination."""
    contacts = svc.get_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/{contact_id}", response_model=ContactOut)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    """Retrieve a specific contact by ID."""
    db_contact = svc.get_contact_by_id(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    """Update an existing contact."""
    # Check if phone number already exists for a different contact
    db_contact_by_phone = svc.get_contact_by_phone(db, phone=contact.phone)
    if db_contact_by_phone and db_contact_by_phone.id != contact_id:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    db_contact = svc.update_contact_by_id(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    """Delete a contact."""
    success = svc.delete_contact(db, contact_id=contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}
