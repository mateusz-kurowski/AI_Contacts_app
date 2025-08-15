import { Pen } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog";
import { SidebarMenuAction } from "@/components/ui/sidebar";
import type { Contact } from "@/types/contact";
import ContactForm from "./ContactForm";

interface EditContactDialogProps {
	contact: Contact;
	isAction?: boolean;
}

const EditContactDialog = ({ contact, isAction }: EditContactDialogProps) => {
	const penIcon = <Pen className="h-3 w-3" />;
	const textColour = "text-blue-600";
	return (
		<Dialog>
			<DialogTrigger asChild>
				{isAction ? (
					<SidebarMenuAction
						className={`group-data-[collapsible=icon]:hidden mr-6 cursor-pointer hover:${textColour}`}
						showOnHover
					>
						{penIcon}
					</SidebarMenuAction>
				) : (
					<Button
						className={`h-3 w-3 cursor-pointer hover:${textColour}`}
						variant="ghost"
					>
						{penIcon}
					</Button>
				)}
			</DialogTrigger>
			<DialogContent>
				<DialogTitle>Edit Contact</DialogTitle>
				<ContactForm contact={contact} isInDialog />
			</DialogContent>
		</Dialog>
	);
};

export default EditContactDialog;
