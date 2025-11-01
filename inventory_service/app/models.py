from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warehouse = Column(String, nullable=True, default="default")
