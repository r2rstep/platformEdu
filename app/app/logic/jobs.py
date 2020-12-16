from celery.result import AsyncResult
from sqlalchemy.orm import Session

from app import crud
from app.schemas.jobs import JobState, JobResult


def get_job_result(db: Session, job_id: int) -> (JobState, JobResult):
    job = crud.job.get(db, job_id)
    celery_task = AsyncResult(job.celery_task_id)
    state = JobState.pending
    result = JobResult.unknown

    if celery_task.ready():
        state = JobState.finished
        result = JobResult.successful if celery_task.successful() else JobResult.failed
    elif celery_task.state().lower() in ['started', 'retry']:
        state = JobState.running
    return state, result
