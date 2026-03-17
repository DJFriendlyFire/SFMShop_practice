from asyncpg import Pool

from src.database.connection import get_pool


async def get_db_pool() -> Pool:
    """Возвращает пул соединений"""

    pool = get_pool()
    return pool
