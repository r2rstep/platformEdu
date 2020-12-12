from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate, User
from app.tests.utils.utils import random_lower_string, random_name


@pytest.fixture(scope='module')
def username() -> str:
    yield random_name()


@pytest.fixture(scope='module')
def created_user(client: TestClient, username: str, superuser_token_headers: dict, db: Session) -> User:
    password = random_lower_string()
    create_data = UserCreate(name=username, password=password)
    resp = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=create_data.dict(),
    )
    assert 200 <= resp.status_code < 300
    created_user_ = User(**resp.json())
    yield created_user_
    if crud.user.get(db, id=created_user_.id):
        crud.user.remove(db, id=created_user_.id)


def test_create_new_user(client: TestClient, db: Session, created_user: User, username: str) -> None:
    user = crud.user.get_by_name(db, name=username)
    assert user
    assert user.name == created_user.name


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_name()
    password = random_lower_string()
    user_in = UserCreate(name=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_name(db, name=username)
    assert existing_user
    assert existing_user.name == api_user["name"]


def test_create_user_existing_username(
    client: TestClient, db: Session
) -> None:
    name = random_name()
    password = random_lower_string()
    user_in = UserCreate(name=name, password=password)
    crud.user.create(db, obj_in=user_in)
    r = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict(),
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_name()
    password = random_lower_string()
    user_in = UserCreate(name=username, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_name()
    password2 = random_lower_string()
    user_in2 = UserCreate(name=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for lecture in all_users:
        assert "name" in lecture
