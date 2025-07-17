from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from services.auth import get_password_hash  # ✅ nombre correcto

def create_user(db: Session, user: UserCreate) -> User:
    try:
        print("➡️ Intentando crear usuario:", user.email)

        hashed_password = get_password_hash(user.password)
        print("🔐 Contraseña hasheada correctamente")

        db_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            role=user.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print("✅ Usuario creado:", db_user.email)
        return db_user

    except Exception as e:
        print("❌ Error al crear usuario:", str(e))
        raise HTTPException(status_code=500, detail="Error interno al registrar usuario")