# tests/test_schemas.py
from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models.order import OrderCreate
from src.models.product import ProductCreate
from src.models.user import UserCreate, UserResponse, UserUpdate


class TestUserSchemas:
    """Тесты для User схем."""

    def test_user_create_valid(self):
        """✅ Валидные данные создаются без ошибок."""
        user = UserCreate(
            email="test@example.com",
            username="testuser",
            password_hash="$2b$12$examplehash123",
            first_name="Иван",
            last_name="Иванов",
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    def test_user_create_invalid_email(self):
        """❌ Неверный email вызывает ошибку."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="not-an-email",  # ❌ Неверный формат
                username="testuser",
                password_hash="$2b$12$examplehash123",
            )
        assert "email" in str(exc_info.value).lower()

    def test_user_create_short_username(self):
        """❌ Короткий username вызывает ошибку."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="ab",  # ❌ Меньше 3 символов
                password_hash="$2b$12$examplehash123",
            )

    def test_user_create_from_dict(self):
        """✅ Можно создать из dict."""
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password_hash": "$2b$12$examplehash123",
        }
        user = UserCreate(**data)
        assert user.email == "test@example.com"

    def test_user_response_from_db_dict(self):
        """✅ UserResponse создаётся из dict (как из БД)."""
        db_data = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Иван",
            "last_name": "Иванов",
            "is_active": True,
            "is_verified": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        user = UserResponse(**db_data)
        assert user.id == 1
        assert user.email == "test@example.com"

    def test_user_update_partial(self):
        """✅ Update может содержать только некоторые поля."""
        update = UserUpdate(first_name="Пётр")
        assert update.first_name == "Пётр"
        assert update.email is None  # Не передано


class TestProductSchemas:
    """Тесты для Product схем."""

    def test_product_create_valid(self):
        """✅ Валидный товар создаётся."""
        product = ProductCreate(
            name="Тестовый товар", price=Decimal("999.99"), stock_quantity=100
        )
        assert product.name == "Тестовый товар"
        assert product.price == Decimal("999.99")

    def test_product_create_negative_price(self):
        """❌ Отрицательная цена вызывает ошибку."""
        with pytest.raises(ValidationError):
            ProductCreate(name="Товар", price=Decimal("-100"))  # ❌ Отрицательная

    def test_product_create_zero_price(self):
        """❌ Нулевая цена вызывает ошибку (gt=0)."""
        with pytest.raises(ValidationError):
            ProductCreate(name="Товар", price=Decimal("0"))  # ❌ Ноль


class TestOrderSchemas:
    """Тесты для Order схем."""

    def test_order_create_valid(self):
        """✅ Валидный заказ создаётся."""
        order = OrderCreate(
            user_id=1,
            total_amount=Decimal("1999.99"),
            shipping_address="г. Москва, ул. Тестовая, д. 1",
        )
        assert order.user_id == 1
        assert order.status == "pending"  # default

    def test_order_create_short_address(self):
        """❌ Короткий адрес вызывает ошибку."""
        with pytest.raises(ValidationError):
            OrderCreate(
                user_id=1,
                total_amount=Decimal("100"),
                shipping_address="Москва",  # ❌ Меньше 10 символов
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
