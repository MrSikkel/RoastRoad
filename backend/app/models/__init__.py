"""ORM-модели приложения.

Импортирует все модели, чтобы Alembic и SQLAlchemy видели полный набор таблиц
в Base.metadata.
"""

from .address import UserAddress
from .article import Article, ArticleComment, CommentLike
from .cart import Cart, CartItem
from .category import Category
from .feedback import FeedbackRequest
from .order import Order, OrderItem, OrderStatus, PaymentMethod
from .password_reset import PasswordResetToken
from .product import Product
from .promocode import Promocode
from .user import Role, User

__all__ = [
    "Article",
    "ArticleComment",
    "Cart",
    "CartItem",
    "Category",
    "CommentLike",
    "FeedbackRequest",
    "Order",
    "OrderItem",
    "OrderStatus",
    "PasswordResetToken",
    "PaymentMethod",
    "Product",
    "Promocode",
    "Role",
    "User",
    "UserAddress",
]
