from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from schemas.user import UserPublic

class RequestCreate(BaseModel):
    title: str
    description: str
    category: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class RequestRating(BaseModel):  # ✅ Nuevo esquema para calificar
    rating: float  # 1.0 a 5.0
    review: Optional[str] = None

class RequestOut(BaseModel):
    id: UUID
    title: str
    description: str
    category: str
    status: str
    created_at: datetime
    client_id: UUID
    provider_id: Optional[UUID] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    rating: Optional[float] = None
    review: Optional[str] = None

    client: Optional[UserPublic] = None  # ✅ relación anidada

    class Config:
        from_attributes = True