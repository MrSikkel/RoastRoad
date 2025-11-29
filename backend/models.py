from sqlalchemy import Column, Integer, String, Enum, DateTime, func, ForeignKey, Boolean, Text, DECIMAL, JSON
from database import Base
from sqlalchemy.orm import relationship
import enum

# Роли для пользователя
class Role(enum.Enum):
    user = "user"
    admin = "admin"

"""
# Методы оплаты
class Payment_method(enum.Enum):
    card = "card"
    cash = "cash"
    online = "online"

# Статус заказа
class Order_status(enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
"""

# Пользователь
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    patronymic = Column(String(255))
    phone = Column(String(20))
    role = Column(Enum(Role), default=Role.user, nullable=False)
    registration_date = Column(DateTime, default=func.now())
    
    addresses = relationship("User_address", back_populates="user")
    #reviews = relationship("Review", back_populates="user")
    #articles = relationship("Article", back_populates="author")
    #comments = relationship("Article_comment", back_populates="user")
    #cart = relationship("Cart", back_populates="user", uselist=False)
    #orders = relationship("Order", back_populates="user")

# Адрес клиента
class User_address(Base):
    __tablename__ = "user_address"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    country = Column(String(63))
    city = Column(String(179))
    street = Column(String(58))
    house_number = Column(String(20))
    entrance = Column(Integer)
    is_current = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="addresses")
    #orders = relationship("Order", back_populates="address")

"""
# Товар
class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(7, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("product_category.id"), nullable=False, index=True)
    images = Column(JSON)
    specifications = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    category = relationship("Product_category", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    cart_items = relationship("Cart_item", back_populates="product")
    order_items = relationship("Order_item", back_populates="product")
    
    def get_specifications(self):
        if self.specifications:
            try:
                return json.loads(self.specifications)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_specifications(self, specifications):
        self.specifications = json.dumps(specifications) if specifications else None
    
    def get_specification_value(self, key, default=None):
        specs = self.get_specifications()
        return specs.get(key, default)
    
    def get_images(self):
        #Получить изображения как Python список"
        return self.images or []
    
    def add_image(self, image_url):
        #Добавить изображение
        if self.images is None:
            self.images = []
        if image_url not in self.images:
            self.images.append(image_url)
    
    def remove_image(self, image_url):
        #Удалить изображение
        if self.images and image_url in self.images:
            self.images.remove(image_url)

    
# Категории товаров
class Product_category(Base):
    __tablename__ = "product_category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

    products = relationship("Product", back_populates="category")
    
# Отзывы
class Review(Base):
    __tablename__ = "review"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")


# Статья
class Article(Base):
    __tablename__ = "article"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    comments_id = Column(Text)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    images = Column(JSON)
    tags = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    author = relationship("User", back_populates="articles")
    comments = relationship("Article_comment", back_populates="article")
    
    def get_images(self):
        #Получить изображения как Python список
        return self.images or []
    
    def get_tags(self):
        #Получить теги как Python список
        return self.tags or []

# Комментарии к статье
class Article_comment(Base):
    __tablename__ = "article_comment"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
  
  
# Корзина
class Cart(Base):
    __tablename__ = "cart"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="cart")
    items = relationship("Cart_item", back_populates="cart")
    
# Товар в корзине
class Cart_item(Base):
    __tablename__ = "cart_item"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")


# Заказ
class Order(Base):
    __tablename__ = "order"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("user_address.id"), nullable=False)
    payment_method = Column(Enum(Payment_method)) 
    promo_code = Column(String(255))
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(Order_status), default=Order_status.pending)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    address = relationship("User_address", back_populates="orders")
    items = relationship("Order_item", back_populates="order")
    
# Товар в заказе
class Order_item(Base):
    __tablename__ = "order_item"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
"""