from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pendiente")  # pendiente, aceptado, completado

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    client_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    provider_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    client = relationship("User", foreign_keys=[client_id], backref="requests_made")
    provider = relationship("User", foreign_keys=[provider_id], backref="requests_taken")

    # ⭐ Campos de calificación
    rating = Column(Float, nullable=True)  # 1.0 a 5.0
    review = Column(String, nullable=True)  # Comentario del cliente