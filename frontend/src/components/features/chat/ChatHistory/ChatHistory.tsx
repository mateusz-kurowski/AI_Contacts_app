import { useQuery } from "@tanstack/react-query";
import { useEffect, useRef } from "react";
import { getHelloMessage } from "@/queries/chat";
import { useChatStore } from "../../../../stores/chatStore";
import { MessageList } from "../../../ui/message-list";

const ChatHistory = () => {
	const { isTyping, messages, addMessage, setIsTyping } = useChatStore();
	const scrollContainerRef = useRef<HTMLDivElement>(null);

	const areMessagesEmpty = !messages.length;

	const {
		data: helloMessage,
		error,
		isLoading,
	} = useQuery({
		enabled: areMessagesEmpty,
		queryFn: getHelloMessage,
		queryKey: ["helloMessage"],
		retry: 1,
	});

	useEffect(() => {
		if (areMessagesEmpty) {
			setIsTyping(isLoading);
		}
	}, [isLoading, setIsTyping, areMessagesEmpty]);

	useEffect(() => {
		if (helloMessage && areMessagesEmpty) {
			addMessage({
				...helloMessage,
				createdAt: new Date(helloMessage.createdAt),
			});
		}
	}, [helloMessage, areMessagesEmpty, addMessage]);

	useEffect(() => {
		if (error && areMessagesEmpty) {
			addMessage({
				content:
					"Hello! I'm your AI Contacts assistant. How can I help you today?",
				createdAt: new Date(),
				id: "welcome-fallback",
				role: "assistant",
			});
		}
	}, [areMessagesEmpty, addMessage, error]);

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
		<div className="w-full h-full overflow-y-auto p-1" ref={scrollContainerRef}>
			<MessageList
				isTyping={isTyping}
				messageOptions={{ animation: "fade" }}
				messages={messages}
			/>
		</div>
	);
};

export default ChatHistory;
