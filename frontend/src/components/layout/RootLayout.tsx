import { Outlet } from "react-router";
import { Toaster } from "../ui/sonner";
import ContactsSideBar from "./ContactsSideBar/ContactsSideBar";
import Header from "./Header";

export default function RootLayout() {
	return (
		<div className="min-h-screen w-full flex flex-col">
			<Header />
			<div className="flex-1 flex overflow-hidden">
				<main className="flex-1 container mx-auto px-4 py-4 overflow-auto">
					<Outlet />
				</main>
				<ContactsSideBar />
			</div>
			<Toaster />
		</div>
	);
}
