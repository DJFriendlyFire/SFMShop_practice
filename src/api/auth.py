from datetime import datetime, timezone, timedelta
from typing import Optional

from asyncpg import Pool
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from src.api.config import settings
from src.database.dependencies import get_db_pool
from src.database.queries import users as user_queries

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    pool: Pool = Depends(get_db_pool),
):
    """Зависимость для получения текущего пользователя"""

    token = credentials.credentials
    token_data = decode_token(token)

    async with pool.acquire() as conn:
        user = await user_queries.get_user_by_id_with_conn(token_data.user_id, conn)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Юзер не найден или неактивен",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
    }


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет совпадает ли пароль с хешем"""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хэширует пароль перед сохранением в БД"""

    return pwd_context.hash(password)


class Token(BaseModel):
    """Модель ответа при логине"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenDate(BaseModel):
    """Модель данных которые получает из токена"""

    user_id: Optional[int] = None
    email: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен"""

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {"exp": expire, "iat": datetime.now(timezone.utc), "type": "access"}
    )

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> TokenDate:
    """Декодирует и проверяет JWT токен"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить ваши данные в системе",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        user_id: int = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise credentials_exception

        return TokenDate(user_id=user_id, email=email)

    except JWTError as e:
        raise credentials_exception
