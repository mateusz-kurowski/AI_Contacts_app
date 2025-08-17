from src.db.db import get_db
from src.db.schemas import ContactCreate, ContactUpdate
from src.services.contact_service import get_contact_service
from src.api.responses import Response

def create_contact_tool(name: str, phone: str) -> str:
    """Create a new contact with the given name and phone number."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contact_data = ContactCreate(name=name, phone=phone)
        result = service.create_contact(db, contact_data)
        return f"Contact created successfully: {result.name} - {result.phone}"
    finally:
        db.close()


def get_contacts_tool() -> str:
    """Get all contacts."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contacts = service.get_contacts(db)
        if not contacts:
            return Response.NO_CONTACTS_FOUND
        contact_list = [f"{c.name}: {c.phone}" for c in contacts]
        return "Contacts:\n" + "\n".join(contact_list)
    finally:
        db.close()


def update_contact_by_phone_num_tool(phone: str, name: str, new_phone: str) -> str:
    """Update an existing contact by phone number."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contact_data = ContactUpdate(name=name, phone=new_phone)
        result = service.update_contact_by_phone_num(db, phone, contact_data)
        if result:
            return f"Contact updated successfully: {result.name} - {result.phone}"
        else:
            return Response.NO_CONTACTS_FOUND
    finally:
        db.close()


def delete_contact_by_number_tool(phone: str) -> str:
    """Delete a contact by phone number."""
    db = next(get_db())
    try:
        service = get_contact_service()
        success = service.delete_contact_by_phone(db, phone)
        return "Contact deleted successfully." if success else "Contact not found."
    finally:
        db.close()


def search_contacts_tool(query: str) -> str:
    """Search contacts by name or phone number."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contacts = service.search_contacts(db, query)
        if not contacts:
            return Response.NO_CONTACTS_FOUND
        contact_list = [f"{c.name}: {c.phone}" for c in contacts]
        return f"Found {len(contacts)} contact(s) matching '{query}':\n" + "\n".join(
            contact_list
        )
    finally:
        db.close()


def get_contact_by_id_tool(contact_id: int) -> str:
    """Get detailed information about a specific contact by ID."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contact = service.get_contact_by_id(db, contact_id)
        if not contact:
            return Response.CONTACT_NOT_FOUND
        return f"Contact Details:\nID: {contact.id}\nName: {contact.name}\nPhone: {contact.phone}\nCreated: {contact.created_at}"
    finally:
        db.close()
