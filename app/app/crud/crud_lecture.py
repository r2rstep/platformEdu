from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session

from .base import CRUDBase
from .order_direction import OrderDirection
from app.models.lecture import Lecture
from app.schemas.lecture import LectureCreate, LectureUpdate


class CRUDLecture(CRUDBase[Lecture, LectureCreate, LectureUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: LectureCreate, author_id: UUID4
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

    def get_sorted_by_upload_time(self,
                                  db: Session,
                                  *,
                                  order_direction: OrderDirection,
                                  limit: int,
                                  upload_time_included: datetime = None) -> Lecture:
        # this could be probably optimized by using dogpile cache
        if order_direction == OrderDirection.descending:
            if upload_time_included:
                filter_query = Lecture.uploaded_at <= upload_time_included
            order_by = Lecture.uploaded_at.desc()
        else:
            if upload_time_included:
                filter_query = Lecture.uploaded_at >= upload_time_included
            order_by = Lecture.uploaded_at.asc()

        query = db.query(self.model)
        if upload_time_included:
            query = query.filter(filter_query)
        return query.order_by(order_by).limit(limit).all()


lecture = CRUDLecture(Lecture)
