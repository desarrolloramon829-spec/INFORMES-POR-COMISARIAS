"""Router para endpoints de informes estadísticos."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    FiltrosInforme, FiltrosComparativo,
    InformeResponse, ComparativoResponse,
)
from app.services.data_processor import (
    informe_delitos_modalidades,
    informe_dias_semana,
    informe_franja_horaria,
    informe_movilidad,
    informe_armas,
    informe_ambito,
    informe_jurisdicciones,
    informe_comparativo,
)

router = APIRouter(prefix="/api/informes", tags=["Informes"])


@router.post("/delitos-modalidades", response_model=InformeResponse)
def get_delitos_modalidades(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe de delitos con sus modalidades."""
    return informe_delitos_modalidades(db, filtros)


@router.post("/dias-semana", response_model=InformeResponse)
def get_dias_semana(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe de hechos por día de la semana."""
    return informe_dias_semana(db, filtros)


@router.post("/franja-horaria", response_model=InformeResponse)
def get_franja_horaria(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe de hechos por franja horaria."""
    return informe_franja_horaria(db, filtros)


@router.post("/movilidad", response_model=InformeResponse)
def get_movilidad(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe de medios de movilidad utilizados."""
    return informe_movilidad(db, filtros)


@router.post("/armas", response_model=InformeResponse)
def get_armas(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe de armas utilizadas."""
    return informe_armas(db, filtros)


@router.post("/ambito", response_model=InformeResponse)
def get_ambito(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe por ámbito de ocurrencia."""
    return informe_ambito(db, filtros)


@router.post("/jurisdicciones", response_model=InformeResponse)
def get_jurisdicciones(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Informe de hechos por jurisdicción."""
    return informe_jurisdicciones(db, filtros)


@router.post("/comparativo", response_model=ComparativoResponse)
def get_comparativo(
    filtros: FiltrosComparativo,
    db: Session = Depends(get_db),
):
    """Informe comparativo entre dos períodos."""
    return informe_comparativo(db, filtros)


@router.post("/completo")
def get_informe_completo(
    filtros: FiltrosInforme,
    db: Session = Depends(get_db),
):
    """Genera todos los informes en una sola respuesta."""
    return {
        "delitos_modalidades": informe_delitos_modalidades(db, filtros),
        "dias_semana": informe_dias_semana(db, filtros),
        "franja_horaria": informe_franja_horaria(db, filtros),
        "movilidad": informe_movilidad(db, filtros),
        "armas": informe_armas(db, filtros),
        "ambito": informe_ambito(db, filtros),
        "jurisdicciones": informe_jurisdicciones(db, filtros),
    }
