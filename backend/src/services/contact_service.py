from typing import List, Optional

from sqlalchemy.orm import Session
from src.db.models.Contact import ContactModel
from src.db.schemas import ContactCreate, ContactUpdate


class ContactService:
    def get_contacts(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ContactModel]:  # Return SQLAlchemy model
        """Get all contacts with pagination."""
        return sorted(
            db.query(ContactModel).offset(skip).limit(limit).all(), key=lambda c: c.id
        )

    def get_contact_by_phone(self, db: Session, phone: str) -> Optional[ContactModel]:
        """Get a contact by phone number."""
        return db.query(ContactModel).filter(ContactModel.phone == phone).first()

    def get_contact_by_id(self, db: Session, contact_id: int) -> Optional[ContactModel]:
        """Get detailed information about a specific contact by ID."""
        return db.query(ContactModel).filter(ContactModel.id == contact_id).first()

    def get_contact_by_name(self, db: Session, name: str) -> Optional[ContactModel]:
        """Get a contact by exact name (case-insensitive)."""
        return db.query(ContactModel).filter(ContactModel.name.ilike(name)).first()

    def create_contact(self, db: Session, contact: ContactCreate) -> ContactModel:
        """Create a new contact."""
        # Check for duplicate phone numbers
        existing_contact = self.get_contact_by_phone(db, contact.phone)
        if existing_contact:
            raise ValueError(
                f"Contact with phone number {contact.phone} already exists"
            )

        db_contact = ContactModel(name=contact.name, phone=contact.phone)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    def update_contact_by_id(
        self, db: Session, contact_id: int, contact: ContactUpdate
    ) -> Optional[ContactModel]:
        """Update an existing contact by ID."""
        db_contact = (
            db.query(ContactModel).filter(ContactModel.id == contact_id).first()
        )
        if db_contact:
            db_contact.name = contact.name
            db_contact.phone = contact.phone
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete_contact(self, db: Session, contact_id: int) -> bool:
        """Delete a contact by ID."""
        db_contact = (
            db.query(ContactModel).filter(ContactModel.id == contact_id).first()
        )
        if db_contact:
            db.delete(db_contact)
            db.commit()
            return True
        return False

    def update_contact_by_phone_num(
        self, db: Session, phone: str, contact: ContactUpdate
    ) -> Optional[ContactModel]:
        """Update a contact by phone number."""
        db_contact = db.query(ContactModel).filter(ContactModel.phone == phone).first()
        if db_contact:
            db_contact.name = contact.name
            db_contact.phone = contact.phone
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete_contact_by_phone(self, db: Session, phone: str) -> bool:
        """Delete a contact by phone number."""
        db_contact = db.query(ContactModel).filter(ContactModel.phone == phone).first()
        if db_contact:
            db.delete(db_contact)
            db.commit()
            return True
        return False

    def delete_contact_by_name(self, db: Session, name: str) -> bool:
        """Delete a contact by name (case-insensitive)."""
        db_contact = (
            db.query(ContactModel).filter(ContactModel.name.ilike(name)).first()
        )
        if db_contact:
            db.delete(db_contact)
            db.commit()
            return True
        return False

    def update_contact_by_name(
        self, db: Session, name: str, contact: ContactUpdate
    ) -> Optional[ContactModel]:
        """Update a contact found by name (case-insensitive)."""
        db_contact = (
            db.query(ContactModel).filter(ContactModel.name.ilike(name)).first()
        )
        if db_contact:
            db_contact.name = contact.name
            db_contact.phone = contact.phone
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def search_contacts(self, db: Session, query: str) -> List[ContactModel]:
        """Search contacts by name or phone number."""
        return (
            db.query(ContactModel)
            .filter(
                ContactModel.name.ilike(f"%{query}%")
                | ContactModel.phone.ilike(f"%{query}%")
            )
            .all()
        )


def get_contact_service() -> ContactService:
    """Dependency to get the contact service."""
    return ContactService()
