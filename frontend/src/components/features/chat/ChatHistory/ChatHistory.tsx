import { useChatStore } from "../../../../stores/chatStore";
import { MessageList } from "../../../ui/message-list";

const ChatHistory = () => {
	const { messages } = useChatStore();

	return (
		<div className="w-full overflow-y-auto">
			<MessageList messages={messages} />
		</div>
	);
};

export default ChatHistory;
