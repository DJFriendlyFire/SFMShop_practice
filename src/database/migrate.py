# src/database/migrate.py

import asyncio
import sys

from src.database.connection import init_pool, get_pool, close_pool
from src.database.tables import MIGRATIONS


async def run_migrations():
    """Выполняет миграции."""

    print("Starting database migrations...")

    try:
        await init_pool()
        pool = get_pool()

        for migrate_name, sql_query in MIGRATIONS:
            print(f"{migrate_name} starting....")
            try:
                await pool.execute(sql_query)
                print(f"{migrate_name} completed.")
            except Exception as e:
                print(f"{migrate_name} FAILED: {e}")
                raise

        print(f"All migrations completed.")
        return True

    except Exception as e:
        print(f"Migrations ERROR: {e}")
        return False

    finally:
        await close_pool()


if __name__ == "__main__":
    success = asyncio.run(run_migrations())
    sys.exit(0 if success else 1)
