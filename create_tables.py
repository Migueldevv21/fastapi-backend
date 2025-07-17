from database import Base, engine
from models.user import User
from models.request import ServiceRequest  # agrega esta línea

print("Creando tablas...")
Base.metadata.create_all(bind=engine)


