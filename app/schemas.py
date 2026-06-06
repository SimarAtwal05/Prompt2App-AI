from pydantic import BaseModel


class FoodItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str | None = None
    available: bool = True


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(FoodItemBase):
    pass


class FoodItemResponse(FoodItemBase):
    id: int

    class Config:
        from_attributes = True