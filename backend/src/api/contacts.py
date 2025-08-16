from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.db import get_db
from src.db.schemas import ContactCreate, Contact, ContactUpdate
from src.services.contact_service import ContactService, get_contact_service
from src.api.responses import Response

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=Contact)
@router.post("", response_model=Contact)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    db_contact = svc.get_contact_by_phone(db, phone=contact.phone)
    if db_contact:
        raise HTTPException(
            status_code=400, detail=Response.CONTACT_ALREADY_EXISTS.value
        )

    created_contact = svc.create_contact(db=db, contact=contact)

    return Contact.model_validate(created_contact)


@router.get("/", response_model=List[Contact])
@router.get("", response_model=List[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    contacts = svc.get_contacts(db, skip=skip, limit=limit)

    return [Contact.model_validate(contact) for contact in contacts]


@router.get("/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    db_contact = svc.get_contact_by_id(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail=Response.CONTACT_NOT_FOUND)

    return Contact.model_validate(db_contact)


@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    db_contact_by_phone = svc.get_contact_by_phone(db, phone=contact.phone)
    if db_contact_by_phone and db_contact_by_phone.id != contact_id:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    db_contact = svc.update_contact_by_id(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return Contact.model_validate(db_contact)


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    svc: ContactService = Depends(get_contact_service),
):
    success = svc.delete_contact(db, contact_id=contact_id)
    if not success:
        raise HTTPException(status_code=404, detail=Response.CONTACT_NOT_FOUND.value)
    return {"message": Response.CONTACT_DELETED.value}