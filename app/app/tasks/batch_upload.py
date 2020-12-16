from app.core.celery_app import celery_app
from app.logic import batch_upload


@celery_app.task(task_track_started=True)
def process_batch_upload(batch_data: dict):
    batch_upload.process(batch_data)
