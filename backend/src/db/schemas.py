import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, constr
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

PhoneE164 = Annotated[str, PhoneNumberValidator(number_format="E164")]
phone_e164_regex = re.compile(r"^\+[1-9]\d{1,14}$")

class ContactBase(BaseModel):
    name: constr(min_length=1, max_length=50)  # type: ignore
    phone: PhoneE164


class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass


class Contact(ContactBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ChatResponse(BaseModel):
    content: str
    id: str
    role: Literal["user", "assistant"]
    createdAt: str


class NewChatMessage(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    content: str = Field(
        min_length=2,
        max_length=400,
        examples=["Hello, how can I help you?"],
        description="The content of the chat message, must be between 2 and 400 characters long.",
    )
