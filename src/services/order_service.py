"""
Краткий отчет по улучшениям:
- магические числа вынесены в константы
- добавлен типизация входных и выходных данных
- вложенный цикл вынесен в отдельную функцию для улучшения читаемости и разделения ответственности
- добавлены дополнительные проверки
- убрана промежуточная переменная result и используется более питонический подход с list comprehension
    при этом код остается читаемым
"""

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
