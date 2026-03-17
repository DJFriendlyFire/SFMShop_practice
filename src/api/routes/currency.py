# src/api/routes/currency.py
from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.services.external_api_service import (
    CurrencyAPIService,
    ExternalAPIError,
    RateLimitError,
    TimeoutError,
)

router = APIRouter()


# 🔹 Dependency для получения сервиса
async def get_currency_service() -> CurrencyAPIService:
    """Создаёт и возвращает сервис валют."""
    service = CurrencyAPIService()
    await service.__aenter__()  # Инициализируем клиент
    return service


@router.get("/rates")
async def get_rates(
    base: str = Query(
        default="RUB", description="Базовая валюта", min_length=3, max_length=3
    ),
    service: CurrencyAPIService = Depends(get_currency_service),
):
    """
    Получает текущие курсы валют.

    🔹 Ответ кэшируется на 1 час
    🔹 Повторные попытки при ошибках сети
    """
    try:
        data = await service.get_exchange_rates(base.upper())
        return {
            "success": True,
            "base": data["base"],
            "date": data.get("date"),
            "rates": data["rates"],
        }

    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="External API timeout. Please try again.",
        )
    except ExternalAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Currency API error: {str(e)}",
        )


@router.get("/convert")
async def convert_currency(
    amount: float = Query(..., gt=0, description="Сумма для конвертации"),
    from_currency: str = Query(
        ..., min_length=3, max_length=3, description="Из валюты"
    ),
    to_currency: str = Query(..., min_length=3, max_length=3, description="В валюту"),
    service: CurrencyAPIService = Depends(get_currency_service),
):
    """
    Конвертирует сумму из одной валюты в другую.

    🔹 Пример: ?amount=1000&from_currency=RUB&to_currency=USD
    """
    try:
        result = await service.convert_currency(amount, from_currency, to_currency)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot convert {from_currency} to {to_currency}",
            )

        return {
            "success": True,
            "from": {"amount": amount, "currency": from_currency.upper()},
            "to": {"amount": result, "currency": to_currency.upper()},
            "rate": result / amount if amount else 0,
        }

    except (RateLimitError, TimeoutError, ExternalAPIError) as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.get("/currencies")
async def list_currencies(
    base: str = Query(default="RUB", min_length=3, max_length=3),
    service: CurrencyAPIService = Depends(get_currency_service),
):
    """Возвращает список поддерживаемых валют."""
    try:
        currencies = await service.get_supported_currencies(base.upper())
        return {
            "success": True,
            "base": base.upper(),
            "count": len(currencies),
            "currencies": sorted(currencies),
        }
    except ExternalAPIError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
