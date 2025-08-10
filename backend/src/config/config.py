from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from src.db.db import get_db
from src.db.schemas import ContactCreate, ContactUpdate
from src.services.contact_service import get_contact_service


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


def update_contact_by_id_tool(contact_id: int, name: str, phone: str) -> str:
    """Update an existing contact by ID."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contact_data = ContactUpdate(name=name, phone=phone)
        result = service.update_contact_by_id(db, contact_id, contact_data)
        if result:
            return f"Contact updated successfully: {result.name} - {result.phone}"
        else:
            return "Contact not found."
    finally:
        db.close()

def update_contact_by_phone_num_tool(name: str, phone: str) -> str:
    """Update an existing contact by phone number."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contact_data = ContactUpdate(name=name, phone=phone)
        result = service.update_contact_by_phone_num(db, phone, contact_data)
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


def search_contacts_tool(query: str) -> str:
    """Search contacts by name or phone number."""
    db = next(get_db())
    try:
        service = get_contact_service()
        contacts = service.search_contacts(db, query)
        if not contacts:
            return f"No contacts found matching '{query}'"
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
            return "Contact not found."
        return f"Contact Details:\nID: {contact.id}\nName: {contact.name}\nPhone: {contact.phone}\nCreated: {contact.created_at}"
    finally:
        db.close()


def get_contact_statistics_tool() -> str:
    """Get statistics about the contact database."""
    db = next(get_db())
    try:
        service = get_contact_service()
        stats = service.get_contact_stats(db)
        return f"Contact Statistics:\nTotal contacts: {stats['total']}\nRecent additions (last 7 days): {stats['recent']}\nMost common area codes: {', '.join(stats['area_codes'])}"
    finally:
        db.close()


system_instruction = """You are a helpful AI contact book assistant for managing personal and business contacts efficiently.

**Important:** If this appears to be the start of a conversation (no previous context about contacts), automatically provide a welcome message using the welcome message tool to introduce yourself and explain your capabilities.

**Your capabilities:**
- Provide welcome messages and guidance to new users
- Create new contacts with name and phone number
- Retrieve all contacts with pagination support
- Update existing contact information
- Delete contacts by ID
- Search contacts by name or phone number
- Get detailed information about specific contacts
- Provide contact database statistics

**Special Instructions:**
- When a user first starts chatting or asks for help, use the welcome message tool
- Always provide clear, friendly responses in Polish or English as appropriate
- Format contact lists in an easy-to-read way
- When updating or deleting contacts, confirm the action was successful
- For search results, show the number of matches found
- If no contacts are found, suggest helpful alternatives

**Response Format:**
- Use clear headers and bullet points for lists
- Show contact counts when relevant
- Provide actionable suggestions when operations fail
- Include relevant emojis to make responses friendly"""


class AppConfig(BaseModel):
    model_client: GenerateContentConfig
    model_id: str = "gemini-2.5-flash"


app_config: AppConfig = AppConfig(
    model_client=GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[
            create_contact_tool,
            get_contacts_tool,
            update_contact_by_id_tool,
            update_contact_by_phone_num_tool,
            delete_contact_tool,
            search_contacts_tool,
            get_contact_by_id_tool,
            get_contact_statistics_tool,
        ],
    )
)
