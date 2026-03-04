"""Servicio de procesamiento de datos para generación de informes."""
import logging
from datetime import date, datetime
from typing import Optional

from sqlalchemy import func, case, desc, and_, extract
from sqlalchemy.orm import Session

from app.models import HechoDelictual, Importacion
from app.schemas import (
    FiltrosInforme, FiltrosComparativo,
    InformeResponse, FilaInforme,
    ComparativoResponse, ComparativoFila,
    DashboardResponse,
)

logger = logging.getLogger(__name__)

# Orden canónico de días de la semana
ORDEN_DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Orden canónico de franjas horarias
ORDEN_FRANJAS = [
    "Madrugada (00:00-05:59)",
    "Mañana (06:00-08:59)",
    "Vespertina (09:00-12:59)",
    "Siesta (13:00-15:59)",
    "Tarde (16:00-19:59)",
    "Noche (20:00-23:59)",
]


def _aplicar_filtros(query, filtros: FiltrosInforme):
    """Aplica filtros comunes a una query."""
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
    return query


def _filtros_dict(filtros: FiltrosInforme) -> dict:
    """Convierte filtros a dict para incluir en la respuesta."""
    return {k: v for k, v in filtros.model_dump().items() if v is not None}


def informe_delitos_modalidades(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe de delitos con modalidades."""
    query = db.query(
        HechoDelictual.delito,
        HechoDelictual.modalidad,
        func.count().label("cantidad"),
    ).filter(HechoDelictual.delito.isnot(None))

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.delito, HechoDelictual.modalidad)
    query = query.order_by(desc("cantidad"))

    resultados = query.all()
    total = sum(r.cantidad for r in resultados)

    filas = [
        FilaInforme(
            categoria=r.delito or "Sin dato",
            subcategoria=r.modalidad or "Sin modalidad",
            cantidad=r.cantidad,
            porcentaje=round((r.cantidad / total * 100) if total > 0 else 0, 2),
        )
        for r in resultados
    ]

    return InformeResponse(
        titulo="Delitos con Modalidades",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_dias_semana(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe por día de la semana."""
    query = db.query(
        HechoDelictual.dia_hecho,
        func.count().label("cantidad"),
    ).filter(HechoDelictual.dia_hecho.isnot(None))

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.dia_hecho)

    resultados = {r.dia_hecho: r.cantidad for r in query.all()}
    total = sum(resultados.values())

    filas = []
    for dia in ORDEN_DIAS:
        cantidad = resultados.get(dia, 0)
        filas.append(FilaInforme(
            categoria=dia,
            cantidad=cantidad,
            porcentaje=round((cantidad / total * 100) if total > 0 else 0, 2),
        ))

    return InformeResponse(
        titulo="Hechos por Día de la Semana",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_franja_horaria(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe por franja horaria."""
    query = db.query(
        HechoDelictual.franja_horaria,
        func.count().label("cantidad"),
    ).filter(HechoDelictual.franja_horaria.isnot(None))

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.franja_horaria)

    resultados = {r.franja_horaria: r.cantidad for r in query.all()}
    total = sum(resultados.values())

    filas = []
    # Intentar ordenar por las franjas canónicas, luego agregar las no reconocidas
    franjas_vistas = set()
    for franja in ORDEN_FRANJAS:
        for key, cant in resultados.items():
            if key and franja.split(" ")[0].lower() in key.lower():
                filas.append(FilaInforme(
                    categoria=key,
                    cantidad=cant,
                    porcentaje=round((cant / total * 100) if total > 0 else 0, 2),
                ))
                franjas_vistas.add(key)
                break

    # Agregar franjas no reconocidas
    for key, cant in resultados.items():
        if key not in franjas_vistas:
            filas.append(FilaInforme(
                categoria=key,
                cantidad=cant,
                porcentaje=round((cant / total * 100) if total > 0 else 0, 2),
            ))

    return InformeResponse(
        titulo="Hechos por Franja Horaria",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_movilidad(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe por medio de movilidad utilizado."""
    query = db.query(
        HechoDelictual.vehiculo_utilizado,
        func.count().label("cantidad"),
    ).filter(HechoDelictual.vehiculo_utilizado.isnot(None))

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.vehiculo_utilizado)
    query = query.order_by(desc("cantidad"))

    resultados = query.all()
    total = sum(r.cantidad for r in resultados)

    filas = [
        FilaInforme(
            categoria=r.vehiculo_utilizado or "Sin dato",
            cantidad=r.cantidad,
            porcentaje=round((r.cantidad / total * 100) if total > 0 else 0, 2),
        )
        for r in resultados
    ]

    return InformeResponse(
        titulo="Medios de Movilidad Utilizados",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_armas(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe por arma utilizada (filtrado a robos agravados)."""
    query = db.query(
        HechoDelictual.arma_utilizada,
        func.count().label("cantidad"),
    ).filter(
        HechoDelictual.arma_utilizada.isnot(None),
    )

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.arma_utilizada)
    query = query.order_by(desc("cantidad"))

    resultados = query.all()
    total = sum(r.cantidad for r in resultados)

    filas = [
        FilaInforme(
            categoria=r.arma_utilizada or "Sin dato",
            cantidad=r.cantidad,
            porcentaje=round((r.cantidad / total * 100) if total > 0 else 0, 2),
        )
        for r in resultados
    ]

    return InformeResponse(
        titulo="Armas Utilizadas",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_ambito(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe por ámbito de ocurrencia."""
    query = db.query(
        HechoDelictual.lugar_hecho,
        HechoDelictual.detalle_lugar,
        func.count().label("cantidad"),
    ).filter(HechoDelictual.lugar_hecho.isnot(None))

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.lugar_hecho, HechoDelictual.detalle_lugar)
    query = query.order_by(desc("cantidad"))

    resultados = query.all()
    total = sum(r.cantidad for r in resultados)

    filas = [
        FilaInforme(
            categoria=r.lugar_hecho or "Sin dato",
            subcategoria=r.detalle_lugar,
            cantidad=r.cantidad,
            porcentaje=round((r.cantidad / total * 100) if total > 0 else 0, 2),
        )
        for r in resultados
    ]

    return InformeResponse(
        titulo="Ámbito de Ocurrencia",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_jurisdicciones(db: Session, filtros: FiltrosInforme) -> InformeResponse:
    """Genera informe por jurisdicción."""
    query = db.query(
        HechoDelictual.jurisdiccion,
        func.count().label("cantidad"),
    ).filter(HechoDelictual.jurisdiccion.isnot(None))

    query = _aplicar_filtros(query, filtros)
    query = query.group_by(HechoDelictual.jurisdiccion)
    query = query.order_by(desc("cantidad"))

    resultados = query.all()
    total = sum(r.cantidad for r in resultados)

    filas = [
        FilaInforme(
            categoria=r.jurisdiccion or "Sin dato",
            cantidad=r.cantidad,
            porcentaje=round((r.cantidad / total * 100) if total > 0 else 0, 2),
        )
        for r in resultados
    ]

    return InformeResponse(
        titulo="Hechos por Jurisdicción",
        total=total,
        filas=filas,
        filtros_aplicados=_filtros_dict(filtros),
    )


def informe_comparativo(db: Session, filtros: FiltrosComparativo) -> ComparativoResponse:
    """Genera informe comparativo entre dos períodos."""
    filtros_base = {}
    if filtros.regional:
        filtros_base["regional"] = filtros.regional
    if filtros.comisaria:
        filtros_base["comisaria"] = filtros.comisaria

    # Periodo 1
    q1 = db.query(
        HechoDelictual.delito,
        func.count().label("cantidad"),
    ).filter(
        HechoDelictual.fecha_hecho >= filtros.periodo1_desde,
        HechoDelictual.fecha_hecho <= filtros.periodo1_hasta,
        HechoDelictual.delito.isnot(None),
    )
    if filtros.regional:
        q1 = q1.filter(HechoDelictual.regional == filtros.regional)
    if filtros.comisaria:
        q1 = q1.filter(HechoDelictual.comisaria_origen == filtros.comisaria)
    r1 = {r.delito: r.cantidad for r in q1.group_by(HechoDelictual.delito).all()}

    # Periodo 2
    q2 = db.query(
        HechoDelictual.delito,
        func.count().label("cantidad"),
    ).filter(
        HechoDelictual.fecha_hecho >= filtros.periodo2_desde,
        HechoDelictual.fecha_hecho <= filtros.periodo2_hasta,
        HechoDelictual.delito.isnot(None),
    )
    if filtros.regional:
        q2 = q2.filter(HechoDelictual.regional == filtros.regional)
    if filtros.comisaria:
        q2 = q2.filter(HechoDelictual.comisaria_origen == filtros.comisaria)
    r2 = {r.delito: r.cantidad for r in q2.group_by(HechoDelictual.delito).all()}

    # Combinar
    todos_delitos = sorted(set(list(r1.keys()) + list(r2.keys())))
    total_p1 = sum(r1.values())
    total_p2 = sum(r2.values())

    filas = []
    for delito in todos_delitos:
        c1 = r1.get(delito, 0)
        c2 = r2.get(delito, 0)
        diff = c2 - c1
        pct = round(((c2 - c1) / c1 * 100) if c1 > 0 else (100.0 if c2 > 0 else 0), 2)
        filas.append(ComparativoFila(
            categoria=delito,
            cantidad_periodo1=c1,
            cantidad_periodo2=c2,
            diferencia=diff,
            porcentaje_cambio=pct,
        ))

    filas.sort(key=lambda x: abs(x.diferencia), reverse=True)

    return ComparativoResponse(
        titulo="Comparativo entre Períodos",
        periodo1=f"{filtros.periodo1_desde} a {filtros.periodo1_hasta}",
        periodo2=f"{filtros.periodo2_desde} a {filtros.periodo2_hasta}",
        total_periodo1=total_p1,
        total_periodo2=total_p2,
        filas=filas,
    )


def generar_dashboard(db: Session) -> DashboardResponse:
    """Genera datos para el dashboard principal."""
    total = db.query(func.count(HechoDelictual.id)).scalar() or 0

    total_comisarias = db.query(
        func.count(func.distinct(HechoDelictual.comisaria_origen))
    ).scalar() or 0

    # Hechos del mes actual
    hoy = date.today()
    primer_dia_mes = date(hoy.year, hoy.month, 1)
    hechos_mes = db.query(func.count(HechoDelictual.id)).filter(
        HechoDelictual.fecha_hecho >= primer_dia_mes
    ).scalar() or 0

    # Top delito
    top = db.query(
        HechoDelictual.delito,
        func.count().label("cnt"),
    ).filter(
        HechoDelictual.delito.isnot(None),
    ).group_by(HechoDelictual.delito).order_by(desc("cnt")).first()

    # Última importación
    ultima = db.query(Importacion).order_by(
        desc(Importacion.fecha_importacion)
    ).first()

    # Hechos por mes (últimos 12 meses)
    hechos_por_mes = db.query(
        extract("year", HechoDelictual.fecha_hecho).label("anio"),
        extract("month", HechoDelictual.fecha_hecho).label("mes"),
        func.count().label("cantidad"),
    ).filter(
        HechoDelictual.fecha_hecho.isnot(None),
    ).group_by("anio", "mes").order_by("anio", "mes").limit(24).all()

    meses_data = [
        {"anio": int(r.anio), "mes": int(r.mes), "cantidad": r.cantidad}
        for r in hechos_por_mes
    ]

    return DashboardResponse(
        total_hechos=total,
        total_comisarias=total_comisarias,
        hechos_mes_actual=hechos_mes,
        top_delito=top.delito if top else None,
        top_delito_cantidad=top.cnt if top else 0,
        ultima_importacion=ultima.fecha_importacion.isoformat() if ultima else None,
        hechos_por_mes=meses_data,
    )
