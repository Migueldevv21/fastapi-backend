from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class RequestCreate(BaseModel):
    title: str
    description: str
    category: str
    latitude: Optional[float] = None  # ✅ Coordenadas opcionales
    longitude: Optional[float] = None

class RequestOut(BaseModel):
    id: UUID
    title: str
    description: str
    category: str
    status: str
    created_at: datetime
    client_id: UUID
    provider_id: Optional[UUID] = None
    latitude: Optional[float] = None  # ✅ Coordenadas devueltas
    longitude: Optional[float] = None

    class Config:
        from_attributes = True