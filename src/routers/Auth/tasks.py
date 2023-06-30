import time

from src.config.celery_config import celery_app

@celery_app.task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})

async def operation_task(self, num1, num2, operation):
    if operation == "add" or operation == "Add":
        c = num1 + num2
    elif operation == "sub" or operation == "Sub":
        c = num1 - num2
    elif operation == "multi" or operation == "Multi":
        c = num1 * num2
    elif operation == "divide" or operation == "Divide":
        c = num1 / num2
    return c