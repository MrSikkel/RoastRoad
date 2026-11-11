"""Схемы товара.

images/specifications объявлены как list/dict напрямую — никаких json.loads
и прочих «костылей» (JSON-тип в модели сериализует их сам).
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from .category import CategoryOut


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    short_description: str | None = None
    description: str | None = None
    price: Decimal = Field(gt=0)
    category_id: int = Field(gt=0)
    images: list[str] = Field(default_factory=list)
    specifications: dict[str, str] = Field(default_factory=dict)
    stock: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    """Все поля необязательны, ограничения сохраняются."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    short_description: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)
    images: list[str] | None = None
    specifications: dict[str, str] | None = None
    stock: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ProductDetailOut(ProductOut):
    """Сводный ответ для страницы товара: добавляет вложенную категорию."""

    category: CategoryOut | None = None
