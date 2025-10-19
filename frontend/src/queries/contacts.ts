import type { Contact } from "../types/contact";

export const getContacts = async (): Promise<Contact[]> => {
	const response = await fetch("/api/contacts");
	if (!response.ok) {
		throw new Error("Failed to fetch contacts");
	}
	return response.json();
};

export const addContact = async (
	contact: Omit<Contact, "id">,
): Promise<Contact> => {
	const response = await fetch("/api/contacts", {
		body: JSON.stringify(contact),
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
	});
	if (!response.ok) {
		console.log("Error adding contact:", response.statusText);
		throw new Error("Failed to add contact");
	}
	return response.json();
};

export const updateContact = async (contact: Contact): Promise<Contact> => {
	const { id, ...newContactBody } = contact;
	const response = await fetch(`/api/contacts/${id}`, {
		body: JSON.stringify(newContactBody),
		headers: {
			"Content-Type": "application/json",
		},
		method: "PUT",
	});
	if (!response.ok) {
		console.log("Error updating contact:", response.statusText);
		throw new Error("Failed to update contact");
	}
	return response.json();
};

export const deleteContact = async (id: number) => {
	const response = await fetch(`/api/contacts/${id}`, {
		method: "DELETE",
	});
	if (!response.ok) {
		console.log("Error deleting contact:", response.statusText);
		throw new Error("Failed to delete contact");
	}
	return response.json();
};
