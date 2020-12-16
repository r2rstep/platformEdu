from fastapi import APIRouter, Response, status

from app.core.config import settings
from app.tasks.batch_upload import process_batch_upload

router = APIRouter()


@router.get('/{job_id')
def get_job_details(job_id: int):
    pass
