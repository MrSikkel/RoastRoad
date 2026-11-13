"""Pydantic-схемы приложения."""

from .address import AddressCreate, AddressOut, AddressUpdate
from .article import ArticleCreate, ArticleDetailOut, ArticleOut, ArticleUpdate
from .category import CategoryOut
from .product import ProductCreate, ProductDetailOut, ProductOut, ProductUpdate
from .user import (
    ChangePassword,
    ForgotPassword,
    ResetPassword,
    Token,
    UserLogin,
    UserOut,
    UserRegister,
    UserUpdate,
)

__all__ = [
    "AddressCreate",
    "AddressOut",
    "AddressUpdate",
    "ArticleCreate",
    "ArticleDetailOut",
    "ArticleOut",
    "ArticleUpdate",
    "CategoryOut",
    "ChangePassword",
    "ForgotPassword",
    "ProductCreate",
    "ProductDetailOut",
    "ProductOut",
    "ProductUpdate",
    "ResetPassword",
    "Token",
    "UserLogin",
    "UserOut",
    "UserRegister",
    "UserUpdate",
]
