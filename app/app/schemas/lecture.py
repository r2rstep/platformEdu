from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, UUID4


# Shared properties
class LectureBase(BaseModel):
    title: Optional[str]
    content: Optional[str] = None
    type_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    excerpt: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    pdf_download_url: Optional[str] = None
    slug: Optional[str] = None


# Properties to receive on item creation
class LectureCreate(LectureBase):
    title: str


# Properties to receive on item update
class LectureUpdate(LectureBase):
    pass


# Properties shared by models stored in DB
class LectureInDBBase(LectureBase):
    id: UUID4
    title: str
    author_id: UUID4
    uploaded_at: datetime
    slug: str

    class Config:
        orm_mode = True


# Properties to return to client
class Lecture(LectureInDBBase):
    pass


# Properties properties stored in DB
class LectureInDB(LectureInDBBase):
    author_id: UUID4


class LecturesLinks(BaseModel):
    self: str
    previous: str = None
    next: str = None


class Lectures(BaseModel):
    total: int
    count: int
    items: List[Lecture]
    links: LecturesLinks
