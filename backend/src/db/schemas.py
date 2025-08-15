from typing import Literal

from pydantic import BaseModel, Field, constr
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from typing import Annotated


# Phone number in E.164 format (almost raw)
PhoneE164 = Annotated[str, PhoneNumberValidator(number_format="E164")]


# Pydantic schemas
class ContactBase(BaseModel):
    name: constr(min_length=1)  # type: ignore
    phone: PhoneE164


class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    content: str
    id: str
    role: Literal["user", "assistant"]
    createdAt: str


class NewChatMessage(BaseModel):
    content: str = Field(
        ...,
        min_length=2,
        max_length=400,
        strip_whitespace=True,
        examples=["Hello, how can I help you?"],
        description="The content of the chat message, must be between 2 and 400 characters long.",
    )
