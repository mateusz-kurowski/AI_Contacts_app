import { BookUser, Trash2 } from "lucide-react";
import { Link } from "react-router";
import { useChatStore } from "@/stores/chatStore";
import { Button } from "../ui/button";

const Header = () => {
	const { clearMessages } = useChatStore();
	return (
		<header className="h-16 flex items-center justify-between w-full px-6 bg-background border-b border-border shadow-sm">
			<Link to="/">
				<div className="flex items-center gap-3">
					<BookUser className="h-6 w-6 text-blue-600 dark:text-blue-400" />
					<h1 className="text-xl font-semibold text-foreground">AI Contacts</h1>
				</div>
			</Link>
			<Button
				className="text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
				onClick={clearMessages}
				size="icon"
				title="Clear chat history"
				variant="outline"
			>
				<Trash2 className="h-5 w-5" />
			</Button>
		</header>
	);
};

export default Header;
