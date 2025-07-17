from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from services.dependencies import get_current_user
from typing import List
import math

router = APIRouter(prefix="/providers", tags=["Proveedores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fórmula de Haversine para calcular distancia en km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radio de la tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.get("/nearby")
def get_nearby_providers(
    latitude: float = Query(...),
    longitude: float = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "cliente":
        return {"error": "Solo los clientes pueden buscar proveedores cercanos"}

    providers = db.query(User).filter(
        User.role == "proveedor",
        User.is_available == True,
        User.latitude.isnot(None),
        User.longitude.isnot(None)
    ).all()

    # Calcular distancia y ordenar
    result = []
    for p in providers:
        distance = haversine(latitude, longitude, p.latitude, p.longitude)
        result.append({
            "id": str(p.id),
            "name": p.name,
            "email": p.email,
            "distance_km": round(distance, 2)
        })

    result.sort(key=lambda x: x["distance_km"])
    return result
