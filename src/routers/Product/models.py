from src.config.db_config import Base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float, Text
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from src.routers.Auth.models import User

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    batch_No = Column(String, nullable=False)
    selling_price = Column(Float, nullable=False)
    list_price = Column(Float, nullable=False)
    discount_price = Column(String, nullable=True)
    product_size = Column(String, nullable=True)
    product_color = Column(String, nullable=True)
    description= Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    users = relationship("User", back_populates="products")
    product_images = relationship('ProductImage', back_populates='products')


class ProductImage(Base):
    __tablename__ = 'product_image'
    id = Column(Integer, primary_key=True, index=True)
    product_image_name = Column(String, nullable=False)
    product_image_path = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    products = relationship("Product", back_populates='product_images')


User.products = relationship('Product', order_by = Product.id, back_populates = "users", cascade="all, delete, delete-orphan")
Product.product_images = relationship('ProductImage', order_by = ProductImage.id, back_populates = "products", cascade="all, delete, delete-orphan")
Base.metadata.create_all(engine)