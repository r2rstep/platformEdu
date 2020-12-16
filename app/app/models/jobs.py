from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Job(Base):
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    celery_task_id = Column(String, nullable=False)
