# ==================
# УРОК 1: ПЕРЕМЕННЫЕ И СТРОКИ (STR)
# ==================

# Решение задачи от тимлида
company_name = "SFMShop"

welcome_message = "Добро пожаловать в " + company_name + "!"
slogan = company_name + " - лучший выбор для покупок"
email_subject = "Спасибо за покупку в " + company_name

print(welcome_message)
print(slogan)
print(email_subject)

# Практика: Задание 1 - Форматирование имен пользователей
raw_name_1 = "ИВАН"
raw_name_2 = "мария"
raw_name_3 = "пЕТР"

formatted_name_1 = raw_name_1.capitalize()
formatted_name_2 = raw_name_2.capitalize()
formatted_name_3 = raw_name_3.capitalize()

print(formatted_name_1)
print(formatted_name_2)
print(formatted_name_3)

# Практика: Задание 2 - Форматирование цены
price = "1999"

price_prefix = "от"
currency = "руб."

formatted_price = price_prefix + " " + price + " " + currency
print(formatted_price)

# Практика: Задание 3 - Расширенная обработка имен
name_1 = "  ИВАН  "
name_2 = "мария"
name_3 = "  пЕТР  "
name_4 = "АННА"
name_5 = "  олег  "

cleaned_name_1 = name_1.strip().capitalize()
cleaned_name_2 = name_2.strip().capitalize()
cleaned_name_3 = name_3.strip().capitalize()
cleaned_name_4 = name_4.strip().capitalize()
cleaned_name_5 = name_5.strip().capitalize()

print(cleaned_name_1)
print(cleaned_name_2)
print(cleaned_name_3)
print(cleaned_name_4)
print(cleaned_name_5)

# ==================
# УРОК 2: ЧИСЛА (INT, FLOAT)
# ==================

# Урок 2: Решение задачи от тимлида - Конвертация валют
exchange_rate = 75.5

product_1_price_usd = 29.99
product_2_price_usd = 49.99
product_3_price_usd = 99.99

# Конвертируем в рубли и округляем
product_1_price_rub = round(product_1_price_usd * exchange_rate, 2)
product_2_price_rub = round(product_2_price_usd * exchange_rate, 2)
product_3_price_rub = round(product_3_price_usd * exchange_rate, 2)

print(product_1_price_rub)
print(product_2_price_rub)
print(product_3_price_rub)

# Практика: Задание 1 - Расчет итоговой стоимости заказа
price_per_item = 1500.0
quantity = 3
discount = 0.1  # 10% скидка

# Расчет итоговой стоимости
final_price = price_per_item * quantity * (1 - discount)
final_price_rounded = round(final_price, 2)

print(final_price_rounded)

# Практика: Задание 2 - Расширенный расчет стоимости заказов
# Заказ 1: с обычной скидкой
order_1_price = 2000.0
order_1_quantity = 2
order_1_discount = 0.15

# Заказ 2: без скидки
order_2_price = 3000.0
order_2_quantity = 1
order_2_discount = 0.0

# Заказ 3: с большой суммой
order_3_price = 5000.0
order_3_quantity = 3
order_3_discount = 0.2

# Обработка заказа 1
subtotal_1 = order_1_price * order_1_quantity
discount_amount_1 = subtotal_1 * order_1_discount
final_price_1 = round(subtotal_1 - discount_amount_1, 2)

print("Заказ 1:")
print("Исходная цена:", subtotal_1, "руб.")
print("Размер скидки:", discount_amount_1, "руб.")
print("Итоговая стоимость:", final_price_1, "руб.")
print()

# Обработка заказа 2
subtotal_2 = order_2_price * order_2_quantity
discount_amount_2 = subtotal_2 * order_2_discount
final_price_2 = round(subtotal_2 - discount_amount_2, 2)

print("Заказ 2:")
print("Исходная цена:", subtotal_2, "руб.")
print("Размер скидки:", discount_amount_2, "руб.")
print("Итоговая стоимость:", final_price_2, "руб.")
print()

# Обработка заказа 3
subtotal_3 = order_3_price * order_3_quantity
discount_amount_3 = subtotal_3 * order_3_discount
final_price_3 = round(subtotal_3 - discount_amount_3, 2)

print("Заказ 3:")
print("Исходная цена:", subtotal_3, "руб.")
print("Размер скидки:", discount_amount_3, "руб.")
print("Итоговая стоимость:", final_price_3, "руб.")
print()

# ==================
# УРОК 3: УСЛОВНЫЕ ОПЕРАТОРЫ
# ==================

# Урок 3: Решение задачи от тимлида - Проверка условий заказа
user_age = 20
product_quantity = 5

# Проверяем оба условия через and
if user_age >= 18 and product_quantity > 0:
    print("Заказ можно оформить")
else:
    # Определяем причину отказа
    if user_age < 18:
        print("Заказ нельзя оформить: пользователь несовершеннолетний")
    if product_quantity <= 0:
        print("Заказ нельзя оформить: товара нет на складе")

# Практика: Задание 1 - Определение размера скидки
order_total = 6000

if order_total > 10000:
    discount_rate = 0.15  # 15%
elif order_total > 5000:
    discount_rate = 0.10  # 10%
else:
    discount_rate = 0.05  # 5%

print("Размер скидки:", discount_rate * 100, "%")

# Практика: Задание 2 - Валидация и расчет стоимости заказа
order_total = 6000

# Проверяем, что сумма не отрицательная
if order_total < 0:
    print("Ошибка: сумма заказа не может быть отрицательной")
else:
    # Определяем размер скидки
    if order_total > 10000:
        discount_rate = 0.15
    elif order_total > 5000:
        discount_rate = 0.10
    else:
        discount_rate = 0.05

    # Рассчитываем размер скидки в рублях
    discount_amount = order_total * discount_rate

    # Рассчитываем итоговую стоимость
    final_price = round(order_total - discount_amount, 2)

    # Выводим результаты
    print("Исходная сумма:", order_total, "руб.")
    print("Размер скидки:", discount_rate * 100, "%")
    print("Размер скидки:", discount_amount, "руб.")
    print("Итоговая стоимость:", final_price, "руб.")

# ==================
# УРОК 4: ЦИКЛЫ (FOR, WHILE)
# ==================

# Урок 4: Решение задачи от тимлида - Поиск заказов с суммой больше 5000
order_1 = 3000
order_2 = 6000
order_3 = 4500
order_4 = 8000
order_5 = 2000

# Создаем последовательность заказов через range
for i in range(1, 6):
    # Получаем значение заказа в зависимости от номера
    if i == 1:
        order_total = order_1
    elif i == 2:
        order_total = order_2
    elif i == 3:
        order_total = order_3
    elif i == 4:
        order_total = order_4
    else:
        order_total = order_5

    # Проверяем условие и выводим
    if order_total > 5000:
        print("Заказ", i, ":", order_total)

# Практика: Задание 1 - Поиск товаров с ценой больше 1000
price_1 = 500
price_2 = 1500
price_3 = 800
price_4 = 2000
price_5 = 1200

# Перебираем товары от 1 до 5
for product_number in range(1, 6):
    # Определяем цену товара по номеру
    if product_number == 1:
        price = price_1
    elif product_number == 2:
        price = price_2
    elif product_number == 3:
        price = price_3
    elif product_number == 4:
        price = price_4
    else:
        price = price_5

    # Проверяем условие и выводим
    if price > 1000:
        print("Товар", product_number, ":", price, "руб.")

# Практика: Задание 2 - Расширенная обработка товаров
price_1 = 500
price_2 = 1500
price_3 = 800
price_4 = 2000
price_5 = 1200

# Счетчик товаров с ценой больше 1000
count = 0

# Переменные для поиска максимальной цены
max_price = 0
max_price_product = 0

print("Товары с ценой больше 1000:")

# Перебираем товары от 1 до 5
for product_number in range(1, 6):
    # Определяем цену товара по номеру
    if product_number == 1:
        price = price_1
    elif product_number == 2:
        price = price_2
    elif product_number == 3:
        price = price_3
    elif product_number == 4:
        price = price_4
    else:
        price = price_5

    # Проверяем условие и выводим
    if price > 1000:
        print("Товар", product_number, ":", price, "руб.")
        count = count + 1

    # Ищем максимальную цену
    if price > max_price:
        max_price = price
        max_price_product = product_number

print("Количество товаров с ценой больше 1000:", count)
print(
    "Товар с максимальной ценой: Товар", max_price_product, ", цена", max_price, "руб."
)

# ==================
# УРОК 5: СПИСКИ (LIST)
# ==================

# Урок 5: Решение задачи от тимлида - Подсчет общей суммы заказов
orders = [1500, 2300, 890, 4500, 1200]

# Используем встроенные функции
total = sum(orders)
count = len(orders)
average = total / count

print("Общая сумма:", total)
print("Средний чек:", average)

# Практика: Задание 1 - Сортировка и поиск цен товаров
prices = [1500, 2300, 890, 4500, 1200]

# Сортируем по убыванию
prices.sort(reverse=True)

# Находим максимальную и минимальную цену
max_price = max(prices)
min_price = min(prices)

# Выводим результаты
print("Отсортированные цены:", prices)
print("Максимальная цена:", max_price)
print("Минимальная цена:", min_price)

# Практика: Задание 2 - Управление корзиной покупок
cart = []

# Добавляем товары
cart.append(["Ноутбук", 50000])
cart.append(["Мышь", 1500])
cart.append(["Клавиатура", 3000])

print("Корзина после добавления товаров:", cart)

# Удаляем товар
cart.remove(["Мышь", 1500])

print("Корзина после удаления:", cart)

# Сортируем по названию
cart.sort()

print("Корзина после сортировки:", cart)

# Ищем самый дорогой товар
if len(cart) > 0:
    max_price = 0
    max_price_item = None

    for item in cart:
        price = item[1]  # Цена - второй элемент (индекс 1)
        if price > max_price:
            max_price = price
            max_price_item = item

    print("Самый дорогой товар:", max_price_item)
else:
    print("Корзина пустая")

# ==================
# УРОК 6: СЛОВАРИ (DICT) И МНОЖЕСТВА (SET)
# ==================

# Урок 6: Решение задачи от тимлида - Хранение данных пользователя и подсчет уникальных посетителей
# Хранение данных пользователя в словаре
user = {"name": "Иван Иванов", "email": "ivan@example.com", "phone": "+7 999 123-45-67"}

# Получение данных по ключу
print("Имя:", user["name"])
print("Email:", user["email"])

# Подсчет уникальных посетителей через множество
visitors = {"user_123", "user_456", "user_123", "user_789"}
unique_count = len(visitors)

print("Уникальных посетителей:", unique_count)

# Практика: Задание 1 - Работа со словарем товара
product = {"name": "Ноутбук", "price": 50000, "quantity": 5}

# Обновляем количество
product["quantity"] = 10

# Получаем ключи и значения
keys = product.keys()
values = product.values()

print("Ключи словаря:", keys)
print("Значения словаря:", values)

# Практика: Задание 2 - Система хранения данных о пользователях и товарах
# Словарь пользователей
users = {}

# Словарь товаров
products = {
    "Ноутбук": {"price": 50000, "category": "Электроника"},
    "Мышь": {"price": 1500, "category": "Аксессуары"},
}

# Множество уникальных посетителей
visitors = set()

# Добавление пользователя
users[1] = {"name": "Иван", "email": "ivan@test.com"}

print("Пользователь добавлен:", users[1])

# Поиск товара
if "Ноутбук" in products:
    laptop = products["Ноутбук"]
    price = laptop["price"]
    print("Цена товара 'Ноутбук':", price, "руб.")
else:
    print("Товар не найден")

# Проверка уникальности посетителя
visitors.add("user_123")
is_visited = "user_123" in visitors
print("Посетитель 'user_123' был на сайте:", is_visited)

# ==================
# УРОК 7: КОРТЕЖИ (TUPLE) И ИХ ОСОБЕННОСТИ
# ==================

# Урок 7: Решение задачи от тимлида - Хранение размеров товара
# Хранение размеров в кортеже
dimensions = (30, 20, 15)

# Распаковка для расчета объема
length, width, height = dimensions
volume = length * width * height

print("Размеры товара:", dimensions)
print("Объем упаковки:", volume)

# Практика: Задание 1 - Работа с кортежами
# Создание кортежа с координатами
coordinates = (10, 20)

# Распаковка кортежа
x, y = coordinates

print("Координата x:", x)
print("Координата y:", y)

# Использование кортежа как ключа в словаре
locations = {(10, 20): "Офис", (30, 40): "Склад"}

# Получение названия места по координатам
location_name = locations[coordinates]
print("Название места:", location_name)

# Практика: Задание 2 - Система хранения координат доставки
# Словарь для хранения координат доставки
delivery_coordinates = {}

# Добавление координат для заказов
delivery_coordinates[1] = (55.7558, 37.6173)
delivery_coordinates[2] = (59.9343, 30.3351)

# Получение координат заказа с ID 1
order_id = 1
if order_id in delivery_coordinates:
    coords = delivery_coordinates[order_id]
    print("Координаты заказа", order_id, ":", coords)

    # Распаковка координат
    latitude, longitude = coords
    print("Широта:", latitude)
    print("Долгота:", longitude)
else:
    print("Координаты заказа", order_id, ": Заказ не найден")

# Обработка случая отсутствия заказа
order_id = 3
if order_id in delivery_coordinates:
    coords = delivery_coordinates[order_id]
    print("Координаты заказа", order_id, ":", coords)
else:
    print("Координаты заказа", order_id, ": Заказ не найден")

# ==================
# УРОК 8: ФУНКЦИИ
# ==================


# Урок 8: Решение задачи от тимлида - Валидация email
def validate_email(email):
    if "@" in email and "." in email:
        return True
    else:
        return False


# Проверка всех email через функцию
email_1 = "ivan@example.com"
email_2 = "petr@test"
email_3 = "invalid-email"

result_1 = validate_email(email_1)
result_2 = validate_email(email_2)
result_3 = validate_email(email_3)

print("Email 1 валиден:", result_1)
print("Email 2 валиден:", result_2)
print("Email 3 валиден:", result_3)


# Практика: Задание 1 - Функция расчета цены со скидкой
def calculate_price_with_discount(price, discount_percent):
    final_price = price * (1 - discount_percent / 100)
    return final_price


# Вызов функции для разных товаров
price_1 = calculate_price_with_discount(1000, 10)
price_2 = calculate_price_with_discount(5000, 15)

print("Цена товара 1 со скидкой:", price_1)
print("Цена товара 2 со скидкой:", price_2)


# Практика: Задание 2 - Набор функций для работы с заказами
def calculate_order_total(price, quantity, discount):
    total = (price * quantity) * (1 - discount)
    return total


def check_stock_availability(stock_quantity, required_quantity):
    if stock_quantity >= required_quantity:
        return True
    else:
        return False


def format_order_info(order_id, total):
    info = "Заказ #" + str(order_id) + ", Сумма: " + str(total) + " руб."
    return info


# Использование функций вместе
stock_available = check_stock_availability(10, 3)
print("Товар доступен:", stock_available)

if stock_available:
    order_total = calculate_order_total(1000, 3, 0.1)
    order_info = format_order_info(1, order_total)
    print("Информация о заказе:", order_info)

# ==================
# УРОК 9: РАБОТА С ФАЙЛАМИ
# ==================

# Урок 9: Решение задачи от тимлида - Сохранение лога ошибок
error_message = "Ошибка: товар не найден на складе\n"

# Использование контекстного менеджера и режима 'a'
with open("data/errors.log", "a") as file:
    file.write(error_message)

# Практика: Задание 1 - Чтение и запись товаров
# Чтение товаров из файла
with open("data/products.txt", "r") as file:
    lines = file.readlines()

# Обработка товаров и запись в новый файл
with open("data/products_with_prices.txt", "w") as file:
    for line in lines:
        product = line.strip()  # Удаляем символ переноса строки
        product_with_price = product + " - 1000 руб.\n"
        file.write(product_with_price)

# Практика: Задание 2 - Обработка заказов из файла
try:
    # Чтение заказов из файла
    with open("data/orders.txt", "r") as file:
        lines = file.readlines()

    # Обработка заказов
    new_orders_count = 0
    new_orders_total = 0

    for line in lines:
        line = line.strip()  # Удаляем символ переноса строки
        if line:  # Пропускаем пустые строки
            # Находим позиции двоеточий через find()
            first_colon = line.find(":")
            second_colon = line.find(":", first_colon + 1)

            # Если найдены оба двоеточия, извлекаем части через срезы
            if first_colon != -1 and second_colon != -1:
                order_id = line[0:first_colon]
                order_sum = int(line[first_colon + 1 : second_colon])
                order_status = line[second_colon + 1 :]

                if order_status == "новый":
                    new_orders_count = new_orders_count + 1
                    new_orders_total = new_orders_total + order_sum

    # Запись результатов
    with open("data/processed_orders.txt", "w") as file:
        file.write("Обработано заказов: " + str(new_orders_count) + "\n")
        file.write("Общая сумма: " + str(new_orders_total) + " руб.\n")

    print("Обработка завершена")

except FileNotFoundError:
    print("Файл data/orders.txt не найден")

# ==================
# УРОК 10: ИМПОРТИРОВАНИЕ МОДУЛЕЙ, СОЗДАНИЕ СВОИХ МОДУЛЕЙ
# ==================

# Урок 10: Решение задачи от тимлида - Генерация промо-кода
import random

# Генерация случайного числа для промо-кода
promo_number = random.randint(100000, 999999)
promo_code = "PROMO" + str(promo_number)

print("Промо-код:", promo_code)

# Практика: Задание 1 - Создание модуля расчетов
# Импорт своего модуля
from src.utils.calculations import calculate_discount

discount_1 = calculate_discount(1000, 0.1)
discount_2 = calculate_discount(5000, 0.15)

print("Скидка для товара 1:", discount_1)
print("Скидка для товара 2:", discount_2)

# Практика: Задание 2 - Модульная структура проекта
# Импорт функций из модулей
from src.utils.calculations import (
    calculate_discount,
    calculate_delivery,
    calculate_final_price,
)
from src.utils.validators import validate_age, validate_email

# Валидация данных пользователя
age_valid = validate_age(20)
email_valid = validate_email("ivan@test.com")

print("Возраст валиден:", age_valid)
print("Email валиден:", email_valid)

# Расчет стоимости заказа
if age_valid and email_valid:
    price = 1000
    discount = calculate_discount(price, 0.1)
    delivery = calculate_delivery(5)
    final_price = calculate_final_price(price, discount, delivery)
    print("Итоговая стоимость заказа:", final_price, "руб.")

# ==================
# УРОК 11: ОБЛАСТИ ВИДИМОСТИ ПЕРЕМЕННЫХ
# ==================

# Урок 11: Решение задачи от тимлида - Использование глобальной константы
# Глобальная константа
BASE_DELIVERY_COST = 100


def calculate_order_total(price, quantity):
    # Используем глобальную константу в функции
    total = price * quantity + BASE_DELIVERY_COST
    return total


# Использование функции с глобальной константой
order_total = calculate_order_total(1000, 3)
print("Итоговая стоимость заказа:", order_total)

# Практика: Задание 1 - Работа с глобальными переменными
# Глобальная переменная
DISCOUNT_RATE = 0.1


def calculate_price_with_discount(price):
    final_price = price * (1 - DISCOUNT_RATE)
    return final_price


# Первый вызов
price_1 = calculate_price_with_discount(1000)
print("Цена со скидкой 10%:", price_1)

# Изменение глобальной переменной
DISCOUNT_RATE = 0.2

# Второй вызов
price_2 = calculate_price_with_discount(1000)
print("Цена со скидкой 20%:", price_2)

# Практика: Задание 2 - Система настроек приложения
# Глобальные константы
BASE_DISCOUNT = 0.1
BASE_DELIVERY_COST = 100


def calculate_order_price(price, quantity):
    # Локальные переменные
    subtotal = price * quantity
    discount = subtotal * BASE_DISCOUNT  # Используем глобальную константу
    total = subtotal - discount + BASE_DELIVERY_COST  # Используем глобальную константу
    return total


def update_discount(new_discount):
    global BASE_DISCOUNT  # Указываем, что изменяем глобальную переменную
    BASE_DISCOUNT = new_discount


# Расчет с базовой скидкой
price_1 = calculate_order_price(1000, 2)
print("Стоимость заказа (скидка 10%):", price_1)

# Изменение скидки через функцию с global
update_discount(0.15)

# Расчет с новой скидкой
price_2 = calculate_order_price(1000, 2)
print("Стоимость заказа (скидка 15%):", price_2)

# ==================
# УРОК 12: F-СТРОКИ (F-STRINGS) И МЕТОДЫ СТРОК
# ==================

# Урок 12: Решение задачи от тимлида - Форматирование сообщения для лога
# Данные заказа
order_id = 123
order_total = 5000
order_status = "новый"

# Использование f-строки вместо сложной конкатенации
log_message = f"Заказ #{order_id}, Сумма: {order_total} руб., Статус: {order_status}"
print(log_message)


# Практика: Задание 1 - Форматирование информации о товаре
def format_product_info(name, price, quantity):
    info = f"Товар: {name}, Цена: {price} руб., Количество: {quantity}"
    return info


# Использование функции
product_info = format_product_info("Ноутбук", 50000, 10)
print("Информация о товаре:", product_info)

# Обработка списка товаров
products = ["Ноутбук", "Мышь", "Клавиатура"]
products_string = ", ".join(products)
print(f"Товары: {products_string}")

# ==================
# УРОК 13: РАБОТА С ДАТАМИ И ВРЕМЕНЕМ
# ==================

# Урок 13: Решение задачи от тимлида - Расчет срока доставки
from datetime import datetime, timedelta

# Данные заказа
order_date = datetime(2024, 1, 15, 10, 0, 0)
delivery_days = 3

# Расчет даты доставки
delivery_date = order_date + timedelta(days=delivery_days)
print("Дата заказа:", order_date)
print("Дата доставки:", delivery_date)

# Практика: Задание 1 - Работа с датами
# Текущая дата и время
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print("Текущее время:", formatted_time)

# Даты заказа и доставки
order_date = datetime(2024, 1, 15, 10, 0, 0)
delivery_date = datetime(2024, 1, 18, 10, 0, 0)

print("Дата заказа:", order_date.strftime("%Y-%m-%d %H:%M:%S"))
print("Дата доставки:", delivery_date.strftime("%Y-%m-%d %H:%M:%S"))

# Разница между датами
difference = delivery_date - order_date
days = difference.days
print("Дней до доставки:", days)


# Практика: Задание 2 - Система расчета сроков доставки
def calculate_delivery_date(order_date, delivery_days):
    delivery_date = order_date + timedelta(days=delivery_days)
    return delivery_date


def log_order_creation(order_id, order_time):
    formatted_time = order_time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = "Заказ #" + str(order_id) + " создан: " + formatted_time
    return log_message


# Использование функций
order_date = datetime(2024, 1, 15, 10, 0, 0)
delivery_date = calculate_delivery_date(order_date, 3)
print("Дата доставки:", delivery_date)

order_time = datetime.now()
log = log_order_creation(123, order_time)
print(log)

# ==================
# УРОК 14: РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ (REGEX)
# ==================

# Урок 14: Решение задачи от тимлида - Валидация email и телефона
import re


def validate_email(email):
    pattern = r".+@.+\..+"
    result = re.match(pattern, email)
    return result is not None


def validate_phone(phone):
    pattern = r"\+7[\s\d-]+"
    result = re.match(pattern, phone)
    return result is not None


# Данные пользователя
email = "ivan@example.com"
phone = "+7 999 123-45-67"

print("Email валиден:", validate_email(email))
print("Телефон валиден:", validate_phone(phone))


# Практика: Задание 1 - Валидация email через регулярное выражение
def validate_email_regex(email):
    pattern = r".+@.+\..+"
    return re.match(pattern, email) is not None


email_1 = "test@example.com"
email_2 = "invalid-email"

print("Email 1 валиден:", validate_email_regex(email_1))
print("Email 2 валиден:", validate_email_regex(email_2))


# Практика: Задание 2 - Система валидации данных пользователя
def validate_phone_regex(phone):
    pattern = r"\+7[\s\d-]+"
    return re.match(pattern, phone) is not None


def clean_user_input(text):
    # Удаляем все кроме букв, цифр, пробелов и основных символов
    cleaned = re.sub(r"[^\w\s@.-]", "", text)
    return cleaned


def extract_email_from_text(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    result = re.search(pattern, text)
    if result:
        return result.group()
    return None


# Валидация данных
email = "ivan@test.com"
phone = "+7 999 123-45-67"

email_valid = validate_email_regex(email)
phone_valid = validate_phone_regex(phone)

print("Email валиден:", email_valid)
print("Телефон валиден:", phone_valid)

# Очистка пользовательского ввода
user_input = "Заказ #123, сумма 5000 руб.!"
cleaned = clean_user_input(user_input)
print("Очищенный ввод:", cleaned)

# Извлечение email из текста
text_with_email = "Свяжитесь с нами по адресу support@example.com для помощи"
extracted_email = extract_email_from_text(text_with_email)
print("Извлеченный email:", extracted_email)

# ==================
# УРОК 15: КЛАССЫ
# ==================

# Урок 15: Решение задачи от тимлида - Рефакторинг кода через классы
# Импорт классов из модулей
from src.models.product import Product
from src.models.user import User
from src.models.order import Order

# Создание объекта товара
laptop = Product("Ноутбук", 50000, 10)
total_price = laptop.get_total_price()
print("Общая стоимость товара:", total_price)

# Практика: Задание 1 - Создание класса Product
# Класс Product уже создан в src/models/product.py
# Создание объекта и использование
laptop = Product("Ноутбук", 50000, 10)
total = laptop.get_total_price()
print("Общая стоимость товара:", total)

# Практика: Задание 2 - Создание классов Product, User, Order
# Создание пользователя
user = User("Иван Иванов", "ivan@test.com")
print(user.get_info())

# Создание товаров
laptop = Product("Ноутбук", 50000, 1)
mouse = Product("Мышь", 1500, 2)

# Создание заказа
order = Order(user, [laptop, mouse])
total = order.calculate_total()
print("Общая стоимость заказа:", total)

# ==================
# УРОК 16: ПРИНЦИПЫ ООП (НАСЛЕДОВАНИЕ, ИНКАПСУЛЯЦИЯ, ПОЛИМОРФИЗМ)
# ==================

# Урок 16: Решение задачи от тимлида - Система платежей
from src.models.payment import Payment, CardPayment, PayPalPayment

# Создание платежей разных типов
card_payment = CardPayment(1000, "1234 5678 9012 3456")
paypal_payment = PayPalPayment(2000, "user@paypal.com")

# Полиморфизм - единый интерфейс для разных типов
payments = [card_payment, paypal_payment]
for payment in payments:
    print(payment.process_payment())


# Практика: Задание 1 - Наследование
class Animal:
    def make_sound(self):
        return "Звук животного"


class Dog(Animal):
    def make_sound(self):
        return "Гав-гав"


class Cat(Animal):
    def make_sound(self):
        return "Мяу"


# Создание объектов
dog = Dog()
cat = Cat()

# Вызов методов
print(dog.make_sound())
print(cat.make_sound())

# Практика: Задание 2 - Система платежей
# Базовый класс Payment уже создан в src/models/payment.py
# Классы CardPayment и PayPalPayment уже созданы

# Демонстрация полиморфизма
card_payment = CardPayment(1000, "1234 5678 9012 3456")
paypal_payment = PayPalPayment(2000, "user@paypal.com")

# Обработка разных типов платежей через единый интерфейс
payments = [card_payment, paypal_payment]
for payment in payments:
    print(payment.process_payment())

# ==================
# УРОК 30: ПРОДВИНУТЫЕ ОСНОВЫ PYTHON
# ==================

# Урок 30: Решение задачи от тимлида - Оптимизация кода


# Измерение производительности
def measure_performance(func, *args, **kwargs):
    """Измерить время выполнения функции"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Функция {func.__name__} выполнилась за {execution_time:.4f} секунд")
    return result, execution_time


# Практика: Задание 1 - Оптимизация функции обработки данных
# Исходная функция (медленная)
def calculate_total_orders_slow(orders):
    """Медленный подход с вложенными циклами"""
    total = 0
    for order in orders:
        for item in order.items:
            total += item.price * item.quantity
    return total


# Оптимизированная функция (быстрая)
def calculate_total_orders_fast(orders):
    """Быстрый подход с генератором"""
    return sum(item.price * item.quantity for order in orders for item in order.items)


# Практика: Задание 2 - Оптимизация поиска в данных
# Поиск в списке (медленный, O(n))
def find_product_in_list(products, product_id):
    """Поиск в списке (медленный)"""
    for product in products:
        if product.id == product_id:
            return product
    return None


# Поиск в словаре (быстрый, O(1))
def create_products_index(products):
    """Создать словарь для быстрого поиска"""
    return {product.id: product for product in products}


def find_product_in_dict(products_dict, product_id):
    """Поиск в словаре (быстрый)"""
    return products_dict.get(product_id)


# ==================
# УРОК 31: ОБЗОРНО И БАЗОВО ПРО АЛГОРИТМЫ
# ==================

# Урок 31: Решение задачи от тимлида - Поиск товара в большом каталоге
import time


class Product:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def linear_search(products, product_id):
    """Линейный поиск в списке (O(n))"""
    for product in products:
        if product.id == product_id:
            return product
    return None


def dict_search(products_dict, product_id):
    """Поиск в словаре (O(1))"""
    return products_dict.get(product_id)


def compare_search_methods():
    """Сравнить время поиска в списке vs словаре"""
    # Создать большой список товаров
    products = [Product(i, f"Товар {i}") for i in range(10000)]

    # Создать словарь из списка
    products_dict = {product.id: product for product in products}

    # Искать товар с ID 5000
    product_id = 5000

    # Измерить время поиска в списке
    start_time = time.time()
    result_list = linear_search(products, product_id)
    list_time = time.time() - start_time

    # Измерить время поиска в словаре
    start_time = time.time()
    result_dict = dict_search(products_dict, product_id)
    dict_time = time.time() - start_time

    print(f"Поиск в списке: {list_time:.6f} секунд")
    print(f"Поиск в словаре: {dict_time:.6f} секунд")
    print(f"Ускорение: {list_time / dict_time:.2f}x")


# Практика: Задание 1 - Сравнение времени поиска
compare_search_methods()

# Практика: Задание 2 - Выбор правильной структуры данных
# Создание индекса для быстрого поиска
products = [Product(i, f"Товар {i}") for i in range(1000)]
products_index = {product.id: product for product in products}


# Быстрый поиск по ID
def find_product_fast(product_id):
    return products_index.get(product_id)


# Сортировка заказов по дате
class Order:
    def __init__(self, id, total, created_at):
        self.id = id
        self.total = total
        self.created_at = created_at


orders = [
    Order(1, 5000, "2024-01-15"),
    Order(2, 3000, "2024-01-10"),
    Order(3, 8000, "2024-01-20"),
]

# Сортировка по дате
sorted_orders = sorted(orders, key=lambda x: x.created_at)
print("Заказы отсортированы по дате")

# Сортировка по сумме (по убыванию)
sorted_orders_by_total = sorted(orders, key=lambda x: x.total, reverse=True)
print("Заказы отсортированы по сумме")
