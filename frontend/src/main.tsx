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
			<div className="min-h-screen w-full relative">
				<div
					className="absolute inset-0 z-0"
					style={{
						background:
							"radial-gradient(125% 125% at 50% 100%, #000000 40%, #010133 100%)",
					}}
				/>
				<RouterProvider router={router} />
			</div>
		</GlobalProviders>
	</React.StrictMode>,
);
