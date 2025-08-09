import type { PropsWithChildren } from "react";
import { SidebarProvider } from "../ui/sidebar";
import QueryProvider from "./QueryProvider";

const GlobalProviders = ({ children }: PropsWithChildren) => {
	return (
		<QueryProvider>
			<SidebarProvider defaultOpen={false}>{children}</SidebarProvider>
		</QueryProvider>
	);
};

export default GlobalProviders;
