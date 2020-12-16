import json

from celery.result import AsyncResult
from fastapi import APIRouter, Response, status, Depends, File
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app import crud
from app.schemas.jobs import JobCreate, JobType
from app.tasks.batch_upload import process_batch_upload

router = APIRouter()


@router.post('/batchUpload')
def batch_upload(resp: Response, lectures_json: bytes = File(...), db: Session = Depends(deps.get_db)):
    promise: AsyncResult = process_batch_upload.delay(json.loads(lectures_json))
    job_in_db = crud.job.create(db, obj_in=JobCreate(type=JobType.batch_upload, celery_task_id=str(promise.id)))
    resp.status_code = status.HTTP_303_SEE_OTHER
    resp.headers['Location'] = f'{settings.API_V1_STR}/jobs/{job_in_db.id}'
