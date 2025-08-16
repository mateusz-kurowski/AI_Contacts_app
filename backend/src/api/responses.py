from enum import Enum


class Response(Enum):
    CONTACT_NOT_FOUND = "Contact not found"
    CONTACT_ALREADY_EXISTS = "Contact already exists"
    CONTACT_UPDATED = "Contact updated successfully"
    CONTACT_DELETED = "Contact deleted successfully"
