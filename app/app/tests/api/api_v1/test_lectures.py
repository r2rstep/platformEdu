from typing import List

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud
from app.schemas.user import User
from app.schemas.lecture import LectureCreate, Lecture, Lectures
from app.tests.utils.lecture import create_random_lecture


@pytest.fixture
def superuser(db: Session) -> User:
    yield crud.user.get_by_name(db, name=settings.FIRST_SUPERUSER)


@pytest.fixture(autouse=True)
def testcase_teardown(db: Session):
    crud.lecture.remove_all(db)
    yield


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


def test_get_all_lectures(client: TestClient, db: Session):
    num_lectures = 20
    lectures_in_db: List[Lecture] = []
    for _ in range(0, num_lectures):
        lectures_in_db.append(create_random_lecture(db))
    response = client.get(
        f"{settings.API_V1_STR}/lectures"
    )
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    _check_lectures_response(lectures_in_db, num_lectures, num_lectures, lectures)


def test_get_lectures_paginated(client: TestClient, db: Session):
    num_lectures = 21
    limit = 10
    lectures_in_db: List[Lecture] = []
    for _ in range(0, num_lectures):
        lectures_in_db.append(create_random_lecture(db))
    response = client.get(
        f"{settings.API_V1_STR}/lectures?limit={limit}"
    )
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    _check_lectures_response(lectures_in_db[:limit],
                             limit,
                             num_lectures,
                             lectures)
    first_page_lectures_ids = set(lec.id for lec in lectures.items)

    response = client.get(lectures.links.next)
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    _check_lectures_response(lectures_in_db[limit:20], limit, num_lectures, lectures)

    response = client.get(lectures.links.previous)
    lectures = Lectures(**response.json())
    assert set(lec.id for lec in lectures.items) == first_page_lectures_ids


def _check_lectures_response(lectures_in_db, limit, num_lectures, response):
    assert response.total == num_lectures
    assert response.count == limit
    lectures_ids = set(lec.id for lec in response.items)
    assert len(lectures_ids) == limit
    assert lectures_ids == set(lec.id for lec in lectures_in_db)
    return lectures_ids
