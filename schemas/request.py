from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class RequestCreate(BaseModel):
    title: str
    description: str
    category: str

class RequestOut(BaseModel):
    id: UUID
    title: str
    description: str
    category: str
    status: str
    created_at: datetime
    client_id: UUID
    provider_id: Optional[UUID] = None  # si usas provider_id en el modelo

    class Config:
        from_attributes = True
