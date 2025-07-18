# 🔄 Forzar redeploy en Render
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa el engine y Base para crear las tablas
from database import Base, engine

# Importa los routers
from routers import user, auth, request, product, providers, category, service_category




# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Inicializa FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o restringe a ["http://localhost:3000"] por seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agrega las rutas
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(request.router)
app.include_router(providers.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(service_category.router)

# Ruta raíz para probar
@app.get("/")
def read_root():
    return {"mensaje": "¡Hola desde FastAPI!"}
