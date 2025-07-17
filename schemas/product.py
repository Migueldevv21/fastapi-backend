from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    price: float
    image_url: str | None = None
    description: str
    category_id: int  # <- importante

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
