import datetime
import uuid
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    CREATED = 'СОЗДАН'
    PAID = 'ОПЛАЧЕН'
    COMPLETED = 'ЗАВЕРШЕН'
    CANCELLED = 'ОТМЕНЕН'


# Товары ///////////////////////////////////////////////////////////////
class ProductBase(BaseModel):
    sku: str = Field('sku_')
    name: str = Field(None)
    description: Optional[str] = Field(None)
    price: float = Field(0.0)
    discount_price: Optional[float] = Field(0.0)
    stock: int = Field(0)
    category_id: int = Field(0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    discount_price: Optional[float]
    stock: Optional[int]
    category_id: Optional[int]


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True




# Категории ///////////////////////////////////////////////////////////////
class CategoryBase(BaseModel):
    name: str = Field(None)
    # Если parent_id не указываем, то добавляем основную категорию
    # Если указываем, то добавляем подкатегорию для уже созданной категории
    parent_id: Optional[int] = Field(None)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True



# Корзина ///////////////////////////////////////////////////////////////
class CartItemBase(BaseModel):
    user_uuid: uuid.UUID = Field(None)
    product_id: int = Field(1)
    quantity: int = Field(1)
    price: float = Field(0.0)

class CartItemCreate(BaseModel):
    product_id: int = Field(1)
    quantity: int = Field(1, ge=1)
    price: float = Field(0.0)

class CartItemUpdate(CartItemBase):
    id: int
    quantity: int = Field(1, ge=1)

class CartItem(CartItemBase):
    id: int

    class Config:
        from_attributes = True



# Ордеры ///////////////////////////////////////////////////////////////
class OrderBase(BaseModel):
    user_uuid: Optional[uuid.UUID] = Field(None)
    created_at: Optional[datetime.datetime] = Field(None)
    status: OrderStatus = Field(OrderStatus.CREATED)
    total_price: float = Field(0.0)

class OrderCreate(OrderBase):
    pass
    # user_uuid: Optional[uuid.UUID] = Field(None)
    # status: OrderStatus = Field(OrderStatus.CREATED)
    # total_price: Optional[float] = Field(0.0)

class OrderUpdate(BaseModel):
    status: OrderStatus = Field(OrderStatus.CREATED)

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    user_uuid: Optional[uuid.UUID] = Field(None)
    product_id: int = Field(1, ge=1)
    quantity: int = Field(1, ge=1)
    price: float = Field(0.0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

    class Config:
        from_attributes = True
