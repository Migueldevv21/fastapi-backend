from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from services.auth import get_password_hash  # ✅ nombre correcto

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)  # ✅ corregido
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()
