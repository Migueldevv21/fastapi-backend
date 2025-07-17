from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import user as schemas  # ✅ importar como schemas
from schemas.token import Token  # ✅ importar el esquema del token
from crud import user as crud_user  # ✅ importar el módulo crud
from services.auth import create_user
from services.token import create_access_token  # ✅ importar función para generar token
from models.user import User
from services.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/users", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Token)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    db_user = create_user(db, user)
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/providers", response_model=List[schemas.UserOut])
def get_providers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(User).filter(User.role == "proveedor").all()

@router.get("/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: str, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_user.name = user.name
    db_user.email = user.email
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado"}