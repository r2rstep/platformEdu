from typing import List
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud
from app.schemas.user import User
from app.schemas.lecture import LectureCreate, Lecture, Lectures
from app.tests.utils.user import create_random_user
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


@pytest.fixture(scope='module')
def authors(db: Session) -> User:
    crud.user.remove_all(db, leave_superusers=True)
    yield [create_random_user(db) for _ in range(0, 3)]


@pytest.fixture(scope='module')
def lectures_in_db(db: Session, authors: List[User]):
    crud.lecture.remove_all(db)
    num_lectures = 21
    lectures_in_db_: List[Lecture] = []
    for lec_index in range(0, num_lectures):
        lectures_in_db_.append(create_random_lecture(db, author_id=authors[lec_index % len(authors)].id))
    yield lectures_in_db_


def test_get_lecture(client: TestClient, lectures_in_db: List[Lecture]) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/lectures/{lectures_in_db[1].id}"
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == lectures_in_db[1].title
    assert content["content"] == lectures_in_db[1].content
    assert content["id"] == str(lectures_in_db[1].id)
    assert content["author_id"] == str(lectures_in_db[1].author_id)


def test_get_all_lectures(client: TestClient, lectures_in_db: List[Lecture]):
    response = client.get(
        f"{settings.API_V1_STR}/lectures"
    )
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    _check_lectures_response(lectures_in_db, len(lectures_in_db), len(lectures_in_db), lectures)


def test_get_lectures_paginated(client: TestClient, lectures_in_db: List[Lecture]):
    limit = 10
    response = client.get(
        f"{settings.API_V1_STR}/lectures?limit={limit}"
    )
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    _check_lectures_response(lectures_in_db[:limit],
                             limit,
                             len(lectures_in_db),
                             lectures)
    first_page_lectures_ids = set(lec.id for lec in lectures.items)

    response = client.get(lectures.links.next)
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    _check_lectures_response(lectures_in_db[limit:20], limit, len(lectures_in_db), lectures)

    response = client.get(lectures.links.previous)
    lectures = Lectures(**response.json())
    assert set(lec.id for lec in lectures.items) == first_page_lectures_ids


def test_get_lectures_incorrect_filter(client: TestClient):
    response = client.get(
        f"{settings.API_V1_STR}/lectures?filter[incorrect_field]={uuid4()}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.get(
        f"{settings.API_V1_STR}/lectures?filter[author_id]=not_uuid"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_lectures_by_author(client: TestClient, lectures_in_db: List[Lecture], authors: List[User]):
    requested_author_id = authors[1].id
    response = client.get(
        f"{settings.API_V1_STR}/lectures?filter[author_id]={requested_author_id}"
    )
    assert response.status_code == 200
    lectures = Lectures(**response.json())
    requested_author_lectures = [lec for lec in lectures_in_db if lec.author_id == requested_author_id]
    _check_lectures_response(requested_author_lectures,
                             len(requested_author_lectures),
                             len(requested_author_lectures),
                             lectures)


def _check_lectures_response(lectures_in_db, limit, num_lectures, response):
    assert response.total == num_lectures
    assert response.count == limit
    lectures_ids = set(lec.id for lec in response.items)
    assert len(lectures_ids) == limit
    assert lectures_ids == set(lec.id for lec in lectures_in_db)
    return lectures_ids
