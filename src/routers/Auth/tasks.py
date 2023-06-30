import time

from src.config.celery_config import celery_app

@celery_app.task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})

def operation_task(self, x, y, o):
    if o == "add" or o == "Add":
        c = x + y
    elif o== "sub"  or o == "Sub":
        c = x - y
    elif o == "multi"  or o == "Multi":
        c = x * y
    elif o == "divide"  or o == "Divide":
        c = x / y
    return c