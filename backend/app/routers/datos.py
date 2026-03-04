"""Router para endpoints de importación de datos."""
import logging
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db
from app.models import HechoDelictual, Importacion
from app.config import REGIONALES, listar_todas_comisarias
from app.schemas import ImportarRequest, EstadoImportacion, ImportacionInfo
from app.services.shapefile_reader import importar_regional, importar_todo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/datos", tags=["Datos"])


@router.get("/estado", response_model=EstadoImportacion)
def get_estado(db: Session = Depends(get_db)):
    """Estado actual de la base de datos y las importaciones."""
    total_registros = db.query(func.count(HechoDelictual.id)).scalar() or 0

    total_comisarias_importadas = db.query(
        func.count(func.distinct(HechoDelictual.comisaria_origen))
    ).scalar() or 0

    total_disponibles = sum(
        len(r["comisarias"]) for r in REGIONALES.values()
    )

    importaciones = db.query(Importacion).order_by(
        desc(Importacion.fecha_importacion)
    ).limit(50).all()

    return EstadoImportacion(
        total_registros=total_registros,
        total_comisarias_importadas=total_comisarias_importadas,
        total_comisarias_disponibles=total_disponibles,
        importaciones=[
            ImportacionInfo(
                id=imp.id,
                archivo_origen=imp.archivo or "",
                comisaria=imp.comisaria or "",
                regional=imp.regional or "",
                registros_importados=imp.registros_importados or 0,
                registros_error=imp.registros_error or 0,
                estado=imp.estado or "desconocido",
                fecha_importacion=imp.fecha_importacion.isoformat() if imp.fecha_importacion else "",
                mensaje=imp.mensaje,
            )
            for imp in importaciones
        ],
    )


@router.post("/importar")
def importar_datos(
    request: ImportarRequest,
    db: Session = Depends(get_db),
):
    """Importa datos de shapefiles. Se puede filtrar por regional."""
    if request.regional:
        resultados = importar_regional(db, request.regional)
    else:
        resultados = importar_todo(db)

    exitosos = sum(1 for r in resultados if r["estado"] == "completado")
    errores = sum(1 for r in resultados if r["estado"] == "error")
    total_registros = sum(r["registros_importados"] for r in resultados)

    return {
        "mensaje": f"Importación finalizada: {exitosos} archivos OK, {errores} errores",
        "total_registros_importados": total_registros,
        "detalle": resultados,
    }


@router.post("/importar/{regional_key}")
def importar_por_regional(
    regional_key: str,
    db: Session = Depends(get_db),
):
    """Importa datos de una regional específica."""
    if regional_key not in REGIONALES:
        return {"error": f"Regional '{regional_key}' no encontrada. Disponibles: {list(REGIONALES.keys())}"}

    resultados = importar_regional(db, regional_key)

    exitosos = sum(1 for r in resultados if r["estado"] == "completado")
    total_registros = sum(r["registros_importados"] for r in resultados)

    return {
        "mensaje": f"Importación de {REGIONALES[regional_key]['nombre']} finalizada",
        "exitosos": exitosos,
        "total_registros": total_registros,
        "detalle": resultados,
    }


@router.delete("/limpiar")
def limpiar_datos(
    regional: str = None,
    db: Session = Depends(get_db),
):
    """Elimina datos importados. Se puede filtrar por regional."""
    if regional:
        eliminados = db.query(HechoDelictual).filter(
            HechoDelictual.regional == regional
        ).delete()
    else:
        eliminados = db.query(HechoDelictual).delete()

    db.commit()
    return {"mensaje": f"Eliminados {eliminados} registros", "regional": regional}
