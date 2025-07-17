from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(String)
