from typing import List, Optional

from sqlalchemy.orm import Session
from src.db.Contact import Contact
from src.db.schemas import ContactCreate, ContactUpdate


class ContactService:
    def get_contact(self, db: Session, contact_id: int) -> Optional[Contact]:
        """Get a single contact by ID."""
        return db.query(Contact).filter(Contact.id == contact_id).first()

    def get_contacts(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        """Get all contacts with pagination."""
        return sorted(
            db.query(Contact).offset(skip).limit(limit).all(), key=lambda c: c.name
        )

    def get_contact_by_phone(self, db: Session, phone: str) -> Optional[Contact]:
        """Get a contact by phone number."""
        return db.query(Contact).filter(Contact.phone == phone).first()

    def create_contact(self, db: Session, contact: ContactCreate) -> Contact:
        """Create a new contact."""
        db_contact = Contact(name=contact.name, phone=contact.phone)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    def update_contact(
        self, db: Session, contact_id: int, contact: ContactUpdate
    ) -> Optional[Contact]:
        """Update an existing contact."""
        db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if db_contact:
            db_contact.name = contact.name
            db_contact.phone = contact.phone
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete_contact(self, db: Session, contact_id: int) -> bool:
        """Delete a contact by ID."""
        db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if db_contact:
            db.delete(db_contact)
            db.commit()
            return True
        return False


def get_contact_service() -> ContactService:
    """Dependency to get the contact service."""
    return ContactService()
