import type { RouteObject } from "react-router";
import RootLayout from "../components/layout/RootLayout";
import ErrorPage from "../pages/ErrorPage";
import HomePage from "../pages/HomePage";

export const routes: RouteObject[] = [
	{
		children: [
			{
				element: <HomePage />,
				index: true,
			},
		],
		element: <RootLayout />,
		errorElement: <ErrorPage />,
		path: "/",
	},
];
