# Архитектура системы с брокером сообщений для проекта SFMShop:
#
# Компоненты:
# 1. Producer (src/api/main.py):
#    - При создании заказа через POST /orders отправляет задачи в очередь
#    - Задачи отправляются быстро, API отвечает сразу
#    - Не блокирует ответ пользователю
#
# 2. Очередь сообщений (RabbitMQ):
#    - Хранит задачи для обработки
#    - Обеспечивает надежность доставки (сообщения не теряются)
#    - Поддерживает приоритеты задач
#    - Гарантирует порядок обработки
#
# 3. Consumer (src/services/queue_consumer.py):
#    - Получает задачи из очереди
#    - Обрабатывает задачи в фоне
#    - Обрабатывает ошибки и retry (3 попытки)
#    - Может масштабироваться (несколько воркеров)
#
# Задачи для очереди:
# - update_stock: обновление количества товаров на складе
# - send_email: отправка email-уведомлений пользователю
# - generate_report: генерация отчетов по заказам
# - send_notification: отправка push-уведомлений
#
# Преимущества:
# - Быстрый ответ API (не ждет выполнения задач)
# - Масштабируемость (можно запустить несколько Consumer)
# - Надежность (сообщения не теряются, retry при ошибках)
# - Разделение ответственности (API и обработка задач разделены)

from typing import Any

ORDER_STATUS_NEW = "new"
DEFAULT_PRICE = 0
DEFAULT_QUANTITY = 0


def calculate_total(items: list[dict[str, Any]]) -> float:
    """Вычисляет общую сумму заказа.
    Args:
    items: Список позиций заказа с полями 'price' и 'quantity'.

    Returns:
    Общая сумма заказа. Возвращает 0.0 для пустого списка.
    """
    if not items:
        return 0.0

    return sum(
        item.get("price", DEFAULT_PRICE) * item.get("quantity", DEFAULT_QUANTITY)
        for item in items
    )


def process_orders(orders: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Обрабатывает заказы со статусом 'new', добавляя общую сумму.
    Args:
    orders: Список заказов для обработки.

    Returns:
    Список обработанных заказов с добавленным полем 'total'.
    """
    if not orders:
        return []

    return [
        {**order, "total": calculate_total(order.get("items", []))}
        for order in orders
        if order.get("status") == ORDER_STATUS_NEW
    ]
