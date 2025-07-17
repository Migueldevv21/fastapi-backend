from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import product as product_schema
from crud import product as product_crud

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=product_schema.ProductOut)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db, product)

@router.get("/", response_model=list[product_schema.ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    return product_crud.get_products(db)

@router.put("/{product_id}", response_model=product_schema.ProductOut)
def update_product(product_id: int, updated: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_crud.update_product(db, product_id, updated)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_crud.delete_product(db, product_id)
