import { useMutation } from "@tanstack/react-query";
import { useEffect, useRef } from "react";
import { getHelloMessage } from "@/queries/chat";
import { useChatStore } from "../../../../stores/chatStore";
import { MessageList } from "../../../ui/message-list";

const ChatHistory = () => {
	const { isTyping, messages, addMessage, setIsTyping } = useChatStore();
	const scrollContainerRef = useRef<HTMLDivElement>(null);
	const mutation = useMutation({
		mutationFn: getHelloMessage,
	});

	useEffect(() => {
		if (messages.length) return;

		let cancelled = false;

		(async () => {
			if (cancelled) return;

			try {
				setIsTyping(true);
				const helloMessage = await mutation.mutateAsync();
				if (!cancelled) {
					addMessage({
						...helloMessage,
						createdAt: new Date(helloMessage.createdAt),
					});
				}
			} catch (error) {
				if (!cancelled) {
					console.error("Failed to get hello message:", error);
					addMessage({
						content:
							"Hello! I'm your AI Contacts assistant. How can I help you today?",
						createdAt: new Date(),
						id: "welcome-fallback",
						role: "assistant",
					});
				}
			} finally {
				if (!cancelled) {
					setIsTyping(false);
				}
			}
		})();

		return () => {
			cancelled = true;
		};
	}, [messages.length, mutation.mutateAsync, addMessage, setIsTyping]);

	// biome-ignore lint/correctness/useExhaustiveDependencies: this is expected - scrolling is based on new message arrival
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
