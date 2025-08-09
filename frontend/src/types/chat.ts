export interface ChatResponse {
	content: string;
	id: string;
	role: "user" | "assistant";
	createdAt: string;
}
