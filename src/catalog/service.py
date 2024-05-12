
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from .schemas import (Product, ProductCreate, ProductUpdate, Category, CategoryCreate, CategoryUpdate)
from .models import ProductModel, CategoryModel, CartModel, OrderModel
from .dao import ProductDAO, CategoryDAO
from ..exceptions import InvalidTokenException, TokenExpiredException
from ..database import async_session_maker
from ..config import settings


class ProductService:
    @classmethod
    async def get_products(cls, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Product]:
        async with async_session_maker() as session:
            products = await ProductDAO.find_all(session,*filter, offset=offset, limit=limit, **filter_by)

        if products is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
        return products


    @classmethod
    async def get_product_by_id(cls, product_id: int) -> Product:
        async with async_session_maker() as session:
            product = await ProductDAO.find_one_or_none(session, ProductModel.id == product_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Product by id:{product_id} not found")
        return product

    @classmethod
    async def create_product(cls, product: ProductCreate) -> Product:
        async with async_session_maker() as session:
            product_exist = await ProductDAO.find_one_or_none(session, sku=product.sku)
            if product_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

            new_product = await ProductDAO.add(
                session,
                product
            )
            await session.commit()

        return new_product

    @classmethod
    async def update_product(cls, product_id: int, product: ProductUpdate) -> ProductModel:
        async with async_session_maker() as session:
            product_exist = await ProductDAO.find_one_or_none(session, ProductModel.id == product_id)
            if product_exist is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

            updated_product = await ProductDAO.update(
                session,
                ProductModel.id == product_id,
                obj_in=product
            )
            await session.commit()
            return updated_product



class CategoryService:
    @classmethod
    async def get_categories(cls, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Category]:
        async with async_session_maker() as session:
            categories = await CategoryDAO.find_all(session, *filter, offset=offset, limit=limit, **filter_by)

        if categories is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categories not found")
        return [
            Category(
                id=str(item.id),
                name=item.name,
                parent_id=item.parent_id
            ) for item in categories
        ]

    @classmethod
    async def get_category_by_id(cls, category_id: int) -> Category:
        async with async_session_maker() as session:
            category = await CategoryDAO.find_one_or_none(session, CategoryModel.id == category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category


    @classmethod
    async def create_category(cls, category: CategoryCreate) -> Category:
        async with async_session_maker() as session:
            category_exist = await CategoryDAO.find_one_or_none(session, name=category.name)
            if category_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

            new_category = await CategoryDAO.add(
                session,
                category
            )
            await session.commit()

        return new_category
