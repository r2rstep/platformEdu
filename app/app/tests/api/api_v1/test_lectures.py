from datetime import datetime

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud
from app.schemas.user import User
from app.schemas.lecture import LectureCreate, Lecture
from app.tests.utils.lecture import create_random_lecture


@pytest.fixture
def superuser(db: Session) -> User:
    yield crud.user.get_by_name(db, name=settings.FIRST_SUPERUSER)


def test_create_lecture(
    client: TestClient, superuser_token_headers: dict, db: Session, superuser: User
) -> None:
    new_lecture = LectureCreate(title='New Lecture')
    response = client.post(
        f"{settings.API_V1_STR}/lectures/", headers=superuser_token_headers, json=new_lecture.dict(),
    )
    assert response.status_code == 200
    created_lecture = Lecture(**response.json())
    assert created_lecture.title == new_lecture.title
    assert created_lecture.author_id == superuser.id


def test_get_lecture(
    client: TestClient, db: Session
) -> None:
    lecture = create_random_lecture(db)
    response = client.get(
        f"{settings.API_V1_STR}/lectures/{lecture.id}"
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == lecture.title
    assert content["content"] == lecture.content
    assert content["id"] == str(lecture.id)
    assert content["author_id"] == str(lecture.author_id)
