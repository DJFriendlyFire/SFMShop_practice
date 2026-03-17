import time
from typing import Optional

import requests
from requests.exceptions import Timeout, RequestException, ConnectionError


class ExchangeClient:

    def __init__(self, base_url: str = "https://api.exchangerate-api.com/v4/latest"):
        self.base_url = base_url
        self.timeout = 5
        self.max_retries = 3
        self.base_delay_retry = 2

    def get_exchange_rate(self, base: str, target: str) -> Optional[float]:
        """Получить актуальный курс валют с ретраями"""

        for attempt in range(self.max_retries):
            try:
                response = requests.get(f"{self.base_url}/{base}", timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                if target in data.get("rates", {}):
                    return data["rates"][target]
                else:
                    print(f"Валюта не найдена.")
                    return None

            except Timeout:
                if attempt < self.max_retries - 1:
                    delay = self.base_delay_retry**attempt
                    print(f"Таймаут, повтор через {delay} сек")
                    time.sleep(delay)
                else:
                    print("Все попытки исчерпаны.")
                    return None

            except ConnectionError:
                if attempt < self.max_retries - 1:
                    delay = 2**attempt
                    print(f"Ошибка подключения, повтор через {delay} сек")
                    time.sleep(delay)
                else:
                    print("Все попытки исчерпаны.")
                    return None

            except RequestException:
                print("Ошибка подключения.")
                return None

        return None

    def convert_price(
        self, price: float, from_currency: str, to_currency: str
    ) -> Optional[float]:
        """конвертация валют"""
        if from_currency == to_currency:
            return price

        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            return None

        return price * rate


if __name__ == "__main__":
    client = ExchangeClient()
    converted_price = client.convert_price(1000, "USD", "RUB")
    if converted_price:
        print(f"1000 USD = {converted_price} RUB")
    else:
        print("Не удалось получить курс валют")
