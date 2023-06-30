from src.config.db_config import Base, engine

from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float, Text
from sqlalchemy import Column

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)
    is_user = Column(Boolean)
    is_shopkeeper = Column(Boolean)
    is_active = Column(Boolean)

Base.metadata.create_all(engine)