from fastapi import APIRouter, Response, status

from app.core.config import settings

router = APIRouter()


@router.post('/batchUpload')
def batch_upload(resp: Response):
    resp.status_code = status.HTTP_303_SEE_OTHER
    resp.headers['Location'] = f'{settings.API_V1_STR}/jobs/job-id'
