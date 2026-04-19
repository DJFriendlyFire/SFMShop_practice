import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import uvicorn
from asyncpg import Pool
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api import auth as authorization
from src.api.middleware.logging import logging_middleware
from src.api.routes import users, products, orders, currency, auth
from src.database.connection import init_pool, close_pool
from src.database.dependencies import get_db_pool
from src.database.queries import orders as order_queries
from src.models.order import OrderCreate
from src.services.log_service import log_service
from src.services.queue_producer import QueueProducer

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
producer = QueueProducer(
    rabbitmq_url=os.getenv("RABBITMQ_URL"),
    exchange_name=os.getenv("RABBITMQ_EXCHANGE"),
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    log_service.info("Запуск приложения")
    await init_pool()
    log_service.info("Пул ДБ инициализирован")
    await producer.connect()
    log_service.info("RabbitMQ: коннект с producer инициализирован")

    yield

    log_service.info("Завершение работы приложения")
    await close_pool()
    log_service.info("ДБ пул закрыт")
    await producer.close()
    log_service.info("RabbitMQ: коннект с producer закрыт")


app = FastAPI(
    title="SFMShop",
    version="1.0.0",
    lifespan=lifespan,
)


app.middleware("http")(logging_middleware)

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(currency.router, prefix="/api/v1/currency", tags=["Currency"])


@app.get("/", tags=["Root"])
def root():
    """Корневой endpoints / Приветственное сообщение"""
    return {"message": "Welcome to SFMShop API", "docs": "/docs"}


@app.get("/admin", response_class=HTMLResponse, tags=["Admin"])
async def admin_page(request: Request):
    """HTML-страница админ панели"""
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
    dependencies=[Depends(authorization.get_current_user)],
)
async def create_order(
    request: Request, order_in: OrderCreate, pool: Pool = Depends(get_db_pool)
):
    """Создать новый заказ"""

    request_id = request.state.request_id
    log_service.info(f"UUID [{request_id}] create order started")

    async with pool.acquire() as conn:
        order = await order_queries.create_order_with_conn(order_in, conn)

        if order is None:
            log_service.error("Ошибка при создании заказа", uuid=request_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании заказа",
            )

        log_service.info(f"UUID [{request_id}] create order id={order.id} finished")

        try:
            await producer.send_order_task(task_type="send_email", order_data=order)
            await producer.send_order_task(task_type="update_stock", order_data=order)
            await producer.send_order_task(
                task_type="generate_report", order_data=order
            )
        except Exception as e:
            log_service.error(
                f"UUID [{request_id}] Failed to send tasks to RabbitMQ: {e}"
            )

        return order


@app.get("/debug/crash")
async def debug_crash():
    """Эндпоинт для тестирования Sentry — всегда падает"""
    raise Exception("Тестовая ошибка для Sentry!")


if __name__ == "__main__":
    uvicorn.run("src.api.main:app", reload=True)
