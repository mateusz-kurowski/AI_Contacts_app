const createHash = (name: string) =>
	name.split("").reduce((acc, char) => acc + char.charCodeAt(0), 0);

export const getContactColor = (name: string) => {
	const hash = createHash(name);

	const avatarColors = [
		"bg-blue-500 text-white dark:bg-blue-600",
		"bg-green-500 text-white dark:bg-green-600",
		"bg-purple-500 text-white dark:bg-purple-600",
		"bg-pink-500 text-white dark:bg-pink-600",
		"bg-indigo-500 text-white dark:bg-indigo-600",
		"bg-red-500 text-white dark:bg-red-600",
		"bg-yellow-500 text-black dark:bg-yellow-600 dark:text-white",
		"bg-teal-500 text-white dark:bg-teal-600",
		"bg-orange-500 text-white dark:bg-orange-600",
		"bg-cyan-500 text-white dark:bg-cyan-600",
		"bg-rose-500 text-white dark:bg-rose-600",
		"bg-emerald-500 text-white dark:bg-emerald-600",
	];

	return avatarColors[hash % avatarColors.length];
};

export const getInitials = (name: string) =>
	name
		.split(" ")
		.map(([first]) => first)
		.join("")
		.toUpperCase()
		.slice(0, 2);
