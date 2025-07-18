from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.request import RequestCreate, RequestOut
from models.request import ServiceRequest
from services.dependencies import get_current_user
from models.user import User
from typing import List
from schemas.request import RequestRating  # ✅ Importar el nuevo esquema


router = APIRouter(prefix="/requests", tags=["Solicitudes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear solicitud (cliente)
@router.post("/", response_model=RequestOut)
def create_service_request(
    data: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden crear solicitudes")

    request = ServiceRequest(
        title=data.title,
        description=data.description,
        category=data.category,
        client_id=current_user.id
    )

    db.add(request)
    db.commit()
    db.refresh(request)
    return request

# Ver solicitudes pendientes (proveedor)
@router.get("/", response_model=List[RequestOut])
def get_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "proveedor":
        raise HTTPException(status_code=403, detail="Solo los proveedores pueden ver las solicitudes")

    solicitudes = db.query(ServiceRequest).filter(ServiceRequest.status == "pendiente").all()
    return solicitudes
# ver solicitudes cliente
@router.get("/my-requests", response_model=List[RequestOut])
def get_client_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden ver sus solicitudes")

    solicitudes = db.query(ServiceRequest).filter(ServiceRequest.client_id == current_user.id).all()
    return solicitudes

# Aceptar solicitud (proveedor)
@router.put("/{request_id}/accept", response_model=RequestOut)
def accept_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "proveedor":
        raise HTTPException(status_code=403, detail="Solo los proveedores pueden aceptar solicitudes")

    request = db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if request.status != "pendiente":
        raise HTTPException(status_code=400, detail="La solicitud ya fue aceptada o completada")

    request.status = "aceptado"
    request.provider_id = current_user.id

    db.commit()
    db.refresh(request)

    return request

# ✅ Ver solicitudes propias (cliente)
@router.get("/mine", response_model=List[RequestOut])
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden ver sus solicitudes")

    return db.query(ServiceRequest).filter(ServiceRequest.client_id == current_user.id).all()

# ⭐ Calificar solicitud completada (cliente)
@router.put("/{request_id}/rate", response_model=RequestOut)
def rate_completed_request(
    request_id: str,
    data: RequestRating,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden calificar solicitudes")

    request = db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if request.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes calificar esta solicitud")

    if request.status != "completado":
        raise HTTPException(status_code=400, detail="Solo puedes calificar solicitudes completadas")

    request.rating = data.rating
    request.review = data.review

    db.commit()
    db.refresh(request)

    return request
@router.put("/{request_id}/complete", response_model=RequestOut)
def complete_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "proveedor":
        raise HTTPException(status_code=403, detail="Solo los proveedores pueden completar solicitudes")

    request = db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if request.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes completar esta solicitud")

    if request.status != "aceptado":
        raise HTTPException(status_code=400, detail="Solo puedes completar solicitudes aceptadas")

    request.status = "completado"
    db.commit()
    db.refresh(request)

    return request
# ✅ Ver solicitudes aceptadas por el proveedor
@router.get("/provider", response_model=List[RequestOut])
def get_provider_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "proveedor":
        raise HTTPException(status_code=403, detail="Solo los proveedores pueden ver sus solicitudes")

    solicitudes = db.query(ServiceRequest).filter(ServiceRequest.provider_id == current_user.id).all()
    return solicitudes