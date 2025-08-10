import z from "zod";

export interface ChatFormData {
	content: string;
}

export const chatFormSchema = z.object({
	content: z
		.string()
		.min(2, "Please enter at least 2 characters to send a message.")
		.max(
			400,
			"Message too long! Please keep it under 400 characters. Tokens are not cheap.",
		),
});
