from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Ordering CRUD App")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Food Ordering CRUD App is running"}


@app.post("/items/", response_model=schemas.FoodItemResponse)
def add_food_item(item: schemas.FoodItemCreate, db: Session = Depends(get_db)):
    return crud.create_food_item(db, item)


@app.get("/items/", response_model=list[schemas.FoodItemResponse])
def view_menu(db: Session = Depends(get_db)):
    return crud.get_food_items(db)


@app.get("/items/{item_id}", response_model=schemas.FoodItemResponse)
def view_food_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_food_item(db, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Food item not found")

    return item


@app.put("/items/{item_id}", response_model=schemas.FoodItemResponse)
def edit_food_item(
    item_id: int,
    item: schemas.FoodItemUpdate,
    db: Session = Depends(get_db)
):
    updated_item = crud.update_food_item(db, item_id, item)

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Food item not found")

    return updated_item


@app.delete("/items/{item_id}")
def delete_food_item(item_id: int, db: Session = Depends(get_db)):
    deleted_item = crud.delete_food_item(db, item_id)

    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Food item not found")

    return {"message": "Food item deleted successfully"}