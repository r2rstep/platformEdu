from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String)
    bio = Column(Text)
    avatar_url = Column(String)
    social_urls = Column(ARRAY(String))
    # items = relationship("Item", back_populates="owner")
