from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Lecture])
def list_lectures(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve lectures.
    """
    if crud.user.is_superuser(current_user):
        lectures = crud.lecture.get_multi(db, skip=skip, limit=limit)
    else:
        lectures = crud.lecture.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return lectures


@router.post("/", response_model=schemas.Lecture)
def create_lecture(
    *,
    db: Session = Depends(deps.get_db),
    lecture_in: schemas.LectureCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    lecture = crud.lecture.create_with_owner(db=db, obj_in=lecture_in, author_id=current_user.id)
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
