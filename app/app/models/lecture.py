from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class LectureType(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)


class Lecture(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True, nullable=False)
    author = relationship("User", back_populates="lectures")
    type_id = Column(Integer, ForeignKey("lecturetype.id"))
    type = relationship("LectureType")
    thumbnail_url = Column(String)
    excerpt = Column(String)
    uploaded_at = Column(DateTime, nullable=False, index=True)
    pdf_download_url = Column(String)
    slug = Column(String, nullable=False)
    reviews = relationship('Review')
    # number of decimal places should be limited to e.g. 2 to enable index on that column
    rating_average = Column(Numeric(asdecimal=False))
    min_rating_id = Column(Integer, ForeignKey('lectureminrating.id'))
    min_rating = relationship('LectureMinRating')
    video_url = Column(String)


class Review(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    lecture_id = Column(UUID(as_uuid=True), ForeignKey('lecture.id'))
    lecture = relationship('Lecture', back_populates='reviews')
    added_at = Column(DateTime, nullable=False)
    user = Column(String)
    text = Column(String)
    rating = Column(Integer)


class LectureMinRating(Base):
    id = Column(Integer, primary_key=True, index=True)
    shortname = Column(String, unique=True, nullable=False)
    ratings_sum = Column(Numeric(asdecimal=False))
    num_ratings = Column(Integer)
    # rating_sum and num_ratings should probably be exported to a separate table with more lectures stats
    # to enable more options for calculating min_rating_value (e.g. to show only lectures in top X rating)
    min_rating_value = Column(Integer)
    min_rating_per_user = relationship('User', back_populates='lecture_min_rating')
    min_rating_per_lecture = relationship('Lecture', back_populates='min_rating')
