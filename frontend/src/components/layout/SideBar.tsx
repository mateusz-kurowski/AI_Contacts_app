import { useQuery } from "@tanstack/react-query";

const SideBar = () => {
	const { data, error, isLoading } = useQuery({
		queryFn: () =>
			fetch(`${import.meta.env.VITE_API_URL}/contacts`).then((res) =>
				res.json(),
			),
		queryKey: ["contacts"],
	});

	if (isLoading) return <p>Loading...</p>;
	if (error) return <p>Error: {error.message}</p>;
	if (!data) return <p>No data found</p>;

	return (
		<div>
			<h2>Contacts</h2>
			{data && (
				<ul>
					{data.map((contact) => (
						<li key={contact.id}>{contact.name}</li>
					))}
				</ul>
			)}
		</div>
	);
};

export default SideBar;
