from src.config.configuration import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = "sqlite:///./mydb.db"
# Postgres SQL
# DATABASE_URI = 'postgresql://postgres:<password>@localhost/<name_of_the_database>'


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()