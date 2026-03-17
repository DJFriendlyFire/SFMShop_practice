import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.middleware.logging import logging_middleware
from src.api.routes import users, products, orders, auth, currency
from src.database.connection import init_pool, close_pool

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):

    print(f"Запуск приложения...")
    await init_pool()
    print("Пул БД инициализирован.")

    yield

    print("Завершение работы приложения...")
    await close_pool()
    print("Пул ДЛ закрыт.")


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



if __name__ == "__main__":
    uvicorn.run("src.api.main:app", reload=True)
