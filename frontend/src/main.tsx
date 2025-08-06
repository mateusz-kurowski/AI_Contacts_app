import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App";

// biome-ignore lint/style/noNonNullAssertion: we know root exists
ReactDOM.createRoot(document.getElementById("root")!).render(
	<BrowserRouter>
		<App />
	</BrowserRouter>,
);
