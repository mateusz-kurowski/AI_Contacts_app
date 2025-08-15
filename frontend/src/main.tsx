import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router";
import GlobalProviders from "./components/providers/GlobalProviders";
import { routes } from "./routes";
import "./index.css";
const router = createBrowserRouter(routes);

// biome-ignore lint/style/noNonNullAssertion: we know root exists
ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<GlobalProviders>
			<RouterProvider router={router} />
		</GlobalProviders>
	</React.StrictMode>,
);
