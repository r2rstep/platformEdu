from fastapi import APIRouter, Response, status

from app.core.config import settings
from app.tasks.batch_upload import process_batch_upload

router = APIRouter()


@router.post('/batchUpload')
def batch_upload(resp: Response):
    process_batch_upload.delay()
    resp.status_code = status.HTTP_303_SEE_OTHER
    resp.headers['Location'] = f'{settings.API_V1_STR}/jobs/job-id'
