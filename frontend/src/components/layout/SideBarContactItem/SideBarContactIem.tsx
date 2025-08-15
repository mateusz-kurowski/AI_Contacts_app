import { TooltipContent, TooltipTrigger } from "@radix-ui/react-tooltip";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Pen, X } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import ContactForm from "@/components/features/contacts/ContactForm";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import { addContact, deleteContact } from "../../../queries/contacts";
import type { Contact } from "../../../types/contact";
import {
	SidebarMenuAction,
	SidebarMenuButton,
	SidebarMenuItem,
} from "../../ui/sidebar";
import { Tooltip } from "../../ui/tooltip";
import { getContactColor, getInitials } from "./data";

interface ContactProps {
	contact: Contact;
}

const SideBarContactItem = ({ contact }: ContactProps) => {
	const [isOpen, setIsOpen] = useState(false);
	const queryClient = useQueryClient();

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

	const openDialog = () => {
		setIsOpen(true);
	};

	return (
		<>
			<Tooltip>
				<TooltipTrigger asChild>
					<SidebarMenuItem>
						<SidebarMenuButton
							asChild
							className="flex group-data-[collapsible=icon]:justify-center"
						>
							<span className="ml-1 flex items-center gap-3 group-data-[collapsible=icon]:ml-0">
								<div
									className={`h-5 w-5 rounded-full font-medium flex items-center justify-center text-xs p-3 ${getContactColor(
										contact.name,
									)}`}
								>
									{getInitials(contact.name)}
								</div>

								<span className="flex flex-col gap-0.5 min-w-0 flex-1 group-data-[collapsible=icon]:hidden">
									<div className="text-sm font-medium text-foreground truncate">
										{contact.name}
									</div>
									<div className="text-xs text-muted-foreground truncate">
										{contact.phone}
									</div>
								</span>
							</span>
						</SidebarMenuButton>
						<SidebarMenuAction
							className="group-data-[collapsible=icon]:hidden cursor-pointer text-blue-600 mr-6"
							onClick={openDialog}
						>
							<Pen className="h-3 w-3" />
						</SidebarMenuAction>
						<SidebarMenuAction
							className="group-data-[collapsible=icon]:hidden cursor-pointer text-red-600"
							onClick={handleDelete}
							showOnHover
						>
							<X className="h-3 w-3" />
						</SidebarMenuAction>
					</SidebarMenuItem>
				</TooltipTrigger>
				<TooltipContent
					className="tooltip-collapsed-only tooltip-custom flex gap-1"
					side="left"
				>
					<div>
						<p>{contact.name}</p>
						<p className="text-muted-foreground">{contact.phone}</p>
					</div>
					<div className="flex flex-col items-center gap-2">
						<Button
							className="h-3 w-3 cursor-pointer text-blue-600"
							onClick={openDialog}
							variant="ghost"
						>
							<Pen className="h-3 w-3" />
						</Button>
						<Button
							className="h-3 w-3 cursor-pointer text-red-600"
							onClick={handleDelete}
							variant="ghost"
						>
							<X />
						</Button>
					</div>
				</TooltipContent>
			</Tooltip>
			<Dialog onOpenChange={setIsOpen} open={isOpen}>
				<DialogContent>
					<DialogTitle>Edit Contact</DialogTitle>
					<ContactForm contact={contact} isInDialog />
				</DialogContent>
			</Dialog>
		</>
	);
};

export default SideBarContactItem;
