from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app import crud
from app.schemas.lecture import LectureCreate, LectureUpdate, LectureInDB
from app.schemas.user import UserInDB
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


@pytest.fixture(scope='module')
def user(db: Session) -> UserInDB:
    user = create_random_user(db)
    yield user
    crud.user.remove(db, id=user.id)


@pytest.fixture(scope='module')
def lecture(db: Session, user: UserInDB) -> LectureCreate:
    title = random_lower_string()
    content = random_lower_string()
    new_lecture_ = LectureCreate(title=title, content=content, author_id=user.id, uploaded_at=datetime.utcnow(),
                                 slug=random_lower_string())
    yield new_lecture_


@pytest.fixture(scope='module')
def lecture_in_db(db: Session, lecture: LectureCreate) -> LectureInDB:
    lecture_in_db = crud.lecture.create(db=db, obj_in=lecture)
    yield lecture_in_db
    if crud.lecture.get(db=db, id=lecture_in_db.id):
        crud.lecture.remove(db, id=lecture_in_db.id)


def test_create_lecture(db: Session, lecture_in_db: LectureInDB, lecture: LectureCreate, user) -> None:
    assert lecture_in_db.title == lecture.title
    assert lecture_in_db.content == lecture.content
    assert lecture_in_db.author_id == user.id


def test_get_lecture(db: Session, lecture_in_db: LectureInDB) -> None:
    stored_lecture = crud.lecture.get(db=db, id=lecture_in_db.id)
    assert stored_lecture
    assert lecture_in_db.id == stored_lecture.id
    assert lecture_in_db.title == stored_lecture.title
    assert lecture_in_db.content == stored_lecture.content
    assert lecture_in_db.author_id == stored_lecture.author_id


def test_update_lecture(db: Session, lecture_in_db: LectureInDB) -> None:
    description2 = random_lower_string()
    lecture_update = LectureUpdate(content=description2)
    lecture2 = crud.lecture.update(db=db, db_obj=lecture_in_db, obj_in=lecture_update)
    updated_lecture = crud.lecture.get(db=db, id=lecture_in_db.id)
    assert lecture_in_db.id == lecture2.id
    assert lecture_in_db.title == lecture2.title
    assert updated_lecture.content == description2
    assert lecture_in_db.author_id == lecture2.author_id


def test_delete_lecture(db: Session, lecture_in_db: LectureInDB) -> None:
    lecture2 = crud.lecture.remove(db=db, id=lecture_in_db.id)
    lecture3 = crud.lecture.get(db=db, id=lecture_in_db.id)
    assert lecture3 is None
    assert lecture2.id == lecture_in_db.id
