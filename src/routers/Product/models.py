from src.config.db_config import Base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float, Text
from sqlalchemy import Column
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    company_name = Column(String, nullable=True)
    batch_No = Column(String, nullable=True)
    selling_price = Column(Float)
    list_price = Column(Float)
    discount_price = Column(String)
    product_size = Column(String, nullable=True)
    product_color = Column(String, nullable=True)
    description= Column(String, nullable=True)
    image = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("User", back_populates="product")

Base.metadata.create_all(engine)