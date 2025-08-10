import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Send } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { v4 as uuidv4 } from "uuid";
import type z from "zod";
import { sendMessage } from "../../../../queries/chat";
import { useChatStore } from "../../../../stores/chatStore";
import { Button } from "../../../ui/button";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
} from "../../../ui/form";
import { Textarea } from "../../../ui/textarea";
import { type ChatFormData, chatFormSchema } from "./data";

const ChatForm = () => {
	const queryClient = useQueryClient();
	const chatForm = useForm<z.infer<typeof chatFormSchema>>({
		defaultValues: {
			content: "",
		},
		resolver: zodResolver(chatFormSchema),
	});
	const { addMessage, setIsTyping } = useChatStore();

	const chatMutation = useMutation({
		mutationFn: sendMessage,
		mutationKey: ["newMessage"],
		onError: (error: Error) => {
			toast.error("Error sending message", {
				action: {
					label: "Retry",
					onClick: () => chatMutation.mutate(chatForm.getValues()),
				},
				description: error.message,
			});
		},
	});

	const handleSubmit = async (data: ChatFormData) => {
		try {
			addMessage({
				content: data.content,
				createdAt: new Date(),
				id: uuidv4(),
				role: "user",
			});
			chatForm.reset();
			setIsTyping(true);
			const response = await chatMutation.mutateAsync(data);
			addMessage({ ...response, createdAt: new Date(response.createdAt) });
			queryClient.invalidateQueries({ queryKey: ["contacts"] });
		} catch {
			setIsTyping(false);
			toast.error("Error sending message", {
				action: {
					label: "Retry",
					onClick: () => chatMutation.mutate(chatForm.getValues()),
				},
			});
		}
	};

	return (
		<div className="w-full max-w-2xl mx-auto">
			<Form {...chatForm}>
				<form onSubmit={chatForm.handleSubmit(handleSubmit)}>
					<FormField
						control={chatForm.control}
						name="content"
						render={({ field }) => (
							<FormItem>
								<div className="relative">
									<FormControl>
										<Textarea
											{...field}
											className="w-full max-w-full min-h-[60px] max-h-[120px] resize-none pr-12 py-4 text-base border-2 focus:border-primary/50 transition-colors overflow-y-auto"
											placeholder="Ask anything..."
											rows={3}
											style={{ resize: "none" }}
										/>
									</FormControl>
									<Button
										className="absolute bottom-3 right-3 h-8 w-8 p-0"
										size="sm"
										type="submit"
									>
										<Send className="h-4 w-4" />
									</Button>
								</div>
								<FormLabel>Chat history is not stored on the server.</FormLabel>
							</FormItem>
						)}
					/>
				</form>
			</Form>
		</div>
	);
};

export default ChatForm;
