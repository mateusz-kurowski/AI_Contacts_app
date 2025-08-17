from enum import Enum


class Response(Enum):
    CONTACT_NOT_FOUND = "Contact not found"
    NO_CONTACTS_FOUND = "No contacts found"
    CONTACT_ALREADY_EXISTS = "Contact already exists"
    CONTACT_UPDATED = "Contact updated successfully"
    CONTACT_DELETED = "Contact deleted successfully"

    CONTACT_CREATION_FAILED = "Failed to create contact"
    CONTACT_RETRIEVAL_FAILED = "Failed to retrieve contact"
    CONTACT_UPDATE_FAILED = "Failed to update contact"
    CONTACT_DELETION_FAILED = "Failed to delete contact"