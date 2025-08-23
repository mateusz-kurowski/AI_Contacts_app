import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat


def format_phone_number(phone: str, default_region: str = "PL") -> str | None:
    """
    Format phone number to E.164.
    Returns None if invalid or cannot be parsed.
    """
    try:
        stripped_phone = phone.strip()
        num = phonenumbers.parse(stripped_phone, default_region)
        if not phonenumbers.is_valid_number(num):
            return None
        return phonenumbers.format_number(num, PhoneNumberFormat.E164)
    except NumberParseException:
        return None
