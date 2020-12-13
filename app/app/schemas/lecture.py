import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, conint

from .generic import Elements


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
    lecture_rating_average: Optional[float] = None


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
    lecture_rating_average: float


Lectures = Elements[Lecture]


class MinLectureRatingShortname(enum.Enum):
    all_lectures_average = 'all lectures average'


class LectureMinRatingBase(BaseModel):
    shortname: Optional[MinLectureRatingShortname] = None
    ratings_sum: Optional[float] = None
    num_ratings: Optional[int] = None
    min_rating_value: Optional[float] = None


class LectureMinRatingCreate(LectureMinRatingBase):
    shortname: MinLectureRatingShortname


class LectureMinRatingUpdate(LectureMinRatingBase):
    pass


class ReviewBase(BaseModel):
    added_at: Optional[datetime] = None
    user_id: Optional[UUID4] = None
    lecture_id: Optional[UUID4] = None
    text: Optional[str] = None
    rating: Optional[conint(ge=0, le=10)] = None


class ReviewInDbBase(ReviewBase):
    id: UUID4
    added_at: datetime
    user_id: UUID4
    lecture_id: UUID4


class ReviewInDb(ReviewInDbBase):
    pass


class ReviewUpdate(ReviewBase):
    pass


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewInDbBase):
    pass


Reviews = Elements[Review]
