import * as libphonenumber from "google-libphonenumber";

export const phoneUtil = libphonenumber.PhoneNumberUtil.getInstance(); // Export phoneUtil

export const internationalFormat = (phoneNumber: string): string | null => {
	try {
		const number = phoneUtil.parseAndKeepRawInput(phoneNumber);
		return phoneUtil.format(
			number,
			libphonenumber.PhoneNumberFormat.INTERNATIONAL,
		);
	} catch {
		return null;
	}
};

export const validatePhoneNumber = (phoneString: string): boolean => {
	try {
		const number = phoneUtil.parseAndKeepRawInput(phoneString);
		return phoneUtil.isValidNumber(number);
	} catch {
		return false;
	}
};

export const getPhoneCountry = (phoneString: string): string | null => {
	try {
		const number = phoneUtil.parseAndKeepRawInput(phoneString);
		return phoneUtil.getRegionCodeForNumber(number) ?? null;
	} catch {
		return null;
	}
};

// Additional useful utility functions
export const nationalFormat = (phoneNumber: string): string | null => {
	try {
		const number = phoneUtil.parseAndKeepRawInput(phoneNumber);
		return phoneUtil.format(number, libphonenumber.PhoneNumberFormat.NATIONAL);
	} catch {
		return null;
	}
};

export const e164Format = (phoneNumber: string): string | null => {
	try {
		const number = phoneUtil.parseAndKeepRawInput(phoneNumber);
		return phoneUtil.format(number, libphonenumber.PhoneNumberFormat.E164);
	} catch {
		return null;
	}
};
