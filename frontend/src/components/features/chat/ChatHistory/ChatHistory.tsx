import { useChatStore } from "../../../../stores/chatStore";
import { MessageList } from "../../../ui/message-list";

const ChatHistory = () => {
	const { messages } = useChatStore();

	return (
		<div className="w-full h-full overflow-y-auto p-2">
			<MessageList messages={messages} />
		</div>
	);
};

export default ChatHistory;
