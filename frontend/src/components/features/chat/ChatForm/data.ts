import z from "zod";

export interface ChatFormData {
	content: string;
}

export const chatFormSchema = z.object({
	content: z
		.string()
		.min(2, "Input is too short.")
		.max(100, "Tokens are limited. Please shorten your message."),
});
