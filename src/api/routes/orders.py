import logging

from asyncpg import Pool
from fastapi import APIRouter, status, HTTPException, Depends, Request

from src.api import auth
from src.database.dependencies import get_db_pool
from src.database.queries import orders as order_queries
from src.models.order import OrderCreate, OrderResponse, OrderUpdate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
    dependencies=[Depends(auth.get_current_user)],
)
async def create_order(
    request: Request, order_in: OrderCreate, pool: Pool = Depends(get_db_pool)
):
    """Создать новый заказ"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] create order started")

    async with pool.acquire() as conn:
        order = await order_queries.create_order_with_conn(order_in, conn)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании заказа",
            )

        logger.info(f"UUID [{request_id}] create order id={order.id} finished")
        return order


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Получить заказ",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_order(request: Request, order_id: int, pool: Pool = Depends(get_db_pool)):
    """Получить заказ по полю ID"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] get order by id={order_id} started")

    async with pool.acquire() as conn:
        order = await order_queries.get_order_by_id_with_conn(order_id, conn)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заказ с ID={order_id} не найден",
            )

        logger.info(f"UUID [{request_id}] get order by id={order_id} finished")
        return order


@router.get(
    "/",
    response_model=list[OrderResponse],
    summary="Получить все заказы",
    dependencies=[Depends(auth.get_current_user)],
)
async def get_all_orders(
    request: Request, skip: int = 0, limit: int = 10, pool: Pool = Depends(get_db_pool)
):
    """Получить список всех заказов с пагинацией"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] get all orders started")

    limit = min(limit, 100)
    async with pool.acquire() as conn:
        logger.info(f"UUID [{request_id}] get all orders finished")
        return await order_queries.get_all_orders_with_conn(
            conn=conn, skip=skip, limit=limit
        )


@router.patch(
    "/",
    response_model=OrderResponse,
    summary="Обновить заказ",
    dependencies=[Depends(auth.get_current_user)],
)
async def update_order(
    request: Request,
    order_id: int,
    order_in: OrderUpdate,
    pool: Pool = Depends(get_db_pool),
):
    """Обновить частично данные о заказе (только те которые пришли)"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] update order by id={order_id} started")

    async with pool.acquire() as conn:
        order = await order_queries.update_order_with_conn(order_id, order_in, conn)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заказ с ID={order_id} не найден",
            )

        logger.info(f"UUID [{request_id}] update order by id={order_id} finished")
        return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить заказ",
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_order(
    request: Request, order_id: int, pool: Pool = Depends(get_db_pool)
):
    """Удалить заказ по полю ID"""

    request_id = request.state.request_id
    logger.info(f"UUID [{request_id}] delete order by id={order_id} started")

    async with pool.acquire() as conn:
        deleted_order = await order_queries.delete_order_with_conn(order_id, conn)

        if not deleted_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заказ с ID={order_id} не найден",
            )

        logger.info(f"UUID [{request_id}] delete order by id={order_id} finished")
        return None
