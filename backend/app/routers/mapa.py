"""Router para endpoints del mapa interactivo."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import HechoDelictual, Jurisdiccion
from app.schemas import FiltrosInforme, PuntoMapa, PuntosMapaResponse

router = APIRouter(prefix="/api/mapa", tags=["Mapa"])


@router.post("/puntos", response_model=PuntosMapaResponse)
def get_puntos_mapa(
    filtros: FiltrosInforme,
    limite: int = Query(default=5000, le=50000),
    db: Session = Depends(get_db),
):
    """Retorna puntos delictuales para el mapa según filtros."""
    query = db.query(
        HechoDelictual.id,
        HechoDelictual.y,  # latitud
        HechoDelictual.x,  # longitud
        HechoDelictual.delito,
        HechoDelictual.modalidad,
        HechoDelictual.fecha_hecho,
        HechoDelictual.direccion_hecho,
        HechoDelictual.comisaria_origen,
    ).filter(
        HechoDelictual.x.isnot(None),
        HechoDelictual.y.isnot(None),
    )

    if filtros.regional:
        query = query.filter(HechoDelictual.regional == filtros.regional)
    if filtros.comisaria:
        query = query.filter(HechoDelictual.comisaria_origen == filtros.comisaria)
    if filtros.fecha_desde:
        query = query.filter(HechoDelictual.fecha_hecho >= filtros.fecha_desde)
    if filtros.fecha_hasta:
        query = query.filter(HechoDelictual.fecha_hecho <= filtros.fecha_hasta)
    if filtros.delito:
        query = query.filter(HechoDelictual.delito.ilike(f"%{filtros.delito}%"))

    # Contar total antes de limitar
    total = query.count()

    resultados = query.limit(limite).all()

    puntos = [
        PuntoMapa(
            id=r.id,
            latitud=r.y,
            longitud=r.x,
            delito=r.delito or "Sin dato",
            modalidad=r.modalidad,
            fecha=r.fecha_hecho.isoformat() if r.fecha_hecho else None,
            direccion=r.direccion_hecho,
            comisaria=r.comisaria_origen,
        )
        for r in resultados
    ]

    return PuntosMapaResponse(total=total, puntos=puntos)


@router.get("/jurisdicciones")
def get_jurisdicciones(db: Session = Depends(get_db)):
    """Retorna GeoJSON de polígonos de jurisdicciones."""
    jurisdicciones = db.query(Jurisdiccion).all()

    features = []
    for j in jurisdicciones:
        if j.geom:
            from geoalchemy2.shape import to_shape
            geom = to_shape(j.geom)
            features.append({
                "type": "Feature",
                "properties": {
                    "id": j.id,
                    "nombre": j.nombre,
                    "regional": j.regional,
                },
                "geometry": geom.__geo_interface__,
            })

    return {
        "type": "FeatureCollection",
        "features": features,
    }


@router.get("/heatmap")
def get_heatmap_data(
    regional: str = Query(default=None),
    db: Session = Depends(get_db),
):
    """Retorna datos agregados para mapa de calor."""
    query = db.query(
        HechoDelictual.y,
        HechoDelictual.x,
    ).filter(
        HechoDelictual.x.isnot(None),
        HechoDelictual.y.isnot(None),
    )

    if regional:
        query = query.filter(HechoDelictual.regional == regional)

    resultados = query.limit(20000).all()

    return {
        "puntos": [[r.y, r.x, 1.0] for r in resultados],
        "total": len(resultados),
    }
