from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    username: str = Field(
        ..., min_length=4, max_length=100, description="Login пользователя"
    )
    password: str = Field(..., min_length=8, description="Пароль пользователя")
    first_name: Optional[str] = Field(None, max_length=100, description="Имя")
    last_name: Optional[str] = Field(None, max_length=100, description="Фамилия")
