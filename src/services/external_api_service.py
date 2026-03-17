# src/services/external_api_service.py
import asyncio
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict

import httpx

logger = logging.getLogger(__name__)


class ExternalAPIError(Exception):
    """Базовое исключение для ошибок внешнего API."""

    pass


class RateLimitError(ExternalAPIError):
    """Превышен лимит запросов."""

    pass


class TimeoutError(ExternalAPIError):
    """Таймаут запроса."""

    pass


def retry_with_backoff(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Декоратор для повторных попыток с экспоненциальной задержкой.

    🔹 При ошибке ждёт: 1s → 2s → 4s → ...
    🔹 Не повторяет клиентские ошибки (4xx)
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)

                except (
                    httpx.TimeoutException,
                    httpx.NetworkError,
                    ExternalAPIError,
                ) as e:
                    last_exception = e
                    logger.warning(
                        f"⚠️ Попытка {attempt}/{max_attempts} не удалась: {e}"
                    )

                    if attempt < max_attempts:
                        # Экспоненциальная задержка: 1s, 2s, 4s...
                        delay = base_delay * (2 ** (attempt - 1))
                        logger.info(f"🔄 Повтор через {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"❌ Все {max_attempts} попыток исчерпаны")
                        raise

                except httpx.HTTPStatusError as e:
                    # 4xx ошибки не повторяем — это проблема клиента
                    if 400 <= e.response.status_code < 500:
                        logger.error(
                            f"❌ Клиентская ошибка {e.response.status_code}: {e}"
                        )
                        raise ExternalAPIError(f"API error: {e.response.status_code}")
                    # 5xx повторяем — проблема сервера
                    last_exception = e
                    if attempt < max_attempts:
                        delay = base_delay * (2 ** (attempt - 1))
                        await asyncio.sleep(delay)
                    else:
                        raise ExternalAPIError(f"Server error after retries: {e}")

            raise last_exception or ExternalAPIError("Unknown error")

        return wrapper

    return decorator


class CurrencyAPIService:
    """
    Клиент для API курсов валют: https://api.exchangerate-api.com

    🔹 Асинхронный (httpx.AsyncClient)
    🔹 Кэширование ответов (чтобы не превышать лимиты)
    🔹 Повторные попытки при ошибках сети
    🔹 Таймауты для защиты от зависаний
    """

    BASE_URL = "https://api.exchangerate-api.com/v4"
    TIMEOUT = 10.0  # секунд
    CACHE_TTL = timedelta(hours=1)  # Кэш живёт 1 час

    def __init__(self):
        # 🔹 Пул соединений для эффективности
        self._client: Optional[httpx.AsyncClient] = None
        # 🔹 Простой кэш в памяти: {base_currency: {data, expires_at}}
        self._cache: Dict[str, dict] = {}

    async def __aenter__(self):
        """Инициализация клиента (для context manager)."""
        self._client = httpx.AsyncClient(
            timeout=self.TIMEOUT,
            follow_redirects=True,
            # 🔹 Заголовки для вежливости к внешнему API
            headers={"User-Agent": "SFMShop/1.0 (currency-service)"},
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие клиента."""
        if self._client:
            await self._client.aclose()

    def _get_cached(self, base_currency: str) -> Optional[dict]:
        """Проверяет кэш."""
        entry = self._cache.get(base_currency)
        if entry and datetime.now() < entry["expires_at"]:
            logger.debug(f"📦 Cache hit for {base_currency}")
            return entry["data"]
        return None

    def _set_cache(self, base_currency: str, data: dict):
        """Сохраняет в кэш."""
        self._cache[base_currency] = {
            "data": data,
            "expires_at": datetime.now() + self.CACHE_TTL,
        }
        logger.debug(f"💾 Cached rates for {base_currency}")

    @retry_with_backoff(max_attempts=3, base_delay=1.0)
    async def get_exchange_rates(self, base_currency: str = "RUB") -> dict:
        """
        Получает курсы валют относительно базовой.

        🔹 Возвращает: {"base": "RUB", "rates": {"USD": 0.011, "EUR": 0.010, ...}}
        🔹 Кэширует ответ на 1 час
        🔹 Повторяет при сетевых ошибках

        :param base_currency: Код валюты (3 буквы, например "RUB", "USD")
        :raises ExternalAPIError: Если все попытки исчерпаны
        """
        base_currency = base_currency.upper()

        # 🔹 Проверяем кэш
        cached = self._get_cached(base_currency)
        if cached:
            return cached

        if not self._client:
            raise RuntimeError(
                "Client not initialized. Use async with context manager."
            )

        url = f"{self.BASE_URL}/latest/{base_currency}"

        logger.info(f"🌐 Fetching rates for {base_currency} from {url}")

        try:
            response = await self._client.get(url)
            response.raise_for_status()  # Выбрасывает ошибку на 4xx/5xx

            data = response.json()

            # 🔹 Валидация ответа
            if "rates" not in data:
                raise ExternalAPIError(f"Invalid API response: missing 'rates'")

            # 🔹 Сохраняем в кэш
            self._set_cache(base_currency, data)

            logger.info(f"✅ Got {len(data['rates'])} rates for {base_currency}")
            return data

        except httpx.TimeoutException:
            logger.error(f"⏰ Timeout fetching rates for {base_currency}")
            raise TimeoutError(f"Request timed out after {self.TIMEOUT}s")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.error(f"🚫 Rate limit exceeded for currency API")
                raise RateLimitError("Too many requests to currency API")
            logger.error(f"❌ HTTP {e.response.status_code}: {e}")
            raise

        except httpx.RequestError as e:
            logger.error(f"🔌 Network error: {e}")
            raise ExternalAPIError(f"Network error: {e}")

        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}", exc_info=True)
            raise ExternalAPIError(f"Unexpected error: {e}")

    async def convert_currency(
        self, amount: float, from_currency: str, to_currency: str
    ) -> Optional[float]:
        """
        Конвертирует сумму из одной валюты в другую.

        🔹 Использует cross-rate через базовую валюту
        🔹 Возвращает None если валюта не найдена
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return amount

        # 🔹 Получаем курсы относительно from_currency
        rates_data = await self.get_exchange_rates(from_currency)
        rates = rates_data.get("rates", {})

        if to_currency not in rates:
            logger.warning(f"❌ Currency {to_currency} not found in rates")
            return None

        converted = amount * rates[to_currency]
        logger.debug(f"💱 {amount} {from_currency} = {converted:.2f} {to_currency}")
        return round(converted, 2)

    async def get_supported_currencies(self, base_currency: str = "RUB") -> list[str]:
        """Возвращает список доступных валют."""
        data = await self.get_exchange_rates(base_currency)
        return list(data.get("rates", {}).keys())
