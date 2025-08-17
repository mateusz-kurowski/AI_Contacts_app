from fastmcp import FastMCP


def register_contacts_prompts(mcp: FastMCP):
    @mcp.prompt
    def get_contacts_list():
        """Generates a user message for retrieving all contacts"""
        return "Please provide a list of all contacts."

    @mcp.prompt
    def create_contact_prompt(name: str, phone: str):
        """Generates a user message for creating a new contact"""
        return f"Please provide the name and phone number of the new contact: {name}, {phone}."

    @mcp.prompt
    def update_contact_prompt(contact_id: int, name: str, phone: str):
        """Generates a user message for updating an existing contact"""
        return f"Please provide the ID of the contact to update: {contact_id}, along with the new name and phone number: {name}, {phone}."

    @mcp.prompt
    def delete_contact_prompt(contact_id: int):
        """Generates a user message for deleting a contact"""
        return f"Please provide the ID of the contact to delete: {contact_id}."

    @mcp.prompt
    def get_contact_details_prompt(contact_id: int):
        """Generates a user message for retrieving details of a specific contact"""
        return f"Please provide the ID of the contact to retrieve: {contact_id}."

    @mcp.prompt
    def get_contact_details_by_phone_number_prompt(phone_number: str):
        """Generates a user message for retrieving details of a specific contact by phone number"""
        return f"Please provide the details of the contact with a phone number: {phone_number}."
