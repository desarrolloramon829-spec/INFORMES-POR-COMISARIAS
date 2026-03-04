"""Router para endpoints de filtros disponibles."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import HechoDelictual
from app.config import REGIONALES
from app.schemas import RegionalInfo, ComisariaInfo, FiltrosDisponibles

router = APIRouter(prefix="/api/filtros", tags=["Filtros"])


@router.get("/regionales")
def get_regionales():
    """Lista de regionales disponibles."""
    return [
        RegionalInfo(
            codigo=key,
            nombre=data["nombre"],
            total_comisarias=len(data["comisarias"]),
        )
        for key, data in REGIONALES.items()
    ]


@router.get("/comisarias")
def get_comisarias(
    regional: str = Query(default=None, description="Filtrar por regional"),
):
    """Lista de comisarías, opcionalmente filtradas por regional."""
    resultado = []
    for key, data in REGIONALES.items():
        if regional and key != regional:
            continue
        for cria in data["comisarias"]:
            resultado.append(ComisariaInfo(
                nombre=cria["nombre"],
                regional=key,
            ))
    return resultado


@router.get("/delitos")
def get_delitos(db: Session = Depends(get_db)):
    """Lista distinta de delitos disponibles."""
    delitos = db.query(
        HechoDelictual.delito
    ).filter(
        HechoDelictual.delito.isnot(None),
    ).distinct().order_by(HechoDelictual.delito).all()

    return [d.delito for d in delitos]


@router.get("/rango-fechas")
def get_rango_fechas(db: Session = Depends(get_db)):
    """Fecha mínima y máxima disponibles."""
    resultado = db.query(
        func.min(HechoDelictual.fecha_hecho).label("fecha_min"),
        func.max(HechoDelictual.fecha_hecho).label("fecha_max"),
    ).first()

    return {
        "fecha_min": resultado.fecha_min.isoformat() if resultado.fecha_min else None,
        "fecha_max": resultado.fecha_max.isoformat() if resultado.fecha_max else None,
    }


@router.get("/disponibles", response_model=FiltrosDisponibles)
def get_filtros_disponibles(db: Session = Depends(get_db)):
    """Retorna todos los filtros disponibles de una vez."""
    regionales = [
        RegionalInfo(
            codigo=key,
            nombre=data["nombre"],
            total_comisarias=len(data["comisarias"]),
        )
        for key, data in REGIONALES.items()
    ]

    delitos = db.query(
        HechoDelictual.delito
    ).filter(
        HechoDelictual.delito.isnot(None),
    ).distinct().order_by(HechoDelictual.delito).all()

    rango = db.query(
        func.min(HechoDelictual.fecha_hecho).label("fecha_min"),
        func.max(HechoDelictual.fecha_hecho).label("fecha_max"),
    ).first()

    return FiltrosDisponibles(
        regionales=regionales,
        delitos=[d.delito for d in delitos],
        fecha_min=rango.fecha_min.isoformat() if rango.fecha_min else None,
        fecha_max=rango.fecha_max.isoformat() if rango.fecha_max else None,
    )
