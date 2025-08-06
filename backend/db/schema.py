from pydantic import BaseModel, constr


# Pydantic schemas
class ContactBase(BaseModel):
    name: constr(min_length=1)  # type: ignore
    phone: constr(min_length=1)  # type: ignore


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True
