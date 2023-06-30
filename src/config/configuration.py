import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(".env")

EMAIL_USER = os.getenv("MAIL_USERNAME")
EMAIL_PASS = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
EMAIL = os.getenv("MAIL_FROM")
PASS = os.getenv("PASS")
ALGO = os.getenv("ALGO")
BASE_DIR = Path(__file__).resolve().parent
HOST_URL = os.getenv("HOST_URL")
HOST_PORT = os.getenv("HOST_PORT")

# Celery objects

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


class Settings:
    PORT = 8000
    HOST_URL = HOST_URL
    HOST_PORT = HOST_PORT
    TITLE = "Dipu Fastapi App"
    VERSION = "V:0.0.0.1"
    DESCRIPTION = """
        This is my application created in Fastapi, and this application under developing for inventory project.
        Folder Structure follow as well as Nest js app.
        """
    NAME = "Dipu Kumar Sharma"
    EMAIL = EMAIL
    PASS = PASS
    TAGS = [
        {"name": "Auth", "description": "This is Authentication Routes"},
        {"name": "Administrator", "description": "This is Admin Routes"},
        {"name": "Address", "description": "This is Address Routes"},
        {"name": "Customer", "description": "This is customer routes"},
        {"name": "Product", "description": "This is Product Routes"},
        {"name": "Shop", "description": "This is shop Routes"},
    ]
    PROJECT_NAME: str = "Inventory Application"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY = "Sv/w?/T@^CN8RR$O8^I7Tss6'j76it"
    ALGORITHM = ALGO
    CELERY_BROKER_URL = CELERY_BROKER_URL
    CELERY_BACKEND = CELERY_BROKER_URL
    CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
    BASE_DIR: BASE_DIR
    DATABASE_CONNECT_DICT: dict = {}

setting = Settings()
