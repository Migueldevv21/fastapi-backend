from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "cliente" o "proveedor"

class UserUpdate(BaseModel):  # ✅ Nuevo esquema para editar perfil
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    latitude: Optional[float] = None  # ✅ Incluye ubicación si está disponible
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True