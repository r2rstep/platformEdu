from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api import deps
from app import crud
from app.logic.jobs import get_job_result
from app.schemas.jobs import Job, JobLinks

router = APIRouter()


@router.get('/{job_id}', response_model=Job)
def get_job_details(job_id: int, req: Request, db: Session = Depends(deps.get_db)):
    job_in_db = crud.job.get(db, id=job_id)
    state, result = get_job_result(db, job_id)
    return Job(**job_in_db.__dict__, state=state, result=result, links=JobLinks(self=req.url.path.rstrip('/')))
