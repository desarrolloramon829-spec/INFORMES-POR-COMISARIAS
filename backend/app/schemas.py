"""Schemas Pydantic para validación de request/response."""
from pydantic import BaseModel
from datetime import date
from typing import Optional


# --- Filtros ---
class FiltrosInforme(BaseModel):
    regional: Optional[str] = None
    comisaria: Optional[str] = None
    fecha_desde: Optional[str] = None  # YYYY-MM-DD
    fecha_hasta: Optional[str] = None  # YYYY-MM-DD
    delito: Optional[str] = None


class FiltrosComparativo(BaseModel):
    regional: Optional[str] = None
    comisaria: Optional[str] = None
    fecha_desde_1: Optional[str] = None
    fecha_hasta_1: Optional[str] = None
    fecha_desde_2: Optional[str] = None
    fecha_hasta_2: Optional[str] = None


# --- Respuestas de informes ---
class FilaInforme(BaseModel):
    categoria: str
    subcategoria: Optional[str] = None
    cantidad: int
    porcentaje: float


class InformeResponse(BaseModel):
    titulo: str
    total: int
    filas: list[FilaInforme]
    filtros_aplicados: dict


class ComparativoFila(BaseModel):
    categoria: str
    cantidad_periodo1: int
    cantidad_periodo2: int
    diferencia: int
    porcentaje_cambio: Optional[float] = None


class ComparativoResponse(BaseModel):
    titulo: str
    periodo1: str
    periodo2: str
    total_periodo_1: int = 0
    total_periodo_2: int = 0
    filas: list[ComparativoFila]


# --- Mapa ---
class PuntoMapa(BaseModel):
    id: int
    latitud: float
    longitud: float
    delito: str
    modalidad: Optional[str] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    direccion: Optional[str] = None
    jurisdiccion: Optional[str] = None
    comisaria: Optional[str] = None


class PuntosMapaResponse(BaseModel):
    total: int
    puntos: list[PuntoMapa]


# --- Filtros disponibles ---
class RegionalInfo(BaseModel):
    codigo: str
    nombre: str
    total_comisarias: int


class ComisariaInfo(BaseModel):
    codigo: Optional[str] = None
    nombre: str
    regional: str


class FiltrosDisponibles(BaseModel):
    regionales: list[RegionalInfo]
    delitos: Optional[list[str]] = None
    fecha_min: Optional[str] = None
    fecha_max: Optional[str] = None


# --- Importación ---
class ImportarRequest(BaseModel):
    regional: Optional[str] = None  # None = importar todas


class ImportacionInfo(BaseModel):
    id: int
    archivo_origen: str
    comisaria: str
    regional: str
    registros_importados: int
    registros_error: int
    estado: str
    fecha_importacion: str
    mensaje: Optional[str] = None


class EstadoImportacion(BaseModel):
    total_registros: int
    total_comisarias_importadas: int
    total_comisarias_disponibles: int
    importaciones: list[ImportacionInfo]


# --- Dashboard ---
class DashboardResponse(BaseModel):
    total_hechos: int
    total_comisarias: int
    hechos_mes_actual: int
    top_delito: Optional[str] = None
    top_delito_cantidad: int = 0
    jurisdicciones_activas: int = 0
    delitos_top: list[dict] = []
    por_dia: list[dict] = []
    por_franja: list[dict] = []
    ultima_importacion: Optional[str] = None
    hechos_por_mes: list[dict] = []
