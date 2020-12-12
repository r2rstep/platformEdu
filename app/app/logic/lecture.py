from datetime import datetime

from sqlalchemy.orm import Session

from app import crud
from app.crud.order_direction import OrderDirection
from app.schemas.lecture import Lectures, LecturesLinks


def create_slug(title: str) -> str:
    return '-'.join(title.lower().split())


def get_upload_time() -> datetime:
    return datetime.utcnow()


def build_lectures_response(db: Session,
                            url_template: str,
                            cursor: str,  # would hashing the cursor give any benefit (e.g. security)?
                            limit: int):
    def _build_links():
        links = LecturesLinks(self=url_template.format(cursor=cursor, limit=limit))

        if next_page_first_lecture:
            links.next = url_template.format(cursor=next_page_first_lecture.uploaded_at,
                                             limit=limit)

        if len(previous_page_lectures) > 1:
            links.previous = url_template.format(cursor=previous_page_lectures[-1].uploaded_at,
                                                 limit=limit)
        return links

    lectures_in_db = crud.lecture.get_sorted_by_upload_time(
        db,
        order_direction=OrderDirection.ascending,
        limit=limit + 1,
        upload_time_included=cursor
    )
    current_page_lectures = lectures_in_db[:-1] if len(lectures_in_db) > limit else lectures_in_db
    next_page_first_lecture = lectures_in_db[-1] if len(lectures_in_db) > limit else None
    previous_page_lectures = crud.lecture.get_sorted_by_upload_time(
        db,
        order_direction=OrderDirection.descending,
        limit=11,
        upload_time_included=current_page_lectures[0].uploaded_at)

    return Lectures(total=crud.lecture.count(db),
                    count=len(current_page_lectures),
                    items=current_page_lectures,
                    links=_build_links())
