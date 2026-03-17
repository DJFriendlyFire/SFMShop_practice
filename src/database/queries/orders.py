from typing import Optional

from asyncpg import Connection

from src.models.order import OrderCreate, OrderUpdate, OrderResponse


async def create_order_with_conn(
    order_in: OrderCreate, conn: Connection
) -> Optional[OrderResponse]:
    """Создает новый заказ"""

    query = """
    INSERT INTO orders (user_id, status, total_amount, currency, shipping_address, notes)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING *;
    """

    row = await conn.fetchrow(
        query,
        order_in.user_id,
        order_in.status,
        order_in.total_amount,
        order_in.currency,
        order_in.shipping_address,
        order_in.notes,
    )
    return OrderResponse.model_validate(dict(row)) if row else None


async def get_order_by_id_with_conn(
    order_id: int, conn: Connection
) -> Optional[OrderResponse]:
    """Получает заказ по ID"""

    query = """
    SELECT id, user_id, status, total_amount, currency, shipping_address, notes, created_at, updated_at
    FROM orders
    WHERE id = $1;
    """

    row = await conn.fetchrow(query, order_id)
    return OrderResponse.model_validate(dict(row)) if row else None


async def get_orders_by_user_id_with_conn(
    conn: Connection, user_id: int, skip: int = 0, limit: int = 10
) -> list[OrderResponse]:
    """Получает все заказы конкретного юзера с пагинацией"""

    query = """
    SELECT id, user_id, status, total_amount, currency, shipping_address, notes, created_at, updated_at
    FROM orders
    WHERE user_id = $1
    ORDER BY created_at DESC
    OFFSET $2 LIMIT $3;
    """

    rows = await conn.fetch(query, user_id, skip, limit)
    return [OrderResponse.model_validate(dict(row)) for row in rows]


async def get_all_orders_with_conn(
    conn: Connection, skip: int = 0, limit: int = 10, status: Optional[str] = None
) -> list[OrderResponse]:
    """Получает все заказы с пагинацией и (если есть) фильтрацией по статусу"""

    params = [skip, limit]
    if status is not None:
        query = """
        SELECT id, user_id, status, total_amount, currency, shipping_address, notes, created_at, updated_at
        FROM orders
        WHERE status = $3
        ORDER BY created_at DESC
        OFFSET $1 LIMIT $2;
        """
        params.append(status)
    else:
        query = """
        SELECT id, user_id, status, total_amount, currency, shipping_address, notes, created_at, updated_at
        FROM orders
        ORDER BY created_at DESC
        OFFSET $1 LIMIT $2;
        """

    rows = await conn.fetch(query, *params)
    return [OrderResponse.model_validate(dict(row)) for row in rows]


async def update_order_with_conn(
    order_id: int, order_in: OrderUpdate, conn: Connection
) -> Optional[OrderResponse]:
    """Обновляет заказ только то что передано"""

    updates = []
    values = []
    index_params = 1

    if order_in.status is not None:
        updates.append(f"status = ${index_params}")
        values.append(order_in.status)
        index_params += 1

    if order_in.total_amount is not None:
        updates.append(f"total_amount = ${index_params}")
        values.append(order_in.total_amount)
        index_params += 1

    if order_in.shipping_address is not None:
        updates.append(f"shipping_address = ${index_params}")
        values.append(order_in.shipping_address)
        index_params += 1

    if order_in.notes is not None:
        updates.append(f"notes = ${index_params}")
        values.append(order_in.notes)
        index_params += 1

    if not updates:
        return await get_order_by_id_with_conn(order_id)

    updates.append("updated_at = NOW()")
    values.append(order_id)

    query = f"""
            UPDATE orders
            SET {', '.join(updates)}
            WHERE id = ${index_params}
            RETURNING *;
        """

    row = await conn.fetchrow(query, *values)
    return OrderResponse.model_validate(dict(row)) if row else None


async def delete_order_with_conn(order_id: int, conn: Connection) -> bool:
    """Удаляет заказ по полю ID"""

    query = """
    DELETE FROM orders
    WHERE id = $1;
    """

    result = await conn.execute(query, order_id)
    rows_deleted = int(result.split()[-1])
    return rows_deleted > 0
