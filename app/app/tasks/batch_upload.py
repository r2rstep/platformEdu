from app.core.celery_app import celery_app


@celery_app.task
def process_batch_upload():
    pass
