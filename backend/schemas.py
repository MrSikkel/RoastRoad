from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
import re
from decimal import Decimal
from pydantic import field_validator, model_validator
from typing import TYPE_CHECKING, Union, Any
import json

if TYPE_CHECKING:
    from models import Product, Article


class Role(str, Enum):
    user = "user"
    admin = "admin"

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    last_name: Optional[str] = Field(None, min_length=1, max_length=43, strip_whitespace=True)
    first_name: Optional[str] = Field(None, min_length=1, max_length=30, strip_whitespace=True)
    patronymic: Optional[str] = Field(None, max_length=30, strip_whitespace=True)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not any(char.isalpha() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v and not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError('Номер телефона должен быть в международном формате')
        return v

    @field_validator('first_name', 'last_name', 'patronymic')
    @classmethod
    def validate_name_chars(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v and not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', v):
            raise ValueError('Имя может содержать только буквы, пробелы и дефисы')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)

class ChangePassword(BaseModel):
    current_password: str = Field(min_length=6, max_length=40)
    new_password: str = Field(min_length=6, max_length=40)

    @field_validator('new_password')
    @classmethod
    def validate_new_password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Новый пароль должен содержать хотя бы одну цифру')
        if not any(char.isalpha() for char in v):
            raise ValueError('Новый пароль должен содержать хотя бы одну букву')
        return v
    
class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr
    last_name: str = Field(min_length=1, max_length=43, strip_whitespace=True)
    first_name: str = Field(min_length=1, max_length=30, strip_whitespace=True)
    patronymic: Optional[str] = Field(None, max_length=30, strip_whitespace=True)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)

    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError('Номер телефона должен быть в международном формате')
        return v

    @field_validator('first_name', 'last_name', 'patronymic')
    @classmethod
    def validate_name_chars(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', v):
            raise ValueError('Имя может содержать только буквы, пробелы и дефисы')
        return v
"""
# Схема для создания пользователя
class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=40)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not any(char.isalpha() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        return v
"""
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    last_name: Optional[str] = Field(None, min_length=1, max_length=43, strip_whitespace=True)
    first_name: Optional[str] = Field(None, min_length=1, max_length=30, strip_whitespace=True)
    patronymic: Optional[str] = Field(None, max_length=30, strip_whitespace=True)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)

    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError('Номер телефона должен быть в международном формате')
        return v

    @field_validator('first_name', 'last_name', 'patronymic')
    @classmethod
    def validate_name_chars(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', v):
            raise ValueError('Имя может содержать только буквы, пробелы и дефисы')
        return v

class User(UserBase):
    id: int = Field(gt=0)
    role: Role
    registration_date: datetime

    class Config:
        from_attributes = True

class UserProfile(User):
    addresses: List['UserAddress'] = []
    #orders_count: int = Field(ge=0, default=0)
    #reviews_count: int = Field(ge=0, default=0)

class UserAddressBase(BaseModel):
    country: str = Field(min_length=2, max_length=63, strip_whitespace=True)
    city: str = Field(min_length=1, max_length=179, strip_whitespace=True)
    street: str = Field(min_length=2, max_length=58, strip_whitespace=True)
    house_number: str = Field(min_length=1, max_length=20, strip_whitespace=True)
    entrance: Optional[int] = Field(None, ge=1, le=120)
    is_current: bool = True

    @field_validator('country', 'city', 'street')
    @classmethod
    def validate_address_chars(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9\s\-\.,]+$', v):
            raise ValueError('Поля адреса могут содержать только буквы, цифры, пробелы, дефисы и запятые')
        return v

    @field_validator('house_number')
    @classmethod
    def validate_house_number(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9/\-\s]+$', v):
            raise ValueError('Номер дома может содержать только буквы, цифры, пробелы, дефисы и слэши')
        return v

class UserAddressCreate(UserAddressBase):
    pass

class UserAddress(UserAddressBase):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(gt=0)
    category_id: Optional[int] = Field(None, gt=0)
    images: Optional[List[str]] = Field(default_factory=list)
    specifications: Optional[Union[dict, str]] = Field(default_factory=dict)
    
    @field_validator('specifications', mode='before')
    @classmethod
    def parse_specifications(cls, v):
        if v is None:
            return {}
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v) if v else {}
            except json.JSONDecodeError:
                return {}
        return {}
    
    @field_validator('images', mode='before')
    @classmethod
    def parse_images(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v) if v else []
            except json.JSONDecodeError:
                return []
        return []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[Decimal] = None

class ProductOut(BaseModel):
    id: int
    #name: str
    #description: Optional[str]
    #price: Decimal
    #category_id: Optional[int]
    #images: Optional[List[str]]
    #specifications: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True
        
class ArticleBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    short_description: str
    content: str
    images: Optional[List[str]] = Field(default_factory=list)
    tags: Optional[List[str]] = Field(default_factory=list)
    
    @field_validator('images', 'tags', mode='before')
    @classmethod
    def parse_json_list(cls, v, info):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v) if v else []
            except json.JSONDecodeError:
                return []
        return []

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    name: Optional[str]
    short_description: Optional[str]
    content: Optional[str]
    images: Optional[List[str]]
    tags: Optional[List[str]]

class ArticleOut(BaseModel):
    id: int
    #name: str
    #short_description: str
    #content: str
    #images: Optional[List[str]]
    #tags: Optional[List[str]]
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
class ProductCategoryOut(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True