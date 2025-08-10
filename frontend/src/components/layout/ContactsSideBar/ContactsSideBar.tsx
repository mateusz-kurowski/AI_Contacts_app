import { TooltipContent } from "@radix-ui/react-tooltip";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, ArrowRight, Plus } from "lucide-react";
import { useMemo, useState } from "react";
import ContactForm from "@/components/features/contacts/ContactForm/ContactForm";
import { ModeToggle } from "@/components/ui/mode-toggle";
import { getContacts } from "../../../queries/contacts";
import { Button } from "../../ui/button";
import { Dialog, DialogContent, DialogTrigger } from "../../ui/dialog";
import { Input } from "../../ui/input";
import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarGroup,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	useSidebar,
} from "../../ui/sidebar";
import { Tooltip, TooltipTrigger } from "../../ui/tooltip";
import SideBarContactIem from "../SideBarContactIem";

const ContactsSideBar = () => {
	const { toggleSidebar, open } = useSidebar();
	const [searchText, setSearchText] = useState("");

	const { data, error, isLoading } = useQuery({
		queryFn: getContacts,
		queryKey: ["contacts"],
	});

	// Filter contacts based on search text
	const filteredContacts = useMemo(() => {
		if (!data || !searchText.trim()) return data || [];

		return data.filter(
			(contact) =>
				contact.name?.toLowerCase().includes(searchText.toLowerCase()) ||
				contact.phone?.includes(searchText),
		);
	}, [data, searchText]);

	if (isLoading) return <p>Loading...</p>;
	if (error) return <p>Error: {error.message}</p>;
	if (!data) return <p>No data found</p>;

	return (
		<Sidebar collapsible="icon" side="right" variant="sidebar">
			<SidebarContent className="flex-1 min-h-0 overflow-y-auto">
				<Tooltip>
					<TooltipTrigger asChild>
						<Button
							className={`flex gap-1.5 ${open ? "" : "items-center"}`}
							onClick={toggleSidebar}
							size="sm"
							variant="ghost"
						>
							<ArrowLeft className="tooltip-collapsed-only h-4 w-4" />
							<ArrowRight className="tooltip-expanded-only h-4 w-4" />
							<span className="visible-sidebar-sr-only text-sm">
								Hide sidebar
							</span>
						</Button>
					</TooltipTrigger>
					<TooltipContent
						className="tooltip-custom tooltip-collapsed-only"
						side="left"
					>
						Expand sidebar
					</TooltipContent>
				</Tooltip>

				<SidebarHeader className="visible-sidebar-sr-only">
					<h2>Contacts</h2>
					<Input
						onChange={(e) => setSearchText(e.target.value)}
						placeholder="Find contact"
						value={searchText}
					/>
				</SidebarHeader>

				<SidebarGroup>
					<SidebarMenu className="gap-3">
						<SidebarMenuItem>
							<Dialog>
								<Tooltip>
									<TooltipTrigger asChild>
										<DialogTrigger asChild>
											<SidebarMenuButton>
												<Plus className="h-4 w-4" />
												<span className="visible-sidebar-sr-only">
													Add contact
												</span>
											</SidebarMenuButton>
										</DialogTrigger>
									</TooltipTrigger>
									<TooltipContent
										className="tooltip-custom tooltip-collapsed-only"
										side="left"
									>
										Add contact
									</TooltipContent>
								</Tooltip>
								<DialogContent>
									<ContactForm isInDialog />
								</DialogContent>
							</Dialog>
						</SidebarMenuItem>
						{filteredContacts.map((contact) => (
							<SideBarContactIem contact={contact} key={contact.id} />
						))}
					</SidebarMenu>
				</SidebarGroup>
			</SidebarContent>
			<SidebarFooter>
				<ModeToggle />
			</SidebarFooter>
		</Sidebar>
	);
};

export default ContactsSideBar;
