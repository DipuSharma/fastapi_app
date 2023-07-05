import os
import uvicorn
from fastapi import FastAPI
from celery import Celery
from fastapi.staticfiles import StaticFiles
from src.config.configuration import setting
from fastapi.middleware.cors import CORSMiddleware

from src.routers.Auth import controller as auth
from src.routers.Product import controller as product_router

# Celery configuration
from src.config.celery_config import celery_app

# celery command
"""
                   celery -A main.celery_app worker --loglevel=info
""" 
host_url = setting.HOST_URL
port_url = setting.HOST_PORT
app = FastAPI(title=setting.TITLE,
              description=setting.DESCRIPTION,
              version=setting.VERSION,
              openapi_tags=setting.TAGS,
              docs_url="/dipu")

origins = ["http://localhost:3000", '0.0.0.0']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(product_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=f'{host_url}', port=f'{port_url}', reload=True)