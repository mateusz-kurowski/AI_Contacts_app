import type { PropsWithChildren } from "react";
import { SidebarProvider } from "../ui/sidebar";
import { ThemeProvider } from "../ui/theme-provider";
import QueryProvider from "./QueryProvider";

const GlobalProviders = ({ children }: PropsWithChildren) => {
	return (
		<QueryProvider>
			<ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
				<SidebarProvider defaultOpen={false}>{children}</SidebarProvider>
			</ThemeProvider>
		</QueryProvider>
	);
};

export default GlobalProviders;
