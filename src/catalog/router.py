from typing import List, Optional
from fastapi import APIRouter, Depends, status
from .models import ProductModel, CategoryModel
from .schemas import (Product, ProductCreate, ProductUpdate, Category, CategoryCreate, CategoryUpdate)
from .service import ProductService, CategoryService
from ..exceptions import InvalidCredentialsException
from ..config import settings
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.models import UserModel

catalog_router = APIRouter(prefix="/catalog", tags=["Catalog"])


@catalog_router.post("/add_product", status_code=status.HTTP_201_CREATED)
async def add_product(
        product: ProductCreate = Depends(ProductCreate),
        current_user: UserModel = Depends(get_current_superuser),
) -> Product:
    return await ProductService.create_product(product)


@catalog_router.get("/products")
async def get_products(
        offset: Optional[int] = 0,
        limit: Optional[int] = 25,
) -> List[Product]:
    return await ProductService.get_products(offset=offset, limit=limit)

@catalog_router.get("/product{product_id}")
async def get_product_by_id(
        product_id: int,
) -> Product:
    return await ProductService.get_product_by_id(product_id)

@catalog_router.post("/add_category", status_code=status.HTTP_201_CREATED)
async def add_category(
        category: CategoryCreate = Depends(CategoryCreate),
        current_user: UserModel = Depends(get_current_superuser),
) -> Category:
    return await CategoryService.create_category(category)


@catalog_router.get("/categories")
async def get_categories(
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
) -> List[Category]:
    return await CategoryService.get_categories(offset=offset, limit=limit)

@catalog_router.get("/category{category_id}")
async def get_category_by_id(
        category_id: int,
) -> Category:
    return await CategoryService.get_category_by_id(category_id)