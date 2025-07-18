from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.service_category import ServiceCategory
from schemas.service_category import ServiceCategoryCreate
from typing import List
from schemas.service_category import ServiceCategoryOut



router = APIRouter(prefix="/categories", tags=["Service Categories"])

@router.post("/", status_code=201)
def create_category(category: ServiceCategoryCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe
    existing = db.query(ServiceCategory).filter_by(name=category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe.")

    new_category = ServiceCategory(
        name=category.name,
        description=category.description,
        image_url=str(category.image_url) if category.image_url else None,
        is_active=category.is_active
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=List[ServiceCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(ServiceCategory).filter_by(is_active=True).all()
    return categories