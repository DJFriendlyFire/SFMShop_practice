from datetime import datetime
from decimal import Decimal

import pytest

from src.models.order import OrderResponse
from src.models.product import ProductResponse
from src.models.user import UserResponse


@pytest.fixture
def sample_product():
    """Фикстура: тестовый товар"""
    return ProductResponse(
        id=1,
        name="Тестовый товар",
        price=Decimal(123),
        currency="RUB",
        stock_quantity=1,
        is_available=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_user():
    """Фикстура: тестовый пользователь"""
    return UserResponse(
        id=1,
        email="example@mail.com",
        username="Avgust",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_order():
    """Фикстура: тестовый заказ"""
    return OrderResponse(
        id=1,
        user_id=1,
        total_amount=Decimal(0),
        shipping_address="dom",
        status="pending",
        currency="RUB",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_create_product(sample_product):
    """Тест: создание товара"""
    assert sample_product.id == 1
    assert sample_product.name == "Тестовый товар"
    assert sample_product.price == Decimal(123)
    assert sample_product.stock_quantity == 1


def test_create_user(sample_user):
    """Тест: создание пользователя"""
    assert sample_user.id == 1
    assert sample_user.email == "example@mail.com"
    assert sample_user.username == "Avgust"


def test_create_order(sample_order):
    """Тест: создание заказа"""
    assert sample_order.id == 1
    assert sample_order.user_id == 1
    assert sample_order.total_amount == Decimal(0)
    assert sample_order.shipping_address == "dom"
    assert sample_order.status == "pending"
    assert sample_order.currency == "RUB"
