import enum
from typing import Optional

from pydantic import BaseModel


class JobType(enum.IntEnum):
    batch_upload = 0


class JobBase(BaseModel):
    type: Optional[JobType] = None


class JobCreate(JobBase):
    task_id: str


class JobUpdate(JobBase):
    pass


class JobInDbBase(JobBase):
    id: int
    type: JobType

    class Config:
        orm_mode = True


class JobInDb(JobInDbBase):
    id: int
    type: JobType
    task_id: str


class JobLinks(BaseModel):
    self: str


class JobState(enum.Enum):
    pending = 'pending'
    running = 'running'
    finished = 'finished'


class JobResult(enum.Enum):
    unknown = 'unknown'
    successful = 'successful'
    failed = 'failed'


class Job(JobInDbBase):
    state: JobState
    result: JobResult
    links: JobLinks
