"""Aplicación principal FastAPI."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import informes, mapa, datos, filtros
from app.services.data_processor import generar_dashboard

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicialización y shutdown de la aplicación."""
    # Crear tablas si no existen
    logger.info("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas correctamente.")
    yield
    logger.info("Cerrando aplicación...")


app = FastAPI(
    title="Sistema de Informes Delictuales",
    description="API para la Sección de Análisis Delictual - Policía de Tucumán",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(informes.router)
app.include_router(mapa.router)
app.include_router(datos.router)
app.include_router(filtros.router)


@app.get("/")
def root():
    """Endpoint raíz."""
    return {
        "sistema": "Informes Delictuales - Policía de Tucumán",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/dashboard")
def dashboard():
    """Dashboard principal con estadísticas generales."""
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        return generar_dashboard(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    """Health check."""
    from app.database import SessionLocal
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}
