import time
import os
import uuid
import aiofiles
import shutil
from src.config.celery_config import celery_app
from src.config.configuration import HOST

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

file_dir = './static/image/profile/'

async def uploadProfilePicture(file):
    if len(await file.read()) >= 8388608:
        return {"message":"image file greater than 8mb"}
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    content = await file.read()
    extention = file.filename.split('.')[1]
    file_name = file_dir + file.filename
    if extention not in ['jpg', 'png', 'jpeg']:
        return {"message":"your file not valid to upload"}
    generated_url = f'{HOST}' + file_name[1:]
    async with aiofiles.open(file_name, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    return generated_url