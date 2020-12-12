from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
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
    uploaded_at = Column(DateTime, nullable=False)
    pdf_download_url = Column(String)
    slug = Column(String, nullable=False)
