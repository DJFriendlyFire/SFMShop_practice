# src/database/queries/users.py
from typing import Optional

from asyncpg import Connection
from pydantic import EmailStr

from src.models.user import UserCreate, UserResponse, UserUpdate


async def create_user_with_conn(
    user_in: UserCreate, conn: Connection
) -> Optional[UserResponse]:
    """
    Создаёт нового пользователя.
    Возвращает dict с данными пользователя (включая id).
    """

    query = """
    INSERT INTO users (email, username, password_hash, first_name, last_name)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING *;
    """

    row = await conn.fetchrow(
        query,
        user_in.email,
        user_in.username,
        user_in.password_hash,
        user_in.first_name,
        user_in.last_name,
    )
    return UserResponse.model_validate(dict(row)) if row else None


async def get_user_by_id_with_conn(
    user_id: int, conn: Connection
) -> Optional[UserResponse]:
    """Получает пользователя по ID."""

    query = """
    SELECT id, email, username, first_name, last_name, is_active, is_verified, created_at, updated_at
    FROM users
    WHERE id = $1;
    """

    row = await conn.fetchrow(query, user_id)
    return UserResponse.model_validate(dict(row)) if row else None


async def get_user_by_email_with_conn(
    email: EmailStr, conn: Connection
) -> Optional[UserResponse]:
    """Получает пользователя по email."""

    query = """
    SELECT id, email, username, first_name, last_name, is_active, is_verified, created_at, updated_at
    FROM users
    WHERE email = $1;
    """

    row = await conn.fetchrow(query, email)
    return UserResponse.model_validate(dict(row)) if row else None


async def get_all_users_with_conn(
    conn: Connection, skip: int = 0, limit: int = 10
) -> list[UserResponse]:
    """
    Получает список пользователей с пагинацией.

    skip: сколько записей пропустить (для пагинации)
    limit: сколько записей вернуть
    """

    query = """
    SELECT id, email, username, first_name, last_name, is_active, is_verified, created_at, updated_at
    FROM users
    ORDER BY id
    OFFSET $1 LIMIT $2; 
    """

    rows = await conn.fetch(query, skip, limit)
    return [UserResponse.model_validate(dict(row)) for row in rows]


async def update_user_with_conn(
    user_id: int, user_in: UserUpdate, conn: Connection
) -> Optional[UserResponse]:
    """Обновляет данные пользователя (только переданные поля)."""

    updates = []
    values = []
    index_param = 1

    if user_in.email is not None:
        updates.append(f"email = ${index_param}")
        values.append(user_in.email)
        index_param += 1

    if user_in.first_name is not None:
        updates.append(f"first_name = ${index_param}")
        values.append(user_in.first_name)
        index_param += 1

    if user_in.last_name is not None:
        updates.append(f"last_name = ${index_param}")
        values.append(user_in.last_name)
        index_param += 1

    if user_in.is_active is not None:
        updates.append(f"is_active = ${index_param}")
        values.append(user_in.is_active)
        index_param += 1

    if user_in.is_verified is not None:
        updates.append(f"is_verified = ${index_param}")
        values.append(user_in.is_active)
        index_param += 1

    if not updates:
        return await get_user_by_id_with_conn(user_id=user_id)

    updates.append(f"updated_at = NOW()")
    values.append(user_id)

    query = f"""
    UPDATE users
    SET {', '.join(updates)}
    WHERE id = ${index_param}
    RETURNING *;
    """

    row = await conn.fetchrow(query, *values)
    return UserResponse.model_validate(dict(row)) if row else None


async def delete_user_with_conn(user_id: int, conn: Connection) -> bool:
    """Удаляет пользователя по ID. Возвращает True если удалён."""

    query = """
    DELETE FROM users
    WHERE id = $1;
    """

    result = await conn.execute(query, user_id)
    rows_deleted = int(result.split()[-1])
    return rows_deleted > 0


async def get_user_for_auth(email: str, conn: Connection) -> Optional[dict]:
    """Получает пользователя вместе с password_hash (для проверки аутентификации)"""

    query = """
    SELECT id, email, password_hash, is_active
    FROM users
    WHERE LOWER(email) = LOWER($1);
    """

    row = await conn.fetchrow(query, email)
    return dict(row) if row else None
