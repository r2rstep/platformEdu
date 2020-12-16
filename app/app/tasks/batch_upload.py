from app.core.celery_app import celery_app


@celery_app.task(task_track_started=True)
def process_batch_upload():
    print('hello from app')
