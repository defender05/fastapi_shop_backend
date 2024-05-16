from .models import ProductModel, CategoryModel, CartItemModel, OrderModel, OrderItemModel
from .schemas import (ProductCreate, ProductUpdate,
                      CategoryCreate, CategoryUpdate,
                      CartItemCreate, CartItemUpdate,)
from ..base_dao import BaseDAO


class ProductDAO(BaseDAO[ProductModel, ProductCreate, ProductUpdate]):
    model = ProductModel

class CategoryDAO(BaseDAO[CategoryModel, CategoryCreate, CategoryUpdate]):
    model = CategoryModel

class CartDAO(BaseDAO[CartItemModel, CartItemCreate, CartItemUpdate]):
    model = CartItemModel