import type { Contact } from "../types/contact";

export const getContacts = async (): Promise<Contact[]> => {
	const response = await fetch(`${import.meta.env.VITE_API_URL}/contacts`);
	if (!response.ok) {
		throw new Error("Failed to fetch contacts");
	}
	return response.json();
};

export const addContact = async (
	contact: Omit<Contact, "id">,
): Promise<Contact> => {
	const response = await fetch(`${import.meta.env.VITE_API_URL}/contacts`, {
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

export const deleteContact = async (id: number) => {
	const response = await fetch(
		`${import.meta.env.VITE_API_URL}/contacts/${id}`,
		{
			method: "DELETE",
		},
	);
	if (!response.ok) {
		console.log("Error deleting contact:", response.statusText);
		throw new Error("Failed to delete contact");
	}
	return response.json();
};
