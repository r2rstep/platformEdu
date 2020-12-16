from celery import Celery

from app.core.config import settings

celery_app = Celery("worker", broker=f"amqp://guest@{settings.QUEUE_HOSTNAME}//")

celery_app.conf.task_routes = {"app.tasks.batch_upload.*": "batch-upload"}
celery_app.conf.task_track_started
