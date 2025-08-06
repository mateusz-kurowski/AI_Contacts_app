from sqlalchemy.orm import Session
from typing import List, Optional
from .Contact import Contact
from .schema import ContactCreate, ContactUpdate


def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    """Get a single contact by ID."""
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    """Get all contacts with pagination."""
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact_by_phone(db: Session, phone: str) -> Optional[Contact]:
    """Get a contact by phone number."""
    return db.query(Contact).filter(Contact.phone == phone).first()


def create_contact(db: Session, contact: ContactCreate) -> Contact:
    """Create a new contact."""
    db_contact = Contact(name=contact.name, phone=contact.phone)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(
    db: Session, contact_id: int, contact: ContactUpdate
) -> Optional[Contact]:
    """Update an existing contact."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db_contact.name = contact.name
        db_contact.phone = contact.phone
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int) -> bool:
    """Delete a contact by ID."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False
