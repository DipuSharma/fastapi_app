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
    address = relationship("Address", back_populates="users")
    products = relationship("Product", back_populates="users")
    profile_image = relationship("UserProfile", back_populates="users")

class UserProfile(Base):
    __tablename__ = 'profile_image'
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    image_page = Column(String, nullable=False)
    userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    users = relationship("User", back_populates='profile_image')

class BussinessAccount(Base):
    __tablename__ = "bussines_account"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=False)
    registration_no = Column(String, nullable=False)
    gst_no = Column(String, nullable=True)
    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
    state_name = Column(String, nullable=False)
    city_name = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))


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
    users = relationship("User", back_populates="address")


class Invoice(Base):
   __tablename__ = 'invoices'

   id = Column(Integer, primary_key = True)
   userid = Column(Integer, ForeignKey('users.id'))
   invno = Column(Integer)
   amount = Column(Integer)
   users = relationship("User", back_populates = "invoices")

User.invoices = relationship("Invoice", order_by = Invoice.id, back_populates = "users", cascade="all, delete, delete-orphan")
User.address = relationship('Address', order_by = Address.id, back_populates = "users", cascade="all, delete, delete-orphan")
Base.metadata.create_all(engine)
