import type { ChatFormData } from "../components/features/chat/ChatForm/data";
import type { ChatResponse } from "../types/chat";

export const sendMessage = async (
	body: ChatFormData,
): Promise<ChatResponse> => {
	const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
		body: JSON.stringify(body),
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
	});

	if (!response.ok) {
		throw new Error(`HTTP error! status: ${response.status}`);
	}

	return response.json();
};
