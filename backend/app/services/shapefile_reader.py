"""Servicio para leer e importar shapefiles a la base de datos."""
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

import geopandas as gpd
import pandas as pd
from sqlalchemy.orm import Session
from shapely.geometry import Point

from app.models import HechoDelictual, Importacion
from app.config import settings, REGIONALES, SHAPES_ESPECIALES, obtener_ruta_shapefile
from app.utils.date_parser import (
    parsear_fecha, parsear_hora, extraer_codigo_delito,
    limpiar_campo, normalizar_dia, normalizar_franja,
)

logger = logging.getLogger(__name__)

# Asegurar encoding
os.environ["SHAPE_ENCODING"] = settings.SHAPE_ENCODING

# Mapeo de columnas del shapefile a campos del modelo
COLUMN_MAP = {
    "ID_N_SRIO": "id_sumario",
    "JURIS_HECH": "jurisdiccion",
    "DPCIA_INT": "dependencia_interviniente",
    "FECHA_HECH": "fecha_hecho_texto",
    "DIA_HECHO": "dia_hecho",
    "HORA_HECH": "hora_hecho_texto",
    "FRAN_HORAR": "franja_horaria",
    "PRDA_URBAN": "predio_urbano",
    "DIREC_HECH": "direccion_hecho",
    "LUGR_HECHO": "lugar_hecho",
    "DET_LUG_HE": "detalle_lugar",
    "DELITO": "delito",
    "MODUS_OPER": "modalidad",
    "VEHIC_UTIL": "vehiculo_utilizado",
    "DET_VEHIC": "detalle_vehiculo",
    "ARMA_UTILI": "arma_utilizada",
    "DET_ARMA": "detalle_arma",
    "ELEMN_SUST": "elementos_sustraidos",
    "DET_ELE_SU": "detalle_elementos",
    "RESEN_HECH": "resena_hecho",
    "SEXO_VICTI": "sexo_victima",
    "EDAD_VICTI": "edad_victima",
    "AP_NOM_VIC": "nombre_victima",
    "DNI_VICTIM": "dni_victima",
    "DIREC_VICT": "direccion_victima",
    "VIN_DE_VIC": "vinculo_victima",
    "AP_NOM_DEN": "nombre_denunciante",
    "DNI_DENUNC": "dni_denunciante",
    "SEXO_DENUN": "sexo_denunciante",
    "EDAD_DENUN": "edad_denunciante",
    "DIREC_DENU": "direccion_denunciante",
    "AP_NOM_CAU": "nombre_causante",
    "SEXO_CAUS": "sexo_causante",
    "EDAD_CAUSA": "edad_causante",
    "DNI_CAUSAN": "dni_causante",
    "DIREC_CAUS": "direccion_causante",
    "DESC_CAUS": "descripcion_causante",
    "SITUA_CAUS": "situacion_causante",
    "HECH_RESUE": "hecho_resuelto",
    "MES_DENU": "mes",
    "Resol_Hech": "resolucion_hecho",
    "ELEM_SECU": "elem_seguridad",
    "DET_EL_SE1": "det_elem_seg_1",
    "DET_EL_SE2": "det_elem_seg_2",
    "DET_EL_SE3": "det_elem_seg_3",
    "fecha_actu": "fecha_actualizacion",
}


def leer_shapefile(ruta: str) -> Optional[gpd.GeoDataFrame]:
    """Lee un shapefile y retorna un GeoDataFrame."""
    if not os.path.exists(ruta):
        logger.warning(f"Shapefile no encontrado: {ruta}")
        return None

    try:
        gdf = gpd.read_file(ruta)
        logger.info(f"Shapefile leído: {ruta} ({len(gdf)} registros)")
        return gdf
    except Exception as e:
        logger.error(f"Error leyendo shapefile {ruta}: {e}")
        return None


def transformar_fila(row: pd.Series, comisaria: str, regional: str) -> dict:
    """Transforma una fila del GeoDataFrame en un dict para el modelo."""
    registro = {}

    # Mapear columnas existentes
    for col_shp, col_db in COLUMN_MAP.items():
        if col_shp in row.index:
            valor = row[col_shp]
            if pd.isna(valor):
                registro[col_db] = None
            else:
                registro[col_db] = str(valor).strip() if valor is not None else None

    # Campos derivados
    registro["fecha_hecho"] = parsear_fecha(registro.get("fecha_hecho_texto"))
    registro["hora_hecho"] = parsear_hora(registro.get("hora_hecho_texto"))
    registro["codigo_delito"] = extraer_codigo_delito(registro.get("delito"))
    registro["dia_hecho"] = normalizar_dia(registro.get("dia_hecho"))
    registro["franja_horaria"] = normalizar_franja(registro.get("franja_horaria"))

    # Limpiar campos con valores especiales
    for campo in ["vehiculo_utilizado", "arma_utilizada", "modalidad",
                   "lugar_hecho", "sexo_victima", "sexo_causante",
                   "edad_victima", "edad_causante", "elementos_sustraidos",
                   "situacion_causante"]:
        if campo in registro:
            registro[campo] = limpiar_campo(registro.get(campo))

    # Coordenadas
    x = row.get("X")
    y = row.get("Y")
    if pd.notna(x) and pd.notna(y):
        try:
            registro["x"] = float(x)
            registro["y"] = float(y)
            registro["geom"] = f"SRID=4326;POINT({float(x)} {float(y)})"
        except (ValueError, TypeError):
            registro["x"] = None
            registro["y"] = None
            registro["geom"] = None
    else:
        registro["x"] = None
        registro["y"] = None
        registro["geom"] = None

    # Metadatos
    registro["comisaria_origen"] = comisaria
    registro["regional"] = regional
    registro["fecha_importacion"] = datetime.utcnow()

    return registro


def importar_shapefile(
    db: Session,
    ruta: str,
    comisaria: str,
    regional: str,
) -> dict:
    """
    Lee un shapefile e importa sus registros a la base de datos.
    Retorna dict con estadísticas de la importación.
    """
    resultado = {
        "archivo": ruta,
        "comisaria": comisaria,
        "regional": regional,
        "registros_importados": 0,
        "registros_error": 0,
        "estado": "completado",
        "mensaje": None,
    }

    gdf = leer_shapefile(ruta)
    if gdf is None:
        resultado["estado"] = "error"
        resultado["mensaje"] = f"No se pudo leer el archivo: {ruta}"
        return resultado

    # Eliminar registros previos de esta comisaría
    eliminados = db.query(HechoDelictual).filter(
        HechoDelictual.comisaria_origen == comisaria,
        HechoDelictual.regional == regional,
    ).delete()
    if eliminados:
        logger.info(f"Eliminados {eliminados} registros previos de {comisaria}")

    registros_batch = []
    for idx, row in gdf.iterrows():
        try:
            datos = transformar_fila(row, comisaria, regional)
            registros_batch.append(HechoDelictual(**datos))
            resultado["registros_importados"] += 1
        except Exception as e:
            resultado["registros_error"] += 1
            logger.error(f"Error en fila {idx} de {comisaria}: {e}")

        # Insertar en batches de 500
        if len(registros_batch) >= 500:
            db.bulk_save_objects(registros_batch)
            db.flush()
            registros_batch = []

    # Insertar restantes
    if registros_batch:
        db.bulk_save_objects(registros_batch)

    db.commit()

    # Registrar importación
    importacion = Importacion(
        archivo=ruta,
        comisaria=comisaria,
        regional=regional,
        registros_importados=resultado["registros_importados"],
        registros_error=resultado["registros_error"],
        estado=resultado["estado"],
        mensaje=resultado["mensaje"],
    )
    db.add(importacion)
    db.commit()

    logger.info(
        f"Importación de {comisaria}: "
        f"{resultado['registros_importados']} OK, "
        f"{resultado['registros_error']} errores"
    )

    return resultado


def importar_regional(db: Session, regional_key: str) -> list[dict]:
    """Importa todos los shapefiles de una regional."""
    if regional_key not in REGIONALES:
        return [{"estado": "error", "mensaje": f"Regional no encontrada: {regional_key}"}]

    regional = REGIONALES[regional_key]
    resultados = []

    for cria in regional["comisarias"]:
        ruta = obtener_ruta_shapefile(
            settings.SHAPES_BASE_PATH,
            cria["carpeta"],
            cria["archivo"],
        )
        resultado = importar_shapefile(db, ruta, cria["nombre"], regional_key)
        resultados.append(resultado)

    return resultados


def importar_todo(db: Session) -> list[dict]:
    """Importa todos los shapefiles de todas las regionales."""
    resultados = []
    for regional_key in REGIONALES:
        resultados.extend(importar_regional(db, regional_key))

    # Importar shapes especiales
    for especial in SHAPES_ESPECIALES:
        ruta = obtener_ruta_shapefile(
            settings.SHAPES_BASE_PATH,
            especial["carpeta"],
            especial["archivo"],
        )
        resultado = importar_shapefile(db, ruta, especial["nombre"], "ESPECIAL")
        resultados.append(resultado)

    return resultados
