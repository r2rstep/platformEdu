from .base import CRUDBase
from app.models.jobs import Job
from app.schemas.jobs import JobCreate, JobUpdate


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    pass


job = CRUDJob(Job)
