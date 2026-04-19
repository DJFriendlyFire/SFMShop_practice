import pytest

from src.utils.calculations import calculate_delivery, calculate_discount


class TestCalculateDiscount:

    @pytest.mark.parametrize(
        "order_total, expected_discount",
        [
            (0, 0),
            (999.99, 0),
            (1000, 50),
            (1000.01, 50.00),
            (5000, 500),
            (5000.01, 500.00),
            (10000, 1500),
            (10000.01, 1500.00),
            (50000, 7500),
        ],
        ids=[
            "zero_order",
            "just_below_1000",
            "exactly_1000",
            "just_above_1000",
            "exactly_5000",
            "just_above_5000",
            "exactly_10000",
            "just_above_10000",
            "large_order",
        ],
    )
    def test_discount_correct_value(self, order_total, expected_discount):
        assert calculate_discount(order_total) == expected_discount

    @pytest.mark.parametrize(
        "order_total, max_discount_rate",
        [
            (500, 0),
            (1000, 0.05),
            (5000, 0.10),
            (10000, 0.15),
        ],
    )
    def test_discount_does_not_exceed_rate(self, order_total, max_discount_rate):
        discount = calculate_discount(order_total)
        assert discount <= order_total * max_discount_rate

    @pytest.mark.parametrize(
        "invalid_total",
        [
            -1,
            -0.01,
            -9999,
        ],
        ids=["minus_one", "minus_small", "large_negative"],
    )
    def test_negative_order_raises(self, invalid_total):
        with pytest.raises(ValueError, match="Сумма не может быть отрицательной"):
            calculate_discount(invalid_total)


class TestCalculateDelivery:

    @pytest.mark.parametrize(
        "weight, distance, expected",
        [
            (0, 0, 100),
            (1, 0, 110),
            (0, 1, 105),
            (1, 1, 115),
            (10, 100, 700),
            (100, 1000, 6100),
        ],
        ids=[
            "zero_weight_zero_distance",
            "only_weight",
            "only_distance",
            "weight_and_distance",
            "medium_order",
            "large_values",
        ],
    )
    def test_delivery_cost(self, weight, distance, expected):
        assert calculate_delivery(weight, distance) == expected

    @pytest.mark.parametrize(
        "weight, distance",
        [
            (0, 0),
            (1, 1),
            (100, 100),
        ],
    )
    def test_base_price_always_included(self, weight, distance):
        """Стоимость доставки всегда >= базовой цены 100"""
        assert calculate_delivery(weight, distance) >= 100

    # --- Линейный рост от веса и расстояния ---
    def test_delivery_grows_with_weight(self):
        """Увеличение веса увеличивает стоимость"""
        assert calculate_delivery(1, 10) < calculate_delivery(2, 10)

    def test_delivery_grows_with_distance(self):
        """Увеличение расстояния увеличивает стоимость"""
        assert calculate_delivery(5, 1) < calculate_delivery(5, 2)
