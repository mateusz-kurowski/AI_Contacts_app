import { Outlet } from "react-router";
import { StarsBackground } from "../animate-ui/backgrounds/stars";
import { Toaster } from "../ui/sonner";
import { useTheme } from "../ui/theme-provider";
import ContactsSideBar from "./ContactsSideBar/ContactsSideBar";
import Header from "./Header";
export default function RootLayout() {
	const { theme } = useTheme();
	const background =
		theme === "light"
			? "radial-gradient(125% 125% at 50% 90%, #fff 40%, #6366f1 100%)"
			: "radial-gradient(125% 125% at 50% 100%, #000000 40%, #010133 100%)";

	return (
		<div className="min-h-screen w-full relative">
			<StarsBackground
				className="absolute inset-0 z-0"
				style={{ background }}
			/>

			<div className="min-h-screen w-full flex flex-col relative">
				<div className="flex-1 flex overflow-hidden">
					<div className="flex-1 flex flex-col min-w-0">
						<Header />
						<main className="flex-1 overflow-hidden w-full min-w-0">
							<Outlet />
						</main>
					</div>
					<ContactsSideBar />
				</div>
				<Toaster />
			</div>
		</div>
	);
}
