import logging

from asyncpg import Pool
from fastapi import APIRouter, status, Depends, HTTPException, Request

from src.api import auth
from src.database.dependencies import get_db_pool
from src.database.queries.users import (
    create_user_with_conn,
    get_user_by_id_with_conn,
    get_all_users_with_conn,
    update_user_with_conn,
    delete_user_with_conn,
)
from src.models.user import UserCreate, UserUpdate, UserResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Создать пользователя",
    dependencies=[Depends(auth.get_current_user)],
)
async def create_user(request: Request, user_in: UserCreate, pool: Pool = Depends(get_db_pool)):
    """Создает нового пользователя в системе"""

    request_id = request.state.request_id
    logger.info(f"UUD [{request_id}] create_user [{user_in.email}]")

    try:

        hashed_password = auth.get_password_hash(user_in.password_hash)
        user_in.password_hash = hashed_password

        async with pool.acquire() as conn:
            user = await create_user_with_conn(user_in, conn)

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка создания пользователя",
                )

            logger.info(f"UUD [{request_id}] user created [{user.id}]")
            return user

    except Exception as e:
        # Проверяем на уникальность email/username
        if "unique_violation" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already exists",
            )
        raise


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Получить текущего пользователя",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_my_profile(
    request: Request,
    current_user: dict = Depends(auth.get_current_user),
    pool: Pool = Depends(get_db_pool),
):
    """Возвращает данные текущего авторизованного пользователя"""

    request_id = request.state.request_id
    logger.info(
        f"UUID [{request_id}] get my profile by id={current_user['user_id']} started."
    )

    async with pool.acquire() as conn:
        user = await get_user_by_id_with_conn(current_user["user_id"], conn)
        logger.info(
            f"UUID [{request_id}] get my profile by id={current_user['user_id']} finished."
        )
        return user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя по ID",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_user(request: Request, user_id: int, pool: Pool = Depends(get_db_pool)):
    """Получить пользователя по ID"""

    request_id = request.state.request_id
    logger.info(f"UUD [{request_id}] get_user_id [{user_id}]")

    async with pool.acquire() as conn:
        user = await get_user_by_id_with_conn(user_id, conn)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )

        logger.info(f"UUD [{request_id}] return user_id [{user_id}]")
        return user


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Получить всех пользователей",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_all_users(
    request: Request, skip: int = 0, limit: int = 10, pool: Pool = Depends(get_db_pool)
):
    """Получить списка пользователей с пагинацией"""

    request_id = request.state.request_id
    logger.info(f"UUD [{request_id}] get_all_users ")

    async with pool.acquire() as conn:
        users = await get_all_users_with_conn(conn=conn, skip=skip, limit=limit)

        logger.info(f"UUD [{request_id}] return all_users ")
        return users


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Обновить пользователя",
    dependencies=[Depends(auth.get_current_user)],
)
async def update_user(
    request: Request,
    user_id: int,
    user_in: UserUpdate,
    current_user: dict = Depends(auth.get_current_user),
    pool: Pool = Depends(get_db_pool),
):
    """Частичное обновление данных пользователя (только те что пришли)"""
    request_id = request.state.request_id

    if current_user["user_id"] != user_id:
        logger.warning(
            f"UUD [{request_id}] Пользователь id={current_user['user_id']} пытался обновить не свои данные"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав на обновление другого пользователя",
        )

    logger.info(f"UUD [{request_id}] update_user_id [{user_id}] started")
    async with pool.acquire() as conn:
        user = await update_user_with_conn(user_id, user_in, conn)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Юзер с ID={user_id} не найден",
            )

        logger.info(f"UUD [{request_id}] return user [{user_id}] ")
        return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_user(
    request: Request,
    user_id: int,
    pool: Pool = Depends(get_db_pool),
    current_user: dict = Depends(auth.get_current_user),
):
    """Удаление пользователя по ID. Если успешно венет True"""

    request_id = request.state.request_id

    if current_user["user_id"] != user_id:
        logger.warning(
            f"UUD [{request_id}] Пользователь id={current_user['user_id']} пытался удалить не свои данные"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав на удаление другого пользователя",
        )

    logger.info(f"UUD [{request_id}] delete_user_id [{user_id}] started")

    async with pool.acquire() as conn:
        deleted_user = await delete_user_with_conn(user_id, conn)

        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Юзер с ID={user_id} не найден",
            )

        logger.info(f"UUD [{request_id}] delete user access [{user_id}] ")
        return None
