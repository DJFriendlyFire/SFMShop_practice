from datetime import datetime, UTC
from unittest.mock import AsyncMock, patch, ANY

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.api import auth
from src.api.routes.users import router as users_routes
from src.database.dependencies import get_db_pool
from src.models.user import UserResponse


class DummyAcquire:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


class DummyPool:
    def __init__(self, conn=None):
        self.conn = conn or object()

    def acquire(self):
        return DummyAcquire(self.conn)


@pytest.fixture
def app():
    app = FastAPI()

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request.state.request_id = "test-request-id"
        return await call_next(request)

    app.include_router(users_routes, prefix="/users", tags=["Users"])
    return app


@pytest.fixture
def user_response_model():
    return UserResponse(
        id=1,
        email="my_email@email.com",
        username="my_username",
        first_name=None,
        last_name=None,
        is_active=True,
        is_verified=True,
        created_at=datetime(2024, 1, 1, 12, 0, tzinfo=UTC),
        updated_at=datetime(2024, 1, 2, 12, 0, tzinfo=UTC),
    )


@pytest.fixture
def set_current_user(app: FastAPI):
    def _set(user_id: int = 1):
        app.dependency_overrides[auth.get_current_user] = lambda: {"user_id": user_id}

    _set()
    return _set


@pytest.fixture
def set_pool(app: FastAPI):
    def _set(pool=None):
        app.dependency_overrides[get_db_pool] = lambda: pool or DummyPool()

    _set()
    return _set


@pytest.fixture
def client(app, set_current_user, set_pool):
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def user_create_payload():
    return {
        "email": "my_email@email.com",
        "username": "my_username",
        "password_hash": "hash-password",
    }


@pytest.fixture
def user_update_payload():
    return {
        "email": "new_my_email@email.com",
        "first_name": "Test_name",
        "last_name": "Test_lastname",
    }


@pytest.fixture
def user_response_data():
    return {
        "id": 1,
        "email": "my_email@email.com",
        "username": "my_username",
        "first_name": None,
        "last_name": None,
        "is_active": True,
        "is_verified": True,
    }


def test_create_user_success(client, user_create_payload, user_response_model):
    with patch(
        "src.api.routes.users.auth.get_password_hash",
        return_value="hash-password",
    ) as hash_mock, patch(
        "src.api.routes.users.create_user_with_conn",
        new=AsyncMock(return_value=user_response_model),
    ) as create_mock:
        response = client.post("/users/", json=user_create_payload)

    assert response.status_code == 201
    assert response.json()["id"] == user_response_model.id
    assert response.json()["email"] == user_response_model.email
    assert response.json()["username"] == user_response_model.username

    hash_mock.assert_called_once_with("hash-password")
    create_mock.assert_awaited_once()


def test_create_user_unique_violation_returns_400(client, user_create_payload):
    with patch(
        "src.api.routes.users.auth.get_password_hash", return_value="hash-password"
    ), patch(
        "src.api.routes.users.create_user_with_conn",
        new=AsyncMock(side_effect=Exception("unique_violation")),
    ):

        response = client.post("/users/", json=user_create_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email or username already exists"


def test_create_user_returns_500_when_query_returns_none(client, user_create_payload):
    with patch(
        "src.api.routes.users.auth.get_password_hash", return_value="hashed_pass"
    ), patch(
        "src.api.routes.users.create_user_with_conn", new=AsyncMock(return_value=None)
    ):

        response = client.post("/users/", json=user_create_payload)

        assert response.status_code == 500
        assert response.json()["detail"] == "Ошибка создания пользователя"


def test_get_my_profile_success(client, user_response_model):
    with patch(
        "src.api.routes.users.get_user_by_id_with_conn",
        new=AsyncMock(return_value=user_response_model),
    ) as get_mock:

        response = client.get("/users/me")

        assert response.status_code == 200
        assert response.json()["id"] == user_response_model.id
        assert response.json()["username"] == user_response_model.username
        get_mock.assert_awaited_once_with(1, ANY)


@pytest.mark.parametrize(
    "returned_user, expected_status, expected_detail",
    [
        ("user_response_model", 200, None),
        (None, 404, "Пользователь не найден"),
    ],
)
def test_get_user_by_id(
    client, request, returned_user, expected_status, expected_detail
):
    if returned_user == "user_response_model":
        returned_user = request.getfixturevalue("user_response_model")

    with patch(
        "src.api.routes.users.get_user_by_id_with_conn",
        new=AsyncMock(return_value=returned_user),
    ) as mock_get_user:
        response = client.get("/users/1")

    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json()["id"] == returned_user.id
        assert response.json()["email"] == returned_user.email
        assert response.json()["username"] == returned_user.username
        mock_get_user.assert_awaited_once_with(1, ANY)
    else:
        assert response.json()["detail"] == expected_detail
        mock_get_user.assert_awaited_once_with(1, ANY)


@pytest.mark.parametrize(
    "skip, limit",
    [
        (0, 10),
        (10, 5),
        (20, 20),
    ],
)
def test_get_all_users_success(client, skip, limit, user_response_model):
    first_user = user_response_model.model_copy()
    second_user = user_response_model.model_copy(
        update={
            "id": 2,
            "email": "my_email2@email.com",
            "username": "my_username2",
            "first_name": None,
            "last_name": None,
            "is_active": True,
            "is_verified": True,
            "created_at": datetime(2024, 1, 1, 12, 0, tzinfo=UTC),
            "updated_at": datetime(2024, 1, 2, 12, 0, tzinfo=UTC),
        }
    )

    users = [first_user, second_user]

    with patch(
        "src.api.routes.users.get_all_users_with_conn",
        new=AsyncMock(return_value=users),
    ) as get_all_mock:
        response = client.get(f"/users/?skip={skip}&limit={limit}")

        assert response.status_code == 200
        response_date = response.json()

        assert len(response_date) == 2
        assert response_date[0]["id"] == 1
        assert response_date[0]["username"] == "my_username"

        assert response_date[1]["id"] == 2
        assert response_date[1]["username"] == "my_username2"

        get_all_mock.assert_awaited_once_with(conn=ANY, skip=skip, limit=limit)


def test_update_user_forbidden_for_another_user(client, app, user_update_payload):
    app.dependency_overrides[auth.get_current_user] = lambda: {"user_id": 999}

    response = client.patch("/users/1", json=user_update_payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Нет прав на обновление другого пользователя"


def test_update_user_not_found(client, user_update_payload):
    with patch(
        "src.api.routes.users.update_user_with_conn",
        new=AsyncMock(return_value=None),
    ):
        response = client.patch("/users/1", json=user_update_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Юзер с ID=1 не найден"


def test_update_user_success(client, user_response_model):
    update_user_payload = {
        "email": "my_NEW_email@email.com",
        "username": "my_NEW_username",
        "first_name": "Ivan",
        "last_name": "Тульский",
        "is_active": False,
    }

    update_user_model = user_response_model.model_copy(
        update={
            "email": "my_NEW_email@email.com",
            "username": "my_NEW_username",
            "first_name": "Ivan",
            "last_name": "Тульский",
            "is_active": False,
        }
    )

    with patch(
        "src.api.routes.users.update_user_with_conn",
        new=AsyncMock(return_value=update_user_model),
    ) as update_mock:
        response = client.patch("/users/1", json=update_user_payload)

        assert response.status_code == 200
        assert response.json()["email"] == update_user_model.email
        assert response.json()["first_name"] == update_user_model.first_name

        update_mock.assert_awaited_once_with(1, ANY, ANY)


def test_delete_user_forbidden_for_another_user(client, app):
    app.dependency_overrides[auth.get_current_user] = lambda: {"user_id": 999}

    response = client.delete("/users/1")

    assert response.status_code == 403
    assert response.json()["detail"] == "Нет прав на удаление другого пользователя"


def test_delete_user_not_found(client):
    with patch(
        "src.api.routes.users.delete_user_with_conn",
        new=AsyncMock(return_value=False),
    ):
        response = client.delete("/users/1")

        assert response.status_code == 404
        assert response.json()["detail"] == "Юзер с ID=1 не найден"


def test_delete_user_success(client):
    with patch(
        "src.api.routes.users.delete_user_with_conn",
        new=AsyncMock(return_value=True),
    ) as delete_mock:
        response = client.delete("/users/1")

        assert response.status_code == 204
        assert response.content == b""
        delete_mock.assert_awaited_once_with(1, ANY)
