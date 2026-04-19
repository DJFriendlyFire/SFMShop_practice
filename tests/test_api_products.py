from datetime import datetime, UTC
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.api import auth
from src.api.routes.products import router as products_routes
from src.database.dependencies import get_db_pool
from src.models.product import ProductCreate, ProductResponse


class MockAcquire:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


class MockPool:
    def __init__(self, conn=None):
        self.conn = conn or object()

    def acquire(self):
        return MockAcquire(self.conn)


@pytest.fixture
def app():
    app = FastAPI()

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request.state.request_id = "test-request-id"
        return await call_next(request)

    app.include_router(products_routes, prefix="/products", tags=["Products"])
    return app


@pytest.fixture
def set_pool(app: FastAPI):
    def _set(pool=None):
        app.dependency_overrides[get_db_pool] = lambda: pool or MockPool()

    _set()
    return _set


@pytest.fixture
def set_current_user(app: FastAPI):
    def _set(user_id: int = 1):
        app.dependency_overrides[auth.get_current_user] = lambda: {"user_id": user_id}

    _set()
    return _set


@pytest.fixture
def product_create_payload():
    return ProductCreate(name="Test-product", price=Decimal(123))


@pytest.fixture
def client(app: FastAPI, set_current_user, set_pool):
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def product_response_payload(product_create_payload):
    return ProductResponse(
        id=1,
        name="Test-product",
        price=Decimal(123),
        currency="RUB",
        stock_quantity=0,
        is_available=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


def test_create_product_success(
    client, product_create_payload, product_response_payload
):
    with patch(
        "src.api.routes.products.create_product_with_conn",
        new=AsyncMock(return_value=product_response_payload),
    ) as create_mock:
        response = client.post(
            "/products/", json=product_create_payload.model_dump(mode="json")
        )

    assert response.status_code == 201
    assert response.json()["id"] == product_response_payload.id
    assert response.json()["name"] == product_response_payload.name


def test_create_product_500(client, product_create_payload, product_response_payload):
    with patch(
        "src.api.routes.products.create_product_with_conn",
        new=AsyncMock(return_value=None),
    ) as create_mock:
        response = client.post(
            "/products/", json=product_create_payload.model_dump(mode="json")
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "Ошибка при создании продукта"


def test_get_product(client, product_response_payload):
    with patch(
        "src.api.routes.products.get_product_by_id_with_conn",
        new=AsyncMock(return_value=product_response_payload),
    ) as product_mock:
        response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["id"] == product_response_payload.id
    assert response.json()["name"] == product_response_payload.name
    assert response.json()["price"] == str(product_response_payload.price)


def test_get_product_404(client, product_response_payload):
    with patch(
        "src.api.routes.products.get_product_by_id_with_conn",
        new=AsyncMock(return_value=None),
    ) as product_mock:
        response = client.get("/products/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Продукт с ID=1 не найден"
