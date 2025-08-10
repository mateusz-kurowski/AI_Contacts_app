import { BookUser, Trash2 } from "lucide-react";
import { Link } from "react-router";
import { useChatStore } from "@/stores/chatStore";
import { Button } from "../ui/button";

const Header = () => {
	const { clearMessages } = useChatStore();

	return (
		<header className="h-16 flex items-center justify-between w-full px-6 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border/40 shadow-sm sticky top-0 z-50">
			<Link
				className="flex items-center gap-3 group transition-all duration-200 hover:scale-105"
				to="/"
			>
				<div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 shadow-lg group-hover:shadow-xl transition-all duration-200">
					<BookUser className="h-5 w-5 text-white" />
				</div>
				<h1 className="text-xl font-semibold text-foreground group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-200">
					AI Contacts
				</h1>
			</Link>

			<div className="flex items-center gap-2">
				<Button
					className="text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all duration-200 hover:scale-105 border-border/50"
					onClick={clearMessages}
					size="icon"
					title="Clear chat history"
					variant="outline"
				>
					<Trash2 className="h-4 w-4" />
				</Button>
			</div>
		</header>
	);
};

export default Header;
