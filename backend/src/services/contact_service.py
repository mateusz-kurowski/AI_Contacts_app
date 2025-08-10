from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session
from src.db.Contact import Contact
from src.db.schemas import ContactCreate, ContactUpdate


class ContactService:
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
        # Check for duplicate phone numbers
        existing_contact = self.get_contact_by_phone(db, contact.phone)
        if existing_contact:
            raise ValueError(
                f"Contact with phone number {contact.phone} already exists"
            )

        db_contact = Contact(name=contact.name, phone=contact.phone)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    def update_contact_by_id(
        self, db: Session, contact_id: int, contact: ContactUpdate
    ) -> Optional[Contact]:
        """Update an existing contact by ID."""
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

    def update_contact_by_phone_num(
        self, db: Session, phone: str, contact: ContactUpdate
    ) -> Optional[Contact]:
        """Update a contact by phone number."""
        db_contact = db.query(Contact).filter(Contact.phone == phone).first()
        if db_contact:
            db_contact.name = contact.name
            db_contact.phone = contact.phone
            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete_contact_by_phone(self, db: Session, phone: str) -> bool:
        """Delete a contact by phone number."""
        db_contact = db.query(Contact).filter(Contact.phone == phone).first()
        if db_contact:
            db.delete(db_contact)
            db.commit()
            return True
        return False

    def search_contacts(self, db: Session, query: str) -> List[Contact]:
        """Search contacts by name or phone number."""
        return (
            db.query(Contact)
            .filter(
                Contact.name.ilike(f"%{query}%") | Contact.phone.ilike(f"%{query}%")
            )
            .all()
        )

    def get_contact_by_id(self, db: Session, contact_id: int) -> Optional[Contact]:
        """Get detailed information about a specific contact by ID."""
        return db.query(Contact).filter(Contact.id == contact_id).first()

    def get_contact_stats(self, db: Session) -> dict:
        """Get contact database statistics."""
        total = db.query(Contact).count()
        recent_date = datetime.now() - timedelta(days=7)
        recent = db.query(Contact).filter(Contact.created_at >= recent_date).count()

        contacts = db.query(Contact).all()
        area_codes = {}
        for contact in contacts:
            digits = "".join(filter(str.isdigit, contact.phone))
            if len(digits) >= 3:
                area_code = digits[:3]
                area_codes[area_code] = area_codes.get(area_code, 0) + 1

        most_common = sorted(area_codes.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "total": total,
            "recent": recent,
            "area_codes": [code for code, _ in most_common],
        }


def get_contact_service() -> ContactService:
    """Dependency to get the contact service."""
    return ContactService()
