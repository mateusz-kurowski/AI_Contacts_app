import ChatForm from "../components/features/chat/ChatForm/ChatForm";
import ChatHistory from "../components/features/chat/ChatHistory/ChatHistory";

const HomePage = () => {
	return (
		<div className="flex flex-col p-4 h-[calc(100vh-var(--header-height))]">
			<div className="flex-1 overflow-hidden min-h-0">
				<ChatHistory />
			</div>
			<div className="flex-shrink-0">
				<ChatForm />
			</div>
		</div>
	);
};

export default HomePage;
