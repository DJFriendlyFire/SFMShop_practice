from datetime import datetime, UTC
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


class OrderCreate(BaseModel):
    """Модель создания заказа"""

    user_id: int = Field(..., gt=0, description="ID пользователя")
    total_amount: Decimal = Field(..., gt=0, description="Сумма заказа")
    shipping_address: str = Field(..., min_length=10, description="Адрес доставки")
    status: str = Field("pending", description="Статус заказа")
    currency: str = Field("RUB", min_length=3, max_length=3, description="Валюта")
    notes: Optional[str] = Field(
        None, max_length=100, description="Комментарий к заказу"
    )


class OrderResponse(BaseModel):
    """Модель заказов для возврата данных клиенту"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID заказа")
    user_id: int = Field(..., description="ID пользователя")
    total_amount: Decimal = Field(..., description="Сумма заказа")
    shipping_address: str = Field(..., description="Адрес доставки")
    status: str = Field(..., description="Статус заказа")
    currency: str = Field(..., description="Валюта")
    notes: Optional[str] = Field(None, description="Комментарий к заказу")
    created_at: datetime = Field(..., description="Дата создания заказа")
    updated_at: datetime = Field(..., description="Дата последнего обновления заказа")


class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Статус заказа")
    total_amount: Optional[Decimal] = Field(None, gt=0, description="Сумма заказа")
    shipping_address: Optional[str] = Field(
        None, min_length=10, description="Адрес доставки"
    )
    notes: Optional[str] = Field(None, description="Комментарий к заказу")


class OrderCreateEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str = "order.created"
    occurred_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    data: OrderResponse
