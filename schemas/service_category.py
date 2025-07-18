from pydantic import BaseModel, HttpUrl
from typing import Optional

class ServiceCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = True