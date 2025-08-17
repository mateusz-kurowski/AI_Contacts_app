from fastmcp import FastMCP
from typing import List
from src.services.contact_service import get_contact_service
from src.db.db import get_db
from src.db.schemas import ContactCreate, ContactUpdate, Contact
from typing import Annotated
from src.api.responses import Response
from src.db.schemas import phone_e164_regex
from pydantic import Field


def register_contact_tools(mcp: FastMCP):
    @mcp.tool(
        annotations={
            "title": "Get Contacts",
            "description": "Retrieve a list of all contacts",
        },
        tags=["contacts"],
    )
    def get_contacts() -> list[Contact]:
        """Get all contacts from the database"""
        db = next(get_db())
        try:
            contacts = get_contact_service().get_contacts(db)
            return [contact.dict() for contact in contacts]
        except Exception:
            return {"error": Response.CONTACT_RETRIEVAL_FAILED}
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Get Contact by ID",
            "description": "Retrieve a specific contact by their ID",
        },
        tags=["contacts"],
    )
    def get_contact_by_id(
        contact_id: Annotated[int, "The ID of the contact to retrieve"],
    ) -> Contact:
        """Get a specific contact by their ID"""
        db = next(get_db())
        try:
            contact = get_contact_service().get_contact_by_id(db, contact_id=contact_id)
            if not contact:
                return {"error": Response.CONTACT_NOT_FOUND}
            return {"id": contact.id, "name": contact.name, "phone": contact.phone}
        except Exception as e:
            return {"error": f"Failed to get contact: {str(e)}"}
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Create Contact",
            "description": "Create a new contact with name and phone number",
        },
        tags=["contacts"],
    )
    def create_contact(
        name: Annotated[str, "The name of the contact"],
        phone: Annotated[
            str,
            Field(
                description="The phone number of the contact (E.164 format like +1234567890)",
                pattern=phone_e164_regex.pattern,
            ),
        ],
    ) -> Contact:
        """Create a new contact with name and phone number (E.164 format like +1234567890)"""
        db = next(get_db())
        try:
            existing_contact = get_contact_service().get_contact_by_phone(
                db, phone=phone
            )
            if existing_contact:
                return {"error": "Contact with this phone number already exists"}
            contact_data = ContactCreate(name=name, phone=phone)
            created_contact = get_contact_service().create_contact(db, contact_data)
            return {
                "id": created_contact.id,
                "name": created_contact.name,
                "phone": created_contact.phone,
                "message": "Contact created successfully",
            }
        except ValueError as e:
            return {"error": str(e)}
        except Exception:
            return {"error": Response.CONTACT_CREATION_FAILED}
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Update Contact",
            "description": "Update an existing contact's information",
        },
        tags=["contacts"],
    )
    def update_contact(
        contact_id: Annotated[int, "The ID of the contact to update"],
        name: Annotated[str, "The new name of the contact"],
        phone: Annotated[
            str,
            Field(
                description="The new phone number of the contact",
                pattern=phone_e164_regex.pattern,
            ),
        ],
    ) -> Contact | dict:
        """Update an existing contact's information"""
        db = next(get_db())
        try:
            # Check if contact exists
            existing_contact = get_contact_service().get_contact_by_id(
                db, contact_id=contact_id
            )
            if not existing_contact:
                return {"error": "Contact not found"}
            contact_with_phone = get_contact_service().get_contact_by_phone(
                db, phone=phone
            )
            if contact_with_phone and contact_with_phone.id != contact_id:
                return {"error": "Phone number already registered to another contact"}
            contact_data = ContactUpdate(name=name, phone=phone)
            updated_contact = get_contact_service().update_contact_by_id(
                db, contact_id=contact_id, contact=contact_data
            )
            if not updated_contact:
                return {"error": Response.CONTACT_UPDATE_FAILED}
            return {
                **updated_contact.dict(),
                "message": Response.CONTACT_UPDATED,
            }
        except ValueError as e:
            return {"error": str(e)}
        except Exception:
            return {"error": Response.CONTACT_UPDATE_FAILED}
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Delete Contact",
            "description": "Delete a contact by their ID",
        },
        tags=["contacts"],
    )
    def delete_contact(
        contact_id: Annotated[int, "The ID of the contact to delete"],
    ) -> dict:
        """Delete a contact by their ID"""
        db = next(get_db())
        try:
            success = get_contact_service().delete_contact(db, contact_id=contact_id)
            if not success:
                return {"error": Response.CONTACT_NOT_FOUND}
            return {"message": Response.CONTACT_DELETED}
        except Exception:
            return {"error": Response.CONTACT_DELETION_FAILED}
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Search Contacts",
            "description": "Search contacts by name or phone number",
        },
        tags=["contacts"],
    )
    def search_contacts(
        query: Annotated[str, "The search query (name or phone number)"],
    ) -> List[Contact] | dict:
        """Search contacts by name or phone number"""
        db = next(get_db())
        try:
            contacts = get_contact_service().search_contacts(db, query=query)
            return [contact.dict() for contact in contacts]
        except Exception:
            return {"error": Response.CONTACT_RETRIEVAL_FAILED}
        finally:
            db.close()
