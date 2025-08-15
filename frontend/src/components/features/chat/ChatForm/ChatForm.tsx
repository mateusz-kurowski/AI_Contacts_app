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
	FormMessage,
} from "../../../ui/form";
import { Textarea } from "../../../ui/textarea";
import { type ChatFormData, chatFormSchema } from "./data";

const ChatForm = () => {
	const queryClient = useQueryClient();
	const chatForm = useForm<z.infer<typeof chatFormSchema>>({
		defaultValues: {
			content: "",
		},
		mode: "onSubmit",
		resolver: zodResolver(chatFormSchema),
		reValidateMode: "onBlur",
	});
	const { addMessage, setIsTyping } = useChatStore();
	let lastSubmittedData: ChatFormData | null = null;
	const chatMutation = useMutation({
		mutationFn: sendMessage,
		mutationKey: ["newMessage"],
		onError: (error: Error) => {
			toast.error("Error sending message", {
				action: {
					label: "Retry",
					onClick: () =>
						lastSubmittedData && chatMutation.mutate(lastSubmittedData),
				},
				description: error.message,
			});
			chatForm.setValue("content", lastSubmittedData?.content || "");
		},
		onMutate: (data) => {
			chatForm.reset();
			setIsTyping(true);
			addMessage({
				content: data.content,
				createdAt: new Date(),
				id: uuidv4(),
				role: "user",
			});
		},
		onSettled: () => {
			lastSubmittedData = null;
			setIsTyping(false);
		},
		onSuccess: (data) => {
			addMessage({ ...data, createdAt: new Date(data.createdAt) });
			queryClient.invalidateQueries({ queryKey: ["contacts"] });
		},
	});

	const handleSubmit = (data: ChatFormData) => {
		lastSubmittedData = data;
		chatMutation.mutate(data);
	};

	const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
		if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
			e.preventDefault();
			chatForm.handleSubmit(handleSubmit)();
		}
	};

	return (
		<div className="w-full max-w-2xl mx-auto overflow-hidden">
			<Form {...chatForm}>
				<form onSubmit={chatForm.handleSubmit(handleSubmit)}>
					<FormField
						control={chatForm.control}
						name="content"
						render={({ field }) => (
							<FormItem>
								<div className="relative w-full overflow-hidden">
									<FormControl>
										<Textarea
											{...field}
											className="w-full min-h-[60px] max-h-[120px] resize-none break-words pr-12 py-4 text-base border-2 focus:border-primary/50 transition-colors overflow-y-auto"
											onKeyDown={handleKeyDown}
											placeholder="Ask anything... (Ctrl+Enter to send)"
										/>
									</FormControl>
									<Button
										className="absolute bottom-3 right-3 h-8 w-8 p-0 cursor-pointer"
										disabled={
											!chatForm.getValues("content").trim() ||
											chatMutation.isPending
										}
										size="sm"
										type="submit"
									>
										<Send className="h-4 w-4" />
									</Button>
								</div>
								<FormMessage />
							</FormItem>
						)}
					/>
				</form>
			</Form>
		</div>
	);
};

export default ChatForm;
