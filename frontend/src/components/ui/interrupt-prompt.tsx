"use client";

import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";

interface InterruptPromptProps {
	isOpen: boolean;
	close: () => void;
}

export function InterruptPrompt({ isOpen, close }: InterruptPromptProps) {
	return (
		<AnimatePresence>
			{isOpen && (
				<motion.div
					animate={{
						filter: "blur(0px)",
						top: -40,
						transition: {
							filter: { type: "tween" },
							type: "spring",
						},
					}}
					className="absolute left-1/2 flex -translate-x-1/2 overflow-hidden whitespace-nowrap rounded-full border bg-background py-1 text-center text-sm text-muted-foreground"
					exit={{ filter: "blur(5px)", top: 0 }}
					initial={{ filter: "blur(5px)", top: 0 }}
				>
					<span className="ml-2.5">Press Enter again to interrupt</span>
					<button
						aria-label="Close"
						className="ml-1 mr-2.5 flex items-center"
						onClick={close}
						type="button"
					>
						<X className="h-3 w-3" />
					</button>
				</motion.div>
			)}
		</AnimatePresence>
	);
}
