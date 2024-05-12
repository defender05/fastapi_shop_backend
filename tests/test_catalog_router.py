import uuid
import pytest
from httpx import AsyncClient
from fastapi import status
# from fastapi.testclient import TestClient
from src.main import app
from src.catalog.models import ProductModel, CategoryModel

# Создаем экземпляр TestClient для тестирования ендпоинтов приложения
# sync_client = TestClient(app)

# Тест для ендпоинта /add_product
@pytest.mark.anyio
async def test_add_product():
    new_product = {
        "sku": str(uuid.uuid4()),
        "name": "Test",
        "description": "Test",
        "price": 10,
        "discount_price": 5,
        "remaining_stock": 10,
        "category_id": 1
    }
    async with AsyncClient(app=app) as client:
        token = await client.post(
            url="/login",
            json={"email": "admin", "password": "123"}
        )
        created_product = await client.post(
            "/add_product",
            json=new_product,
            headers={'Authorization': 'Bearer ' + token.text}
        )
    assert created_product.status_code == status.HTTP_201_CREATED
    assert created_product.json() == new_product

# Тест для ендпоинта /products
# @pytest.mark.anyio
# async def test_get_products():
#     async with AsyncClient(app=app) as client:
#         response = await client.get("/products")
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.json(), list)
#
# # Тест для ендпоинта /product/{product_id}
# @pytest.mark.anyio
# async def test_get_product_by_id():
#     product_id = 1  # Предполагается, что есть продукт с id=1
#     async with AsyncClient(app=app) as client:
#         response = await client.get(f"/product{product_id}")
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.json(), ProductModel)
#
# # Тест для ендпоинта /add_category
# @pytest.mark.anyio
# async def test_add_category():
#     new_category = {"name": "Test Category"}
#     async with AsyncClient(app=app) as client:
#         response = await client.post("/add_category", json=new_category)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json() == new_category
#
# # Тест для ендпоинта /categories
# @pytest.mark.anyio
# async def test_get_categories():
#     async with AsyncClient(app=app) as client:
#         response = await client.get("/categories")
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.json(), list)
#
# # Тест для ендпоинта /category/{category_id}
# @pytest.mark.anyio
# async def test_get_category_by_id():
#     category_id = 1  # Предполагается, что есть категория с id=1
#     async with AsyncClient(app=app) as client:
#         response = await client.get(f"/category{category_id}")
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.json(), CategoryModel)


# if __name__ == "__main__":
#     # Запуск всех тестов
#     test_add_product()
#     test_get_products()
#     test_get_product_by_id()
#     test_add_category()
#     test_get_categories()
#     test_get_category_by_id()
