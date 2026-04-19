def calculate_discount(order_total: float) -> float:
    """Рассчитать скидку на основе суммы заказа"""
    # Проблема: нет тестов, непонятно, работает ли правильно
    if order_total < 0:
        raise ValueError("Сумма не может быть отрицательной")
    elif order_total >= 10000:
        return round(order_total * 0.15, 2)  # 15% скидка
    elif order_total >= 5000:
        return round(order_total * 0.10, 2)  # 10% скидка
    elif order_total >= 1000:
        return round(order_total * 0.05, 2)  # 5% скидка
    else:
        return 0  # Нет скидки


def calculate_delivery(weight: float, distance: float) -> float:
    """
    Функция расчета стоимости доставки

    :arg weight: Вес товара в кг
    :arg distance: Расстояние доставки в км

    :return Стоимость доставки в рублях
    """
    base_price = 100
    weight_price = weight * 10
    distance_price = distance * 5

    return round(base_price + weight_price + distance_price)
