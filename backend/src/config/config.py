from pydantic import BaseModel
from google.genai.types import GenerateContentConfig
from src.db.db import get_db
from src.services.contact_service import get_contact_service
from src.db.schemas import ContactCreate, ContactUpdate


# Create wrapper functions that handle db internally
def create_contact_tool(name: str, phone: str) -> str:
    """Create a new contact with the given name and phone number."""
    db = next(get_db())  # Get a database session
    try:
        service = get_contact_service()
        contact_data = ContactCreate(name=name, phone=phone)
        result = service.create_contact(db, contact_data)
        return f"Contact created successfully: {result.name} - {result.phone}"
    finally:
        db.close()


def get_contacts_tool(skip: int = 0, limit: int = 10) -> str:
    """Get all contacts with pagination."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contacts = service.get_contacts(db, skip, limit)
        if not contacts:
            return "No contacts found."
        contact_list = [f"{c.name}: {c.phone}" for c in contacts]
        return "Contacts:\n" + "\n".join(contact_list)
    finally:
        db.close()


def update_contact_tool(contact_id: int, name: str, phone: str) -> str:
    """Update an existing contact by ID."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contact_data = ContactUpdate(name=name, phone=phone)
        result = service.update_contact(db, contact_id, contact_data)
        if result:
            return f"Contact updated successfully: {result.name} - {result.phone}"
        else:
            return "Contact not found."
    finally:
        db.close()


def delete_contact_tool(contact_id: int) -> str:
    """Delete a contact by ID."""
    db = next(get_db())
    try:
        service = get_contact_service()
        success = service.delete_contact(db, contact_id)
        return "Contact deleted successfully." if success else "Contact not found."
    finally:
        db.close()


class AppConfig(BaseModel):
    model_client: GenerateContentConfig
    model_id: str = "gemini-2.5-flash"


app_config: AppConfig = AppConfig(
    model_client=GenerateContentConfig(
        system_instruction="You are a helpful contact book assistant. Your task is to help users manage their contacts.",
        tools=[
            create_contact_tool,
            get_contacts_tool,
            update_contact_tool,
            delete_contact_tool,
        ],
    )
)
