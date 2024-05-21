from .models import ProductModel, CategoryModel, CartItemModel, OrderModel, OrderItemModel
from .schemas import (ProductCreate, ProductUpdate,
                      CategoryCreate, CategoryUpdate,
                      CartItemCreate, CartItemUpdate,
                      OrderBase, OrderCreate, OrderUpdate, CartItemBase, )
from ..base_dao import BaseDAO


class ProductDAO(BaseDAO[ProductModel, ProductCreate, ProductUpdate]):
    model = ProductModel

class CategoryDAO(BaseDAO[CategoryModel, CategoryCreate, CategoryUpdate]):
    model = CategoryModel

class CartDAO(BaseDAO[CartItemModel, CartItemBase, CartItemUpdate]):
    model = CartItemModel

class OrderDAO(BaseDAO[OrderModel, OrderCreate, OrderUpdate]):
    model = OrderModel