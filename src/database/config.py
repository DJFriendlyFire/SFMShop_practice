import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Настройки подключения к PostgreSQL"""

    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    host: str = os.getenv("DB_HOST")
    port: int = int(os.getenv("DB_PORT"))
    database: str = os.getenv("DB_NAME")

    @property
    def dsn(self) -> str:
        """Строка подключения DSN"""

        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def pool_config(self) -> dict:
        """Настройка пула соединений"""

        return {
            "dsn": self.dsn,
            "min_size": 2,
            "max_size": 10,
            "command_timeout": 60,
        }
