import ChatForm from "../components/features/chat/ChatForm/ChatForm";
import ChatHistory from "../components/features/chat/ChatHistory/ChatHistory";

const HomePage = () => {
	return (
		<div className="flex flex-col gap-2 items-center h-full">
			<ChatHistory />
			<ChatForm />
		</div>
	);
};

export default HomePage;
