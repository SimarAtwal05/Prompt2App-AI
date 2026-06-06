from sqlalchemy.orm import Session
from app import models, schemas


def create_food_item(db: Session, item: schemas.FoodItemCreate):
    db_item = models.FoodItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_food_items(db: Session):
    return db.query(models.FoodItem).all()


def get_food_item(db: Session, item_id: int):
    return db.query(models.FoodItem).filter(models.FoodItem.id == item_id).first()


def update_food_item(db: Session, item_id: int, item: schemas.FoodItemUpdate):
    db_item = get_food_item(db, item_id)

    if db_item is None:
        return None

    for key, value in item.model_dump().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_food_item(db: Session, item_id: int):
    db_item = get_food_item(db, item_id)

    if db_item is None:
        return None

    db.delete(db_item)
    db.commit()
    return db_item