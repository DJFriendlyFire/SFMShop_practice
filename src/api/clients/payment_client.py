import httpx


class PaymentClient:
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def process_payment(self, order_id: str, amount: float):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._base_url}/api/v1/payment",
                    json={"order_id": order_id, "amount": amount},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Ошибка при попытке оплаты: {e}")
            return None
