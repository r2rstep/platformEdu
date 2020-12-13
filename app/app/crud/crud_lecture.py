from datetime import datetime
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel, validator
from sqlalchemy.orm import Session, Query

from .base import CRUDBase
from .order_direction import OrderDirection
from app.models.lecture import Lecture
from app.schemas.lecture import LectureCreate, LectureUpdate


class LectureQueryFilters(BaseModel):
    author_id: Optional[UUID4] = None

    @validator('author_id', pre=True)
    def author_id_needs_to_be_uuid4(cls, value: str) -> Optional[UUID4]:
        return UUID4(value)

    class Config:
        validate_all = True


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

    def build_db_query_for_get(self,
                               db: Session,
                               *,
                               upload_time_included: datetime = None,
                               limit: int = None,
                               query_filters: LectureQueryFilters = None,
                               order_direction: OrderDirection = None):
        filters = self._get_filters(upload_time_included, order_direction, query_filters)
        order_by = Lecture.uploaded_at.asc()
        if order_direction == OrderDirection.descending:
            order_by = Lecture.uploaded_at.desc()
        query = db.query(self.model)
        if filters:
            query = query.filter(*filters)
        return query.order_by(order_by).limit(limit)

    def _get_filters(self,
                     upload_time_included: datetime,
                     order_direction: OrderDirection,
                     url_filters: LectureQueryFilters = None) -> List[Query]:
        filter_query: List[Query] = []
        if upload_time_included:
            if order_direction == OrderDirection.descending:
                filter_query.append(Lecture.uploaded_at <= upload_time_included)
            else:
                filter_query.append(Lecture.uploaded_at >= upload_time_included)

        if url_filters and url_filters.author_id:
            filter_query.append(Lecture.author_id == url_filters.author_id)

        return filter_query


lecture = CRUDLecture(Lecture)
