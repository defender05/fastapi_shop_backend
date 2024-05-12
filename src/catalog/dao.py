from .models import ProductModel, CategoryModel, CartModel, OrderModel
from .schemas import ProductCreate, ProductUpdate, CategoryCreate, CategoryUpdate
from ..base_dao import BaseDAO


class ProductDAO(BaseDAO[ProductModel, ProductCreate, ProductUpdate]):
    model = ProductModel

class CategoryDAO(BaseDAO[CategoryModel, CategoryCreate, CategoryUpdate]):
    model = CategoryModel

