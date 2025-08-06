import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";

export default defineConfig({
	build: {
		rollupOptions: {
			// Force Rollup to use WASM instead of native binaries
		},
	},
	plugins: [react()],
	// Override Rollup resolution to use WASM
	resolve: {
		alias: {
			rollup: "@rollup/wasm-node",
		},
	},
});
