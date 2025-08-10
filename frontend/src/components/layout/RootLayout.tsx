import { Outlet } from "react-router";
import { Toaster } from "../ui/sonner";
import ContactsSideBar from "./ContactsSideBar/ContactsSideBar";
import Header from "./Header";

export default function RootLayout() {
	return (
		<div className="min-h-screen w-full flex flex-col">
			<div className="flex-1 flex overflow-hidden">
				<div className="flex-1 flex flex-col">
					<Header />
					<main className="flex-1 overflow-hidden">
						<Outlet />
					</main>
				</div>
				<ContactsSideBar />
			</div>
			<Toaster />
		</div>
	);
}
