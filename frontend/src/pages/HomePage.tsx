import ChatForm from "../components/features/chat/ChatForm/ChatForm";
import ChatHistory from "../components/features/chat/ChatHistory/ChatHistory";

const HomePage = () => {
	return (
		<div className="flex flex-col p-4 h-[calc(100vh-var(--header-height))] w-full overflow-hidden">
			<div className="flex-1 overflow-hidden min-h-0 w-full">
				<ChatHistory />
			</div>
			<div className="flex-shrink-0 w-full">
				<ChatForm />
			</div>
		</div>
	);
};

export default HomePage;
