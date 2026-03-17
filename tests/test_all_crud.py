import asyncio
import sys
from decimal import Decimal

from src.database.connection import init_pool, close_pool, get_connection
from src.database.queries.orders import (
    create_order,
    get_order_by_id,
    get_orders_by_user_id,
    update_order,
    delete_order,
)
from src.database.queries.products import (
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product,
)
from src.database.queries.users import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
)
from src.models import (
    UserUpdate,
    UserCreate,
    ProductUpdate,
    ProductCreate,
    OrderCreate,
    OrderUpdate,
)


async def test_all_crud():
    """Тестирует все CRUD-функции."""
    print("🧪 Starting ALL CRUD tests...\n")

    try:
        await init_pool()
        print("✅ Database pool initialized\n")

        # 🆕 ДОБАВИТЬ: Очистка тестовых данных перед запуском
        print("🧹 Cleaning test data...")
        await _cleanup_test_data()
        print("✅ Cleaned\n")

        # ========== USERS ==========
        print("=" * 50)
        print("👤 USERS CRUD TESTS")
        print("=" * 50)

        # CREATE
        print("\n📝 CREATE user")
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            password_hash="$2b$12$examplehash",
            first_name="Иван",
            last_name="Иванов",
        )
        user = await create_user(user_in)
        print(f"   Created: id={user.id}, email={user.email}")
        user_id = user.id

        # GET
        print("\n📝 GET user by ID")
        user = await get_user_by_id(user_id)
        print(f"   Found: {user.username}")

        # GET ALL
        print("\n📝 GET all users")
        users = await get_all_users(skip=0, limit=10)
        print(f"   Total users: {len(users)}")

        # UPDATE
        print("\n📝 UPDATE user")
        user_update = UserUpdate(first_name="Пётр")
        updated = await update_user(user_id, user_update)
        print(f"   Updated first_name: {updated.first_name}")

        # ========== PRODUCTS ==========
        print("\n" + "=" * 50)
        print("📦 PRODUCTS CRUD TESTS")
        print("=" * 50)

        # CREATE
        print("\n📝 CREATE product")
        product_create = ProductCreate(
            name="Тестовый товар",
            price=Decimal("999.99"),
            description="Описание товара",
            sku="TEST-001",
            stock_quantity=100,
        )
        product = await create_product(product_create)
        print(f"   Created: id={product.id}, name={product.name}")
        product_id = product.id

        # GET
        print("\n📝 GET product by ID")
        product = await get_product_by_id(product_id)
        print(f"   Found: {product.name}, price={product.price}")

        # GET ALL
        print("\n📝 GET all products")
        products = await get_all_products(skip=0, limit=10)
        print(f"   Total products: {len(products)}")

        # UPDATE
        print("\n📝 UPDATE product")
        product_update = ProductUpdate(price=Decimal("899.99"))
        updated = await update_product(product_id, product_update)
        print(f"   Updated price: {updated.price}")

        # ========== ORDERS ==========
        print("\n" + "=" * 50)
        print("🛒 ORDERS CRUD TESTS")
        print("=" * 50)

        # CREATE
        print("\n📝 CREATE order")
        order_create = OrderCreate(
            user_id=user_id,
            total_amount=Decimal("1999.98"),
            shipping_address="г. Москва, ул. Тестовая, д. 1",
            status="pending",
        )
        order = await create_order(order_create)
        print(f"   Created: id={order.id}, status={order.status}")
        order_id = order.id

        # GET
        print("\n📝 GET order by ID")
        order = await get_order_by_id(order_id)
        print(f"   Found: order #{order.id}, amount={order.total_amount}")

        # GET BY USER
        print("\n📝 GET orders by user ID")
        orders = await get_orders_by_user_id(user_id, skip=0, limit=10)
        print(f"   User's orders: {len(orders)}")

        # UPDATE
        print("\n📝 UPDATE order")
        order_update = OrderUpdate(status="confirmed")
        updated = await update_order(order_id, order_update)
        print(f"   Updated status: {updated.status}")

        # ========== CLEANUP ==========
        print("\n" + "=" * 50)
        print("🧹 CLEANUP (DELETE)")
        print("=" * 50)

        # DELETE order
        print("\n📝 DELETE order")
        deleted = await delete_order(order_id)
        print(f"   Order deleted: {deleted}")

        # DELETE product
        print("\n📝 DELETE product")
        deleted = await delete_product(product_id)
        print(f"   Product deleted: {deleted}")

        # DELETE user (CASCADE удалит заказы)
        print("\n📝 DELETE user")
        deleted = await delete_user(user_id)
        print(f"   User deleted: {deleted}")

        # VERIFY
        print("\n📝 VERIFY deletion")
        user = await get_user_by_id(user_id)
        print(f"   User after delete: {user} (должно быть None)")

        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"\n💥 TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        await close_pool()


async def _cleanup_test_data():
    """
    Удаляет тестовые данные перед запуском тестов.
    🔹 Важно: сначала orders, потом products, потом users (из-за FOREIGN KEY)
    """
    async with get_connection() as conn:
        # Сначала удаляем заказы (зависят от users)
        await conn.execute(
            "DELETE FROM orders WHERE shipping_address LIKE '%Тестовая%'"
        )

        # Потом товары (независимы, но на всякий случай)
        await conn.execute("DELETE FROM products WHERE sku LIKE 'TEST-%'")

        # Потом пользователей
        await conn.execute("DELETE FROM users WHERE email = 'test@example.com'")

        # Сбрасываем счётчики ID (опционально, чтобы ID начинались с 1)
        # await conn.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")
        # await conn.execute("ALTER SEQUENCE products_id_seq RESTART WITH 1")
        # await conn.execute("ALTER SEQUENCE orders_id_seq RESTART WITH 1")


if __name__ == "__main__":
    success = asyncio.run(test_all_crud())
    sys.exit(0 if success else 1)
