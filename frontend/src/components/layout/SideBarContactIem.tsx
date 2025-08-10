import { TooltipContent, TooltipTrigger } from "@radix-ui/react-tooltip";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Pen, X } from "lucide-react";
import { toast } from "sonner";
import { addContact, deleteContact } from "../../queries/contacts";
import type { Contact } from "../../types/contact";
import ContactForm from "../features/contacts/ContactForm/ContactForm";
import { Dialog, DialogContent, DialogTrigger } from "../ui/dialog";
import {
	SidebarMenuAction,
	SidebarMenuButton,
	SidebarMenuItem,
} from "../ui/sidebar";
import { Tooltip } from "../ui/tooltip";

interface ContactProps {
	contact: Contact;
}

const getInitials = (name: string) => {
	return name
		.split(" ")
		.map((word) => word[0])
		.join("")
		.toUpperCase()
		.slice(0, 2);
};

const SideBarContactIem = ({ contact }: ContactProps) => {
	const handleDelete = async () => {
		await deleteContactMutation.mutateAsync(contact.id);
	};

	const restoreContactMutation = useMutation({
		mutationFn: addContact,
		onSuccess() {
			queryClient.invalidateQueries({ queryKey: ["contacts"] });
		},
	});

	const deleteContactMutation = useMutation({
		mutationFn: deleteContact,
		mutationKey: ["deleteContact", contact.id],
		onError() {
			toast("Error deleting contact", {
				action: {
					label: "Retry",
					onClick: () => deleteContactMutation.mutate(contact.id),
				},
			});
		},
		onSuccess() {
			queryClient.invalidateQueries({ queryKey: ["contacts"] });
			toast("Successfully deleted contact", {
				action: {
					label: "Undo",
					onClick: () => {
						restoreContactMutation.mutate({
							name: contact.name,
							phone: contact.phone,
						});
						toast("Successfully restored contact");
					},
				},
			});
		},
	});

	const queryClient = useQueryClient();

	return (
		<Tooltip>
			<TooltipTrigger>
				<SidebarMenuItem>
					<SidebarMenuButton asChild>
						<span>
							<div className="h-5 w-5 bg-gray-300 rounded-full flex items-center justify-center text-xs font-medium p-3">
								{getInitials(contact.name)}
							</div>
							<span>
								<div>{contact.name}</div>
								<div>{contact.phone}</div>
							</span>
						</span>
					</SidebarMenuButton>
					<SidebarMenuAction>
						<Dialog>
							<DialogTrigger asChild>
								<Pen className="hover:cursor-pointer" />
							</DialogTrigger>
							<DialogContent>
								<ContactForm contact={contact} />
							</DialogContent>
							<X
								className="hover:cursor-pointer hover:text-red-600"
								onClick={handleDelete}
							/>
						</Dialog>
					</SidebarMenuAction>
				</SidebarMenuItem>
			</TooltipTrigger>
			<TooltipContent
				className="tooltip-collapsed-only tooltip-custom"
				side="left"
			>
				<p>{contact.name}</p>
				<p>{contact.phone}</p>
			</TooltipContent>
		</Tooltip>
	);
};

export default SideBarContactIem;
