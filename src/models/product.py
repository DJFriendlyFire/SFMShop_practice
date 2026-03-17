from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    price: Decimal = Field(..., gt=0, description="Цена товара")
    currency: str = Field("RUB", min_length=3, max_length=3, description="Валюта")
    stock_quantity: int = Field(0, ge=0, description="Кол-во товара на складе")
    sku: Optional[str] = Field(None, max_length=100, description="Артикул товара")
    is_available: bool = Field(True, description="Доступен ли товар для заказа")


class ProductResponse(BaseModel):
    """Модель возврата товара для клиента"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID товара")
    name: str = Field(..., description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    price: Decimal = Field(..., description="Цена товара")
    currency: str = Field(..., description="Валюта")
    stock_quantity: int = Field(..., description="Кол-во товара на складе")
    sku: Optional[str] = Field(None, description="Артикул товара")
    is_available: bool = Field(..., description="Доступен ли товар для заказа")
    created_at: datetime = Field(..., description="Дата создания товара")
    updated_at: datetime = Field(..., description="Дата последнего обновления товара")


class ProductUpdate(BaseModel):
    """Модель обновления товара"""

    name: Optional[str] = Field(
        None, min_length=3, max_length=255, description="Новое название товара"
    )
    description: Optional[str] = Field(None, description="Новое описание товара")
    price: Optional[Decimal] = Field(None, gt=0, description="Новая Цена товара")
    currency: Optional[str] = Field(
        None, min_length=3, max_length=3, description="Новая Валюта"
    )
    stock_quantity: Optional[int] = Field(
        None, ge=0, description="Новое Кол-во товара на складе"
    )
    sku: Optional[str] = Field(None, max_length=100, description="Новый Артикул товара")
    is_available: Optional[bool] = Field(
        None, description="Новая Доступность товар для заказа"
    )
