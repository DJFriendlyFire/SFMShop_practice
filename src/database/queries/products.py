from typing import Optional

from asyncpg import Connection

from src.models.product import ProductCreate, ProductUpdate, ProductResponse


async def create_product_with_conn(
    product_in: ProductCreate, conn: Connection
) -> Optional[ProductResponse]:
    """Создает товар."""

    query = """
    INSERT INTO products (name, price, description, currency, stock_quantity, sku, is_available)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING *;
    """

    row = await conn.fetchrow(
        query,
        product_in.name,
        product_in.price,
        product_in.description,
        product_in.currency,
        product_in.stock_quantity,
        product_in.sku,
        product_in.is_available,
    )
    return ProductResponse.model_validate(dict(row)) if row else None


async def get_product_by_id_with_conn(
    product_id: int, conn: Connection
) -> Optional[ProductResponse]:
    """Получает товар по ID."""

    query = """
    SELECT id, name, price, description, currency, stock_quantity, sku, is_available, created_at, updated_at
    FROM products
    WHERE id = $1;
    """

    row = await conn.fetchrow(query, product_id)
    return ProductResponse.model_validate(dict(row)) if row else None


async def get_all_products_with_conn(
    conn: Connection,
    skip: int = 0,
    limit: int = 10,
    is_available: Optional[bool] = None,
) -> list[ProductResponse]:
    """Получает список товаров с пагинацией и (если передан) фильтром по доступности (is_available)"""

    params = [skip, limit]
    if is_available is not None:
        query = """
        SELECT id, name, price, description, currency, stock_quantity, sku, is_available, created_at, updated_at
        FROM products
        WHERE is_available = $3
        ORDER BY id
        OFFSET $1 LIMIT $2;
        """
        params.append(is_available)
    else:
        query = """
                SELECT id, name, price, description, currency, stock_quantity, sku, is_available, created_at, updated_at
                FROM products
                ORDER BY id
                OFFSET $1 LIMIT $2;
                """

    rows = await conn.fetch(query, *params)
    return [ProductResponse.model_validate(dict(row)) for row in rows]


async def update_product_with_conn(
    product_id: int, product_in: ProductUpdate, conn: Connection
) -> Optional[ProductResponse]:
    """Обновляет информацию по товару (только переданное)."""

    updates = []
    values = []
    index_param = 1

    if product_in.name is not None:
        updates.append(f"name = ${index_param}")
        values.append(product_in.name)
        index_param += 1

    if product_in.price is not None:
        updates.append(f"price = ${index_param}")
        values.append(product_in.price)
        index_param += 1

    if product_in.description is not None:
        updates.append(f"description = ${index_param}")
        values.append(product_in.description)
        index_param += 1

    if product_in.currency is not None:
        updates.append(f"currency = ${index_param}")
        values.append(product_in.currency)
        index_param += 1

    if product_in.stock_quantity is not None:
        updates.append(f"stock_quantity = ${index_param}")
        values.append(product_in.stock_quantity)
        index_param += 1

    if product_in.sku is not None:
        updates.append(f"sku = ${index_param}")
        values.append(product_in.sku)
        index_param += 1

    if product_in.is_available is not None:
        updates.append(f"is_available = ${index_param}")
        values.append(product_in.is_available)
        index_param += 1

    if not updates:
        return await get_product_by_id_with_conn(product_id)

    updates.append("updated_at = NOW()")
    values.append(product_id)

    query = f"""
    UPDATE products 
    SET {', '.join(updates)}
    WHERE id = ${index_param}
    RETURNING *;
    """

    row = await conn.fetchrow(query, *values)
    return ProductResponse.model_validate(dict(row)) if row else None


async def delete_product_with_conn(product_id: int, conn: Connection) -> bool:
    """Удалить товар по ID."""

    query = """
    DELETE FROM products
    WHERE id = $1;
    """

    result = await conn.execute(query, product_id)
    rows_deleted = int(result.split()[-1])
    return rows_deleted > 0
