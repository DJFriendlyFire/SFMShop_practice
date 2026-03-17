from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """Модель создания пользователя"""

    email: EmailStr = Field(
        ..., description="email Пользователя.", examples=["user@mail.com"]
    )
    username: str = Field(
        ...,
        min_length=4,
        max_length=100,
        description="login пользователя",
        examples=["qwerty"],
    )
    password_hash: str = Field(..., min_length=8, description="Хэш пароля")
    first_name: Optional[str] = Field(
        None, max_length=100, description="Имя", examples=["Иван"]
    )
    last_name: Optional[str] = Field(
        None, max_length=100, description="Фамилия", examples=["Поддубный"]
    )


class UserResponse(BaseModel):
    """Модель возврата юзера для клиента"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID пользователя")
    email: EmailStr = Field(..., description="email пользователя")
    username: str = Field(..., description="login пользователя")
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    is_active: bool = Field(True, description="Активен ли пользователь")
    is_verified: bool = Field(False, description="Подтвержден ли email")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")


class UserUpdate(BaseModel):
    """Модель для обновления данных пользователя"""

    email: Optional[EmailStr] = Field(None, description="Новый email")
    first_name: Optional[str] = Field(None, max_length=100, description="Новое имя")
    last_name: Optional[str] = Field(None, max_length=100, description="Новая фамилия")
    is_active: Optional[bool] = Field(None, description="Статус активности")
    is_verified: Optional[bool] = Field(None, description="Статус подтверждения")
