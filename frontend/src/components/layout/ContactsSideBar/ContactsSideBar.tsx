import { TooltipContent } from "@radix-ui/react-tooltip";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, ArrowRight, Plus } from "lucide-react";
import ContactForm from "@/components/features/contacts/ContactForm/ContactForm";
import { getContacts } from "../../../queries/contacts";
import { Button } from "../../ui/button";
import { Dialog, DialogContent, DialogTrigger } from "../../ui/dialog";
import { Input } from "../../ui/input";
import {
	Sidebar,
	SidebarContent,
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

	const { data, error, isLoading } = useQuery({
		queryFn: getContacts,
		queryKey: ["contacts"],
	});

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
						Toggle sidebar
					</TooltipContent>
				</Tooltip>

				<SidebarHeader className="visible-sidebar-sr-only">
					<h2>Contacts</h2>
					<Input placeholder="Find contact" />
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
									<ContactForm />
								</DialogContent>
							</Dialog>
						</SidebarMenuItem>
						{data.contacts.map((contact) => (
							<SideBarContactIem contact={contact} key={contact.id} />
						))}
					</SidebarMenu>
				</SidebarGroup>
			</SidebarContent>
		</Sidebar>
	);
};

export default ContactsSideBar;
