import type { PropsWithChildren } from "react";
import QueryProvider from "./QueryProvider";

const GlobalProviders = ({ children }: PropsWithChildren) => {
	return <QueryProvider>{children}</QueryProvider>;
};

export default GlobalProviders;
