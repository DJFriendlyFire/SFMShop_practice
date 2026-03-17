import logging

from asyncpg import Pool
from fastapi import APIRouter, status, HTTPException, Depends, Request

from src.api import auth
from src.database.dependencies import get_db_pool
from src.database.queries.products import (
    create_product_with_conn,
    get_product_by_id_with_conn,
    get_all_products_with_conn,
    update_product_with_conn,
    delete_product_with_conn,
)
from src.models.product import ProductCreate, ProductUpdate, ProductResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать продукт",
    dependencies=[Depends(auth.get_current_user)],
)
async def create_product(
    request: Request, product_in: ProductCreate, pool: Pool = Depends(get_db_pool)
):
    """Создать новый продукт в системе"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] create product started")

    async with pool.acquire() as conn:
        product = await create_product_with_conn(product_in, conn)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании продукта",
            )

        logger.info(f"UUID [{request_id}] created product id={product.id} finished")
        return product


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Получить товар по ID",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_product(
    request: Request, product_id: int, pool: Pool = Depends(get_db_pool)
):
    """Получить товар по полю ID"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] get product by id={product_id} started")

    async with pool.acquire() as conn:
        product = await get_product_by_id_with_conn(product_id, conn)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Продукт с ID={product_id} не найден",
            )

        logger.info(f"UUID [{request_id}] get product by id={product_id} finished")
        return product


@router.get(
    "/",
    response_model=list[ProductResponse],
    summary="Получить все товары",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_all_products(
    request: Request,
    pool: Pool = Depends(get_db_pool),
    skip: int = 0,
    limit: int = 10,
):
    """Получить список всех товаров с пагинацией"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] get all products started")

    limit = min(limit, 100)
    async with pool.acquire() as conn:

        logger.info(f"UUID [{request_id}] get all products finished")
        return await get_all_products_with_conn(conn=conn, skip=skip, limit=limit)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Обновление товара",
    dependencies=[Depends(auth.get_current_user)],
)
async def update_product(
    request: Request,
    product_id: int,
    product_in: ProductUpdate,
    pool: Pool = Depends(get_db_pool),
):
    """Частичное обновление товара по ID(только то что передано)"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] update product by id={product_id} started")

    async with pool.acquire() as conn:
        product = await update_product_with_conn(product_id, product_in, conn)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID={product_id} не найден",
            )

        logger.info(f"UUID [{request_id}] update product by id={product_id} finished")
        return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить товар по ID",
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_product(
    request: Request, product_id: int, pool: Pool = Depends(get_db_pool)
):
    """Удалить товар по полю ID. Вернет True при успешном удалении"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] delete product by id={product_id} started")

    async with pool.acquire() as conn:
        deleted_product = await delete_product_with_conn(product_id, conn)

        if not deleted_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID={product_id} не найден",
            )

        logger.info(f"UUID [{request_id}] delete product by id={product_id} finished")
        return None
