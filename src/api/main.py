import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from asyncpg import Pool
from dotenv import load_dotenv
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
from src.services.queue_producer import QueueProducer

load_dotenv()

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

    print(f"Запуск приложения...")
    await init_pool()
    print("Пул БД инициализирован.")
    await producer.connect()
    print("Коннект с Producer инициализирован.")

    yield

    print("Завершение работы приложения...")
    await close_pool()
    print("Пул ДЛ закрыт.")
    await producer.close()
    print("коннект с Producer закрыт.")


app = FastAPI(
    title="SFMShop",
    version="1.0.0",
    lifespan=lifespan,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

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
    logger.info(f"UUID [{request_id}] create order started")

    async with pool.acquire() as conn:
        order = await order_queries.create_order_with_conn(order_in, conn)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании заказа",
            )

        logger.info(f"UUID [{request_id}] create order id={order.id} finished")

        try:
            await producer.send_order_task(task_type="send_email", order_data=order)
            await producer.send_order_task(task_type="update_stock", order_data=order)
            await producer.send_order_task(
                task_type="generate_report", order_data=order
            )
        except Exception as e:
            logger.error(f"UUID [{request_id}] Failed to send tasks to RabbitMQ: {e}")

        return order


if __name__ == "__main__":
    uvicorn.run("src.api.main:app", reload=True)
