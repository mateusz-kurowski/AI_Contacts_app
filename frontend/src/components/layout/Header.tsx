import { BookUser } from "lucide-react";
import { Link } from "react-router";

const Header = () => {
	return (
		<header
			className="h-16 flex items-center justify-between w-full px-6 bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50"
			style={{ "--header-height": "4rem" } as React.CSSProperties}
		>
			<Link to="/">
				<div className="flex items-center gap-3">
					<BookUser className="h-6 w-6 text-blue-600" />
					<h1 className="text-xl font-semibold text-gray-900">Contacts</h1>
				</div>
			</Link>
		</header>
	);
};

export default Header;
