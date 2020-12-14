from celery import Celery

celery_app = Celery("worker", broker=f"amqp://guest@queue//")

celery_app.conf.task_routes = {"app.tasks.batch_upload": "batch-upload"}
