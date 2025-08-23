from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field
from src.api.responses import Response
from src.db.db import get_db
from src.db.schemas import ContactCreate, ContactUpdate
from src.mcp.tools.schema import GetContactResponse, GetContactsResponse, McpResponse
from src.services.contact_service import get_contact_service
from src.utils.phone import format_phone_number


def register_contact_tools(mcp: FastMCP):
    @mcp.tool(
        annotations={
            "title": "Get Contacts",
            "description": "Retrieve a list of all contacts",
        },
        tags=["contacts"],
    )
    def get_contacts() -> GetContactsResponse:
        """Get all contacts from the database"""
        db = next(get_db())
        try:
            contacts = get_contact_service().get_contacts(db)
            return GetContactsResponse(
                success=True,
                contacts=contacts,
            )
        except Exception:
            return GetContactResponse(
                success=False,
                message=Response.CONTACT_RETRIEVAL_FAILED,
            )
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
    ) -> GetContactResponse:
        """Get a specific contact by their ID"""
        db = next(get_db())
        try:
            contact = get_contact_service().get_contact_by_id(db, contact_id=contact_id)
            if not contact:
                return GetContactResponse(
                    success=False,
                    message=Response.CONTACT_NOT_FOUND,
                )
            return GetContactResponse(
                success=True,
                contact=contact,
            )
        except Exception as e:
            return GetContactResponse(
                success=False,
                message=f"Failed to get contact: {str(e)}",
            )
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Get Contact by Phone Number",
            "description": "Retrieve a specific contact by their phone number",
        },
        tags=["contacts"],
    )
    def get_contact_by_phone_number(
        phone: Annotated[str, "The phone number of the contact to retrieve"],
    ) -> GetContactResponse:
        """Get a specific contact by their phone number"""
        db = next(get_db())
        try:
            formatted_number = format_phone_number(phone)
            if not formatted_number:
                return GetContactResponse(
                    success=False,
                    message="Invalid phone number format",
                )
            contact = get_contact_service().get_contact_by_phone(
                db, phone=formatted_number
            )
            if not contact:
                return GetContactResponse(
                    success=False,
                    message=Response.CONTACT_NOT_FOUND,
                )
            return GetContactResponse(
                success=True,
                contact=contact,
            )
        except Exception as e:
            return GetContactResponse(
                success=False,
                message=f"Failed to get contact: {str(e)}",
            )
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
                description="The phone number of the contact",
            ),
        ],
    ) -> GetContactResponse:
        """Create a new contact with name and phone number (E.164 format like +1234567890)"""
        db = next(get_db())
        try:
            formatted_number = format_phone_number(phone)
            if not formatted_number:
                return GetContactResponse(
                    success=False,
                    message="Invalid phone number format",
                )
            existing_contact = get_contact_service().get_contact_by_phone(
                db, phone=formatted_number
            )
            if existing_contact:
                return GetContactResponse(
                    success=False,
                    message="Contact with this phone number already exists",
                    contact=existing_contact,
                )
            contact_data = ContactCreate(name=name, phone=formatted_number)
            created_contact = get_contact_service().create_contact(db, contact_data)
            return GetContactResponse(
                success=True,
                contact=created_contact,
            )
        except Exception as e:
            return GetContactResponse(
                success=False,
                message=str(e),
            )
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
            "The new phone number of the contact",
        ],
    ) -> GetContactResponse:
        """Update an existing contact's information"""
        db = next(get_db())
        try:
            # Check if contact exists
            existing_contact = get_contact_service().get_contact_by_id(
                db, contact_id=contact_id
            )
            if not existing_contact:
                return GetContactResponse(
                    success=False,
                    message="Contact not found",
                )
            contact_with_phone = get_contact_service().get_contact_by_phone(
                db, phone=phone
            )
            if contact_with_phone and contact_with_phone.id != contact_id:
                return GetContactResponse(
                    success=False,
                    message="Phone number already registered to another contact",
                )
            contact_data = ContactUpdate(name=name, phone=phone)
            updated_contact = get_contact_service().update_contact_by_id(
                db, contact_id=contact_id, contact=contact_data
            )
            if not updated_contact:
                return GetContactResponse(
                    success=False,
                    message=Response.CONTACT_UPDATE_FAILED,
                )
            return GetContactResponse(
                success=True,
                contact=updated_contact,
            )
        except ValueError as e:
            return GetContactResponse(
                success=False,
                message=str(e),
            )
        except Exception:
            return GetContactResponse(
                success=False,
                message=Response.CONTACT_UPDATE_FAILED,
            )
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
    ) -> McpResponse:
        """Delete a contact by their ID"""
        db = next(get_db())
        try:
            success = get_contact_service().delete_contact(db, contact_id=contact_id)
            if not success:
                return McpResponse(
                    success=False,
                    message=Response.CONTACT_NOT_FOUND,
                )
            return McpResponse(
                success=True,
                message=Response.CONTACT_DELETED,
            )
        except Exception:
            return McpResponse(
                success=False,
                message=Response.CONTACT_DELETION_FAILED,
            )
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
    ) -> GetContactsResponse:
        """Search contacts by name or phone number"""
        db = next(get_db())
        try:
            contacts = get_contact_service().search_contacts(db, query=query)
            return GetContactsResponse(
                success=True,
                message="Contacts retrieved successfully",
                contacts=contacts,
            )
        except Exception:
            return GetContactsResponse(
                success=False,
                message=Response.CONTACT_RETRIEVAL_FAILED,
            )
        finally:
            db.close()

    @mcp.tool(
        annotations={
            "title": "Format Phone Number",
            "description": "Format a phone number to E.164 standard",
        },
        tags=["contacts"],
    )
    def format_phone_number_tool(
        phone: str, default_region: str = "PL"
    ) -> GetContactResponse:
        """
        Format phone number to E.164.
        Returns None if invalid or cannot be parsed.
        """
        formatted = format_phone_number(phone, default_region)
        if not formatted:
            return GetContactResponse(
                success=False,
                message=Response.INVALID_PHONE_NUMBER,
            )
        return GetContactResponse(
            success=True,
            contact=formatted,
        )
