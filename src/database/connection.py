from contextlib import asynccontextmanager

import asyncpg

from src.database.config import DatabaseConfig

_pool: asyncpg.Pool | None = None


async def init_pool():
    """Инициализация пула соединений"""

    global _pool
    if _pool is None:
        config = DatabaseConfig()
        _pool = await asyncpg.create_pool(**config.pool_config)
        print("Database pool initialized.")


async def close_pool():
    """Закрывает пул соединений при завершении приложения"""
    global _pool
    if _pool is not None:
        await _pool.close()
        print("Database pool closed.")
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool not initialized.")
    return _pool


@asynccontextmanager
async def get_connection():
    """Контекстный менеджер для получения соединения из пула"""
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn
