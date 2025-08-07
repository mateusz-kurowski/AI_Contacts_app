import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import App from "./App";

// biome-ignore lint/style/noNonNullAssertion: we know root exists
ReactDOM.createRoot(document.getElementById("root")!).render(
	<BrowserRouter>
		<Routes>
			<Route element={<App />} path="/" />
		</Routes>
	</BrowserRouter>,
);
