import { useQuery } from "@tanstack/react-query";
import { useEffect, useRef } from "react";
import { getHelloMessage } from "@/queries/chat";
import { useChatStore } from "../../../../stores/chatStore";
import { MessageList } from "../../../ui/message-list";

const ChatHistory = () => {
	const { isTyping, messages, addMessage, setIsTyping } = useChatStore();
	const scrollContainerRef = useRef<HTMLDivElement>(null);

	const {
		data: helloMessage,
		error,
		isLoading,
	} = useQuery({
		enabled: messages.length === 0, // Only fetch when no messages exist
		queryFn: getHelloMessage,
		queryKey: ["helloMessage"],
		retry: 1,
	});

	useEffect(() => {
		setIsTyping(isLoading);
	}, [isLoading, setIsTyping]);

	useEffect(() => {
		if (helloMessage && messages.length === 0) {
			addMessage({
				...helloMessage,
				createdAt: new Date(helloMessage.createdAt),
			});
		}
	}, [helloMessage, messages.length, addMessage]);

	useEffect(() => {
		if (error && messages.length === 0) {
			console.error("Failed to get hello message:", error);
			addMessage({
				content:
					"Hello! I'm your AI Contacts assistant. How can I help you today?",
				createdAt: new Date(),
				id: "welcome-fallback",
				role: "assistant",
			});
		}
	}, [error, messages.length, addMessage]);

	// Auto-scroll effect
	// biome-ignore lint/correctness/useExhaustiveDependencies: scrolling is based on new message arrival
	useEffect(() => {
		if (scrollContainerRef.current) {
			scrollContainerRef.current.scrollTo({
				behavior: "smooth",
				top: scrollContainerRef.current.scrollHeight,
			});
		}
	}, [messages]);

	return (
		<div className="w-full h-full overflow-y-auto p-2" ref={scrollContainerRef}>
			<MessageList isTyping={isTyping} messages={messages} />
		</div>
	);
};

export default ChatHistory;
