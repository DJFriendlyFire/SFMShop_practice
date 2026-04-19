import pytest

from src.utils.calculations import calculate_discount


@pytest.fixture
def valid_orders():
    """Фикстура с валидными данными"""
    return [
        (0, 0),
        (500, 0),
        (999, 0),
        (1000, 50),
        (3000, 150),
        (5000, 500),
        (7000, 700),
        (10000, 1500),
        (20000, 3000),
    ]


@pytest.mark.parametrize(
    "order_total, expected_discount",
    [
        (0, 0),
        (999, 0),
        (1000, 50),
        (4999, 249.95),
        (5000, 500),
        (9999, 999.9),
        (10000, 1500),
    ],
)
def test_calculate_discount(order_total, expected_discount):
    """Параметризированный тест"""
    result = calculate_discount(order_total)
    assert result == expected_discount


def test_discount_with_fixture(valid_orders):
    """Тест с фикстурами"""
    for order_total, expected in valid_orders:
        assert calculate_discount(order_total) == expected


@pytest.mark.parametrize("order_total", [-1, -100, -9999])
def test_negative_order_total(order_total):
    """Проверка отрицательных значений"""
    with pytest.raises(ValueError, match="Сумма не может быть отрицательной"):
        calculate_discount(order_total)


@pytest.mark.parametrize(
    "order_total, expected",
    [
        (999, 0),  # граница перед 1000
        (1000, 50),  # ровно 1000
        (4999, 249.95),  # перед 5000
        (5000, 500),  # ровно 5000
        (9999, 999.9),  # перед 10000
        (10000, 1500),  # ровно 10000
    ],
)
def test_boundary_values(order_total, expected):
    """граничные случаи"""
    assert calculate_discount(order_total) == expected
