"""Схемы адреса пользователя."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

# Обязательная строка адреса: обрезается по краям, непустая.
AddressField = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]
# Необязательная строка адреса (подъезд/этаж/квартира).
OptionalField = Annotated[
    str, StringConstraints(strip_whitespace=True, max_length=50)
]


class AddressBase(BaseModel):
    city: AddressField
    street: AddressField
    house: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
    ]
    entrance: OptionalField | None = None
    floor: OptionalField | None = None
    apartment: OptionalField | None = None
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    city: AddressField | None = None
    street: AddressField | None = None
    house: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
    ] | None = None
    entrance: OptionalField | None = None
    floor: OptionalField | None = None
    apartment: OptionalField | None = None
    is_default: bool | None = None


class AddressOut(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
