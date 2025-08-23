from pydantic import BaseModel
from src.db.schemas import Contact


class McpResponse(BaseModel):
    success: bool
    message: str | None = None


class ContactResponse(Contact):
    pass


class GetContactsResponse(McpResponse):
    contacts: list[Contact] | None = None


class GetContactResponse(McpResponse):
    contact: Contact | None = None
