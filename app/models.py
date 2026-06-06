from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String)
    available = Column(Boolean, default=True)