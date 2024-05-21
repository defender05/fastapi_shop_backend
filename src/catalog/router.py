from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .models import ProductModel, CategoryModel
from .schemas import (Product, ProductCreate, ProductUpdate,
                      Category, CategoryCreate, CategoryUpdate,
                      CartItem, CartItemCreate, CartItemUpdate,
                      Order, OrderCreate, OrderUpdate)
from .service import ProductService, CategoryService, CartService, OrderService
from ..exceptions import InvalidCredentialsException
from ..config import settings
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.models import UserModel

catalog_router = APIRouter(prefix="/catalog", tags=["Catalog"])
cart_router = APIRouter(prefix="/user", tags=["Cart"])
order_router = APIRouter(prefix="/user", tags=["Order"])

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

@catalog_router.get("/products/{category_id}")
async def get_products_by_category(
        category_id: Optional[int] = None,
):
    products = await ProductService.get_products_by_category(category_id)
    # print(products)
    for item in products:
        print(item)

    return products

@catalog_router.get("/product/{product_id}")
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


@cart_router.get("/category/{category_id}")
async def get_category_by_id(
        category_id: int,
) -> Category:
    return await CategoryService.get_category_by_id(category_id)


@cart_router.get("/cart_items")
async def get_cart_items(
    current_user: UserModel = Depends(get_current_user)
) -> List[CartItem]:
    return await CartService.get_cart_items(user_id=current_user.id)


@cart_router.post("/add_cart_item", status_code=status.HTTP_201_CREATED)
async def add_cart_item(
        cart_item: CartItemCreate = Depends(CartItemCreate),
        current_user: UserModel = Depends(get_current_user),
) -> CartItem:
    return await CartService.add_item_to_cart(cart_item, current_user.id)


@cart_router.delete("/remove_cart_item", status_code=status.HTTP_200_OK)
async def remove_cart_item(
        cart_id: int,
        current_user: UserModel = Depends(get_current_user),
):
    await CartService.remove_cart_item(cart_id)


@order_router.post("/create_order", status_code=status.HTTP_201_CREATED)
async def create_order(
        current_user: UserModel = Depends(get_current_user),
) -> Order:
    new_order = await OrderService.create_order(current_user.id)
    return new_order

@order_router.get("/orders")
async def get_orders(
    current_user: UserModel = Depends(get_current_user)
) -> List[Order]:
    return await OrderService.get_orders(user_id=current_user.id)

@order_router.get("/update_order/{order_id}")
async def update_order(
    order_id: int,
    order: OrderUpdate = Depends(OrderUpdate),
    current_user: UserModel = Depends(get_current_user)
) -> Order:
    return await OrderService.update_order(order_id, order)
