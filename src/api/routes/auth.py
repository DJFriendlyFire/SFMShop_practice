from datetime import timedelta

from asyncpg import Pool
from fastapi import APIRouter, status, HTTPException, Depends

from src.api import auth
from src.api.config import settings
from src.database.dependencies import get_db_pool
from src.database.queries import users as user_quires
from src.models.auth import RegisterRequest, LoginRequest
from src.models.user import UserResponse, UserCreate

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_in: RegisterRequest, pool: Pool = Depends(get_db_pool)):

    email_lower = user_in.email.lower()
    async with pool.acquire() as conn:
        existing = await user_quires.get_user_by_email_with_conn(email_lower, conn)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой пользователь уже существует",
            )

    hashed_password = auth.get_password_hash(user_in.password)

    user_create = UserCreate(
        email=email_lower,
        username=user_in.username,
        password_hash=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )

    async with pool.acquire() as conn:
        user = await user_quires.create_user_with_conn(user_create, conn)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании пользователя",
            )

        return user


@router.post("/login", response_model=auth.Token)
async def login(credentials: LoginRequest, pool: Pool = Depends(get_db_pool)):
    """Аутентификация пользователя и выдача JWT"""

    async with pool.acquire() as conn:
        user = await user_quires.get_user_for_auth(credentials.email, conn)

        if not user or not auth.verify_password(
            credentials.password, user["password_hash"]
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некоректный email or login",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Учетная запись отключена"
            )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user["id"]), "email": str(user["email"])},
        expires_delta=access_token_expires,
    )

    return auth.Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.post("/token/verify")
async def verify_token(token: str):
    """Проверка валидности токена (для тестов)"""

    try:
        token_date = auth.decode_token(token)
        return {"valid": True, "user_id": token_date.user_id, "email": token_date.email}
    except HTTPException as e:
        return {"valid": False, "detail": e.detail}
