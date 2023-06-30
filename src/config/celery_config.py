from celery import Celery
from src.config.configuration import setting

celery_app = Celery(
    "worker",
    broker_url=setting.CELERY_BROKER_URL,
    result_backend="rpc://",
)
celery_app.conf.update(task_track_started=True)