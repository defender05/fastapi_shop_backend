import uuid
from typing import Optional
from pydantic import BaseModel, Field

# Товары ///////////////////////////////////////////////////////////////
class ProductBase(BaseModel):
    sku: str = Field('sku_')
    name: str = Field(None)
    description: Optional[str] = Field(None)
    price: float = Field(0.0)
    discount_price: Optional[float] = Field(0.0)
    remaining_stock: int = Field(0)
    category_id: int = Field(0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    discount_price: Optional[float]
    remaining_stock: Optional[int]
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





# class Category(BaseModel):
#     name: str = Field(None)
#     sub_categories: list = Field(None)
#
#
# class CartItem(BaseModel):
#     product_id: int = Field(None)
#     quantity: int = Field(0)
#
#
# class Cart(BaseModel):
#     items: list[CartItem] = Field(None)
#
# class OrderItem(BaseModel):
#     product_id: int = Field(None)
#     quantity: int = Field(0)
#
#
# class Order(BaseModel):
#     items: list[OrderItem] = Field(None)
