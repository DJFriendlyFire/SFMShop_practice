import asyncio

async def process_order_async(order):
    """Асинхронная обработка заказа"""
    await asyncio.sleep(0.1)  # Имитация асинхронной операции
    return f"Заказ {order.id} обработан"
