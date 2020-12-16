from pydantic import UUID4
from sqlalchemy.orm import Session

from app import crud
from app.db.session import SessionLocal
from app.schemas import UserCreate, LectureCreate, ReviewCreate


def process(batch_data: dict):
    _process_lectures(batch_data['lectures'])


def _process_lectures(lectures_batch_data: list):
    db = SessionLocal()
    lectures_types = crud.lecture_type.get_multi(db, limit=crud.lecture_type.count(db))
    for lecture in lectures_batch_data:
        author = crud.user.get_by_name(db, name=lecture['author']['name'])
        if author:
            author_id = author.id
        else:
            author_id = _create_author(db, author_data=lecture['author'])
        lecture_type_id = [l_type.id for l_type in lectures_types if l_type.name == lecture['type']].pop()
        lecture_id = _create_lecture(db,
                                     lecture_data=lecture,
                                     author_id=author_id,
                                     lecture_type_id=lecture_type_id)
        _create_reviews(db, reviews_batch_data=lecture['reviews'], lecture_id=lecture_id)


def _create_author(db: Session, *, author_data: dict) -> UUID4:
    return crud.user.create(db, obj_in=UserCreate(**author_data,
                                                  password='')).id


def _create_lecture(db: Session, *, lecture_data: dict, author_id: UUID4, lecture_type_id: int) -> UUID4:
    return crud.lecture.create_with_author(db,
                                           obj_in=LectureCreate(**lecture_data,
                                                                type_id=lecture_type_id),
                                           author_id=author_id).id


def _create_reviews(db: Session, *, reviews_batch_data: list, lecture_id: UUID4):
    for review in reviews_batch_data:
        crud.review.create(db, obj_in=ReviewCreate(**review, lecture_id=lecture_id))
