from sqlalchemy import Column, String, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "cliente" o "proveedor"
    is_available = Column(Boolean, default=False)

    # ✅ Campos opcionales para ubicación
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)