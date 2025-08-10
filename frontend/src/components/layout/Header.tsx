import { BookUser, Trash2 } from "lucide-react";
import { Link } from "react-router";
import { useChatStore } from "@/stores/chatStore";
import { Button } from "../ui/button";

const Header = () => {
	const { clearMessages } = useChatStore();
	return (
		<header className="h-16 flex items-center justify-between w-full px-6 bg-white border-b border-gray-200 shadow-sm ">
			<Link to="/">
				<div className="flex items-center gap-3">
					<BookUser className="h-6 w-6 text-blue-600" />
					<h1 className="text-xl font-semibold text-gray-900">Contacts</h1>
				</div>
			</Link>
			<Button
				className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors"
				onClick={clearMessages}
				title="Clear chat history"
				variant="outline"
			>
				<Trash2 className="h-5 w-5" />
			</Button>
		</header>
	);
};

export default Header;
