import { useEffect, useRef } from "react";
import { useChatStore } from "../../../../stores/chatStore";
import { MessageList } from "../../../ui/message-list";

const ChatHistory = () => {
	const { messages } = useChatStore();
	const scrollContainerRef = useRef<HTMLDivElement>(null);

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
			<MessageList messages={messages} />
		</div>
	);
};

export default ChatHistory;
