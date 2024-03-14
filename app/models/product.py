from sqlalchemy import Column, String, Integer, Float, ARRAY, Date

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    information = Column(String)
    features = Column(String)
    url = Column(String)
    price = Column(Float)
    old_price = Column(Float)
    min = Column(Integer)
    images = Column(ARRAY(String))
    spider_name = Column(String)
    brand = Column(String)
    category = Column(String)
    updated_at = Column(Date)
    subcategories = Column(ARRAY(String))
