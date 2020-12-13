import re
from typing import Any
import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import UUID4, ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.logic import lecture as lecture_logic

router = APIRouter()


@router.get("/", response_model=schemas.lecture.Lectures)
def list_lectures(request: Request,
                  limit: int = 100,
                  cursor: str = '',
                  db: Session = Depends(deps.get_db)) -> Any:
    filters_regex = re.compile(r'.*filter\[(?P<key>\w+)\]=(?P<value>[\w\-]+).*')
    filters_parsed = re.match(filters_regex, urllib.parse.unquote(str(request.query_params)))
    filters = None
    if filters_parsed:
        try:
            filters = crud.LectureQueryFilters(**{filters_parsed['key']: filters_parsed['value']})
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return lecture_logic.build_lectures_response(db,
                                                 _build_url_template(request),
                                                 cursor,
                                                 limit,
                                                 filters)


def _build_url_template(request):
    return '{api_base}?cursor={{cursor}}&limit={{limit}}&filter[author_id]={{author_id}}'.format(
        api_base=request.url.path.rstrip('/'))


@router.post("/", response_model=schemas.Lecture)
def create_lecture(
    *,
    db: Session = Depends(deps.get_db),
    lecture_in: schemas.LectureCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    lecture_in.slug = lecture_logic.create_slug(lecture_in.title)
    lecture_in.uploaded_at = lecture_logic.get_upload_time()
    lecture = crud.lecture.create_with_author(db=db, obj_in=lecture_in, author_id=current_user.id)
    return lecture


@router.get("/{id}", response_model=schemas.Lecture)
def get_lecture(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID4
) -> Any:
    lecture = crud.lecture.get(db=db, id=id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Item not found")
    return lecture
