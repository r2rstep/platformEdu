from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, String, Text, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .lecture import Lecture  # noqa: F401


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    company = Column(String)
    bio = Column(Text)
    avatar_url = Column(String)
    social_urls = Column(ARRAY(String))
    lectures = relationship("Lecture", back_populates="author")
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
