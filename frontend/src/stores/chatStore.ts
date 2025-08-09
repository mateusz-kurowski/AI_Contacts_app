import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { Message } from "../components/ui/chat-message";

interface ChatStore {
	messages: Message[];
	isTyping: boolean;
	addMessage: (message: Message) => void;
	clearMessages: () => void;
	setIsTyping: (isTyping: boolean) => void;
}

export const useChatStore = create<ChatStore>()(
	persist(
		(set, get) => ({
			addMessage: (message: Message) =>
				set({
					messages: [...get().messages, message],
				}),
			clearMessages: () => set({ messages: [] }),
			isTyping: false,
			messages: [],
			setIsTyping: (isTyping: boolean) => set({ isTyping }),
		}),
		{
			name: "chat-storage",
			onRehydrateStorage: () => (state) => {
				if (state) {
					state.messages = state.messages.map((message) => ({
						...message,
						createdAt: message.createdAt
							? new Date(message.createdAt)
							: undefined,
					}));
				}
			},
			storage: createJSONStorage(() => sessionStorage),
		},
	),
);
