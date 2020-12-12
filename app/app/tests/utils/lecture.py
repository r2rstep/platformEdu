from datetime import datetime
from typing import Optional

from pydantic import UUID4
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.lecture import LectureCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_lecture(db: Session, *, author_id: Optional[UUID4] = None) -> models.Lecture:
    if author_id is None:
        user = create_random_user(db)
        author_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    lecture_in = LectureCreate(title=title, uploaded_at=datetime.utcnow(),
                               excerpt=description, slug=random_lower_string())
    return crud.lecture.create_with_author(db=db, obj_in=lecture_in, author_id=author_id)
