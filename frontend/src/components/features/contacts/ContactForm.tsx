import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import "react-international-phone/style.css";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { DialogClose, DialogFooter } from "@/components/ui/dialog";
import { PhoneInput } from "@/components/ui/phone-input";
import { addContact, updateContact } from "@/queries/contacts";
import type { Contact } from "@/types/contact";

export const contactFormSchema = z.object({
	name: z
		.string()
		.min(1, "Name is required")
		.min(2, "Name must be at least 2 characters")
		.max(100, "Name must be less than 100 characters")
		.regex(
			/^[a-zA-Z\s'-]+$/,
			"Name can only contain letters, spaces, hyphens and apostrophes",
		),
	phone: z
		.string()
		.min(1, "Phone number is required")
		.min(5, "Phone number is too short"),
});

type ContactFormSchema = z.infer<typeof contactFormSchema>;

const contactFormResolver = zodResolver(contactFormSchema);

interface ContactFormProps {
	isInDialog?: boolean;
	contact?: Contact;
}

const ContactForm = ({ isInDialog, contact }: ContactFormProps) => {
	const contactFormDefaultValues: ContactFormSchema = {
		name: contact?.name ?? "",
		phone: contact?.phone ?? "",
	};

	// Determine if this is edit mode
	const isEditing = !!contact;

	const form = useForm<ContactFormSchema>({
		defaultValues: contactFormDefaultValues,
		mode: "onBlur",
		resolver: contactFormResolver,
	});

	const addMutation = useMutation({
		mutationFn: addContact,
		mutationKey: ["addContact"],
	});

	const editMutation = useMutation({
		mutationFn: updateContact,
		mutationKey: ["editContact", contact?.id],
	});

	const queryClient = useQueryClient();

	const onSubmit = async (data: ContactFormSchema) => {
		try {
			if (isEditing && contact) {
				// Update existing contact
				await editMutation.mutateAsync({
					id: contact.id,
					name: data.name.trim(),
					phone: data.phone,
				});
			} else {
				// Add new contact
				await addMutation.mutateAsync({
					name: data.name.trim(),
					phone: data.phone,
				});
			}

			queryClient.invalidateQueries({ queryKey: ["contacts"] });
			form.reset();
		} catch (error) {
			console.error(
				`Error ${isEditing ? "updating" : "adding"} contact:`,
				error,
			);
			form.setError("root", {
				message: `Failed to ${
					isEditing ? "update" : "add"
				} contact. Please try again.`,
				type: "manual",
			});
		}
	};

	// Determine which mutation is currently pending
	const isPending = isEditing ? editMutation.isPending : addMutation.isPending;

	const submitBtn = (
		<Button
			className="transition-all duration-200 cursor-pointer hover:bg-primary/70"
			disabled={isPending}
			type="submit"
		>
			{isEditing ? "Update Contact" : "Add Contact"}
		</Button>
	);

	return (
		<Form {...form}>
			<form className="space-y-6" onSubmit={form.handleSubmit(onSubmit)}>
				<FormField
					control={form.control}
					name="name"
					render={({ field }) => (
						<FormItem>
							<FormLabel htmlFor="name">Full Name</FormLabel>
							<FormControl>
								<Input
									placeholder="Enter full name"
									{...field}
									className="transition-all duration-200 focus:ring-2 focus:ring-primary/20"
								/>
							</FormControl>
							<FormDescription>Enter the contact's full name</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="phone"
					render={({ field }) => (
						<FormItem>
							<FormLabel htmlFor="phone">Phone Number</FormLabel>
							<FormControl>
								<PhoneInput
									countryCallingCodeEditable={true}
									defaultCountry="PL"
									international
									onChange={(value) => {
										field.onChange(value || "");
										if (form.formState.errors.phone) {
											form.clearErrors("phone");
										}
									}}
									placeholder="Enter phone number"
									value={field.value}
								/>
							</FormControl>
							<FormDescription>
								Include country code (e.g., +48 for Poland)
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				{form.formState.errors.root && (
					<div className="text-sm text-destructive">
						{form.formState.errors.root.message}
					</div>
				)}

				{isInDialog ? (
					<DialogFooter className="gap-2">
						<DialogClose asChild>
							<Button type="button" variant="outline">
								Cancel
							</Button>
						</DialogClose>
						{submitBtn}
					</DialogFooter>
				) : (
					submitBtn
				)}
			</form>
		</Form>
	);
};

export default ContactForm;
