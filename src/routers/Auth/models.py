from src.config.db_config import Base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float, Text
from sqlalchemy import Column
from sqlalchemy.orm import relationship
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
    address = relationship("Address", back_populates="user")
    product = relationship("Product", back_populates="user")


class OTP(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    otp = Column(String, nullable=False)
    status = Column(String, nullable=False)
    exp_time = Column(Float, nullable=False)
    count_otp = Column(Integer, nullable=False)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String, nullable=False)
    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    is_home = Column(Boolean, nullable=False)
    is_office = Column(Boolean, nullable=False)
    is_order = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("User", back_populates="address")

Base.metadata.create_all(engine)