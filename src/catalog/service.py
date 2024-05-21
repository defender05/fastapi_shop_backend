import time
import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, insert, update, delete, literal, func
from sqlalchemy.orm import selectinload, joinedload, aliased, contains_eager

from .schemas import (OrderStatus,
                      Product, ProductCreate, ProductUpdate,
                      Category, CategoryCreate, CategoryUpdate,
                      CartItem, CartItemCreate, CartItemUpdate,
                      Order, OrderBase,
                      OrderItem, OrderItemCreate, OrderItemUpdate, CartItemBase, OrderCreate, OrderUpdate, )
from .models import ProductModel, CategoryModel, CartItemModel, OrderModel, OrderItemModel
from .dao import ProductDAO, CategoryDAO, CartDAO, OrderDAO
from ..exceptions import InvalidTokenException, TokenExpiredException
from ..database import async_session_maker
from ..config import settings


def generate_unique_id() -> str:
    epoch_ms = int(time.time())
    random_int = random.randint(1000, 9999)
    return f"{epoch_ms}.{random_int}"


class ProductService:
    @classmethod
    async def get_products(
            cls,
           *filter,
           offset: int = 0,
           limit: int = 100,
           **filter_by
    ) -> list[Product]:

        async with async_session_maker() as session:
            products = await ProductDAO.find_all(
                session,
                *filter,
                offset=offset,
                limit=limit,
                **filter_by
            )

        if products is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
        return products

    @classmethod
    async def get_products_by_category(
            cls,
            category_id: int
    ) -> list[Product]:

        async with async_session_maker() as session:
            # query = (
            #     select(CategoryModel)
            #     .where(CategoryModel.id == category_id)
            #     .union_all(
            #         select(CategoryModel).where(CategoryModel.parent_id == category_id)
            #     )
            # )
            subquery = (
                select(CategoryModel).where(CategoryModel.parent_id == category_id)
            )
            subresult = await session.execute(subquery)
            subcategories = subresult.scalars().all()
            subcats_ids = [category.id for category in subcategories]
            subcats_ids.append(category_id)

            prod_query = (
                select(ProductModel)
                .where(ProductModel.category_id.in_(subcats_ids))
            )
            prod_result = await session.execute(prod_query)
            products_orm = prod_result.scalars().all()
            products_dto = [Product.model_validate(product, from_attributes=True) for product in products_orm]
            products = products_dto

        if products is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
        return products  # [category for category in categories]

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


class CartService:
    @classmethod
    async def get_cart_items(cls, user_id: str) -> list[CartItem]:
        async with async_session_maker() as session:
            query = (
                select(CartItemModel)
                .where(CartItemModel.user_uuid == user_id)
            )
            result = await session.execute(query)
            cart = result.scalars().all()

        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
        return cart

    @classmethod
    async def add_item_to_cart(cls, item: CartItemCreate, user_id: str) -> CartItem:
        async with async_session_maker() as session:
            cartitem_exist = await CartDAO.find_one_or_none(session, product_id=item.product_id)
            if cartitem_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Cart item already exists")

            new_cart_item = await CartDAO.add(
                session,
                CartItemBase(
                    user_uuid=user_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                )
            )
            await session.commit()

        return new_cart_item

    @classmethod
    async def update_cart_item(cls, item: CartItemUpdate) -> CartItem:
        async with async_session_maker() as session:
            cart_item_exist = await CartDAO.find_one_or_none(session, CartItemModel.id == item.id)
            if cart_item_exist is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

            updated_cart_item = await CartDAO.update(
                session,
                CartItemModel.id == item.id,
                obj_in=item
            )
            await session.commit()
            return updated_cart_item


    @classmethod
    async def remove_cart_item(cls, cart_id: int):
        async with async_session_maker() as session:
            cartitem_exist = await CartDAO.find_one_or_none(session, id=cart_id)
            if cartitem_exist is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
            await CartDAO.delete(
                session,
                CartItemModel.id == cart_id
            )
            await session.commit()


class OrderService:
    @classmethod
    async def get_orders(cls, user_id: str) -> list[Order]:
        async with async_session_maker() as session:
            query = (
                select(OrderModel)
                .where(OrderModel.user_uuid == user_id)
            )
            result = await session.execute(query)
            orders = result.scalars().all()

        if orders is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found")
        return orders

    @classmethod
    async def create_order(cls, user_id: uuid.UUID) -> Order:
        async with async_session_maker() as session:
            # Создаем ордер
            total_price = 0.0
            order = OrderCreate(
                user_uuid=user_id,
                created_at=datetime.utcnow(),
                status=OrderStatus.CREATED,
                total_price=0
            )
            # Получаем список товаров в корзине
            cart_items = await CartService.get_cart_items(str(user_id))
            # Считаем итоговую сумму товаров
            for cart_item in cart_items:
                total_price += cart_item.price * cart_item.quantity

            # Сохраняем ордер
            order.total_price = total_price
            new_order = await OrderDAO.add(session, order)
            await session.commit()

            # Добавляем товары из корзины в ордер и удаляем их из корзины
            for cart_item in cart_items:
                add_orders_item = (
                    insert(OrderItemModel)
                    .values(
                        order_id=new_order.id,
                        product_id=cart_item.product_id,
                        quantity=cart_item.quantity,
                        price=cart_item.price
                    )
                )
                await session.execute(add_orders_item)
                await session.commit()

                # Удаляем товары из корзины
                await CartDAO.delete(session, CartItemModel.id == cart_item.id)
                await session.commit()

        return new_order

    @classmethod
    async def remove_order(cls, order_id: int):
        async with async_session_maker() as session:
            order_exist = await OrderDAO.find_one_or_none(session, id=order_id)
            if order_exist is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
            await OrderDAO.delete(
                session,
                OrderItemModel.id == order_id
            )
            await session.commit()

    @classmethod
    async def update_order(cls, order_id: int, order: OrderUpdate) -> Order:
        async with async_session_maker() as session:
            order_exist = await OrderDAO.find_one_or_none(session, OrderModel.id == order_id)
            if order_exist is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

            updated_order = await OrderDAO.update(
                session,
                OrderModel.id == order_id,
                obj_in=order
            )
            await session.commit()
            return updated_order
