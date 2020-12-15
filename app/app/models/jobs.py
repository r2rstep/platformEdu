from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Job(Base):
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    celery_task_id = Column(String, nullable=False)
