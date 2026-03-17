import time
from typing import Optional, List

import requests
from requests.exceptions import Timeout, ConnectionError, RequestException


class MultiExchangeClient:
    """
    Клиент для работы с несколькими API курсов валют
    Реализует fallback-механизм: при недоступности одного API
    автоматически переключается на следующий из списка.
    """

    def __init__(self, api_urls: List[str]):
        self.api_urls = api_urls
        self.timeout = 5
        self.max_retries = 3
        self.base_delay = 2

    def get_exchange_rate(self, base: str, target: str) -> Optional[float]:
        for api in self.api_urls:
            for attempt in range(self.max_retries):
                try:
                    print(f"Попытка №{attempt+1}, обращение к API:'{api}'")
                    response = requests.get(f"{api}/{base}", timeout=self.timeout)
                    response.raise_for_status()

                    data = response.json()

                    if target in data.get("rates", {}):
                        print(f"Курс найден. Попытка {attempt+1}, api:{api}")
                        return data["rates"][target]
                    else:
                        print(f"Валюта не найдена.")
                        break

                except (Timeout, ConnectionError) as e:
                    if attempt < self.max_retries:
                        delay = self.base_delay**attempt
                        print(
                            f"Ошибка в api:{api}, следующая попытка через {delay} сек"
                        )
                        time.sleep(delay)

                except RequestException:
                    print(f"Ошибка подключения к api:{api}.")
                    break

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
    # Пример использование:
    client = MultiExchangeClient(
        [
            "https://api.exchangerate-api.com/v4/latest",
            "https://api.currencyapi.com/v3/latest",
            "https://api.fixer.io/latest",
        ]
    )

    rate = client.convert_price(100, "USD", "RUB")
    print(rate)
