# backend/routers/category.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import category as category_schema
from crud import category as category_crud

router = APIRouter(prefix="/categories", tags=["categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=category_schema.CategoryOut)
def create_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    print(">> Datos recibidos:", category.dict())  # 👈 aqu
    return category_crud.create_category(db, category)

@router.get("/", response_model=list[category_schema.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return category_crud.get_categories(db)

@router.get("/{category_id}", response_model=category_schema.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = category_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.put("/{category_id}", response_model=category_schema.CategoryOut)
def update_category(category_id: int, category: category_schema.CategoryUpdate, db: Session = Depends(get_db)):
    return category_crud.update_category(db, category_id, category)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_crud.delete_category(db, category_id)
