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
import { PhoneNumberFormat } from "google-libphonenumber";
import { PhoneInput } from "react-international-phone";
import { addContact } from "@/queries/contacts";
import { phoneUtil, validatePhoneNumber } from "./validators";

export const contactFormSchema = z.object({
	name: z.string().min(1, "Name is required"),
	phone: z
		.string()
		.min(1, "Phone number is required")
		.refine(validatePhoneNumber, "Please enter a valid phone number"),
});

type ContactFormSchema = z.infer<typeof contactFormSchema>;

const contactFormDefaultValues: ContactFormSchema = {
	name: "",
	phone: "",
};

const contactFormResolver = zodResolver(contactFormSchema);

const ContactForm = () => {
	const form = useForm<ContactFormSchema>({
		defaultValues: contactFormDefaultValues,
		resolver: contactFormResolver,
	});

	const mutation = useMutation({
		mutationFn: addContact,
		mutationKey: ["addContact"],
	});
	const queryClient = useQueryClient();
	const onSubmit = async (data: ContactFormSchema) => {
		console.log("Form submitted with data:", data);

		try {
			const phoneNumber = phoneUtil.parseAndKeepRawInput(data.phone);
			const country = phoneUtil.getRegionCodeForNumber(phoneNumber);
			const numberType = phoneUtil.getNumberType(phoneNumber);

			// Fixed format usage
			const internationalFormat = phoneUtil.format(
				phoneNumber,
				PhoneNumberFormat.INTERNATIONAL,
			);
			const nationalFormat = phoneUtil.format(
				phoneNumber,
				PhoneNumberFormat.NATIONAL,
			);

			console.log("Country:", country);
			console.log("Number type:", numberType);
			console.log("International format:", internationalFormat);
			console.log("National format:", nationalFormat);

			await mutation.mutateAsync({
				name: data.name,
				phone: internationalFormat,
			});
			queryClient.invalidateQueries({ queryKey: ["contacts"] });
		} catch (error) {
			console.log("Could not parse phone number:", error);
		}
	};

	return (
		<Form {...form}>
			<form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
				<FormField
					control={form.control}
					name="name"
					render={({ field }) => (
						<FormItem>
							<FormLabel htmlFor="name">Name</FormLabel>
							<FormControl>
								<Input placeholder="Name" {...field} />
							</FormControl>
							<FormDescription>Contact name</FormDescription>
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
									defaultCountry="pl"
									inputProps={{
										className:
											"flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
									}}
									onChange={field.onChange}
									placeholder="Enter phone number"
									preferredCountries={["pl", "us", "gb", "ps"]}
									value={field.value}
								/>
							</FormControl>
							<FormDescription>
								Enter your phone number with country code
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<Button type="submit">Submit</Button>
			</form>
		</Form>
	);
};

export default ContactForm;
