from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lecture import Lecture
from app.schemas.lecture import LectureCreate, LectureUpdate


class CRUDLecture(CRUDBase[Lecture, LectureCreate, LectureUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: LectureCreate, author_id: int
    ) -> Lecture:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Lecture]:
        return (
            db.query(self.model)
            .filter(Lecture.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


lecture = CRUDLecture(Lecture)
