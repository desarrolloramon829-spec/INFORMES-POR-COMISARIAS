"""Modelos SQLAlchemy para la base de datos."""
from datetime import date, time, datetime
from sqlalchemy import (
    Column, Integer, String, Date, Time, DateTime, Float, Boolean, Text, Index
)
from geoalchemy2 import Geometry
from app.database import Base


class HechoDelictual(Base):
    """Tabla principal de hechos delictuales importados desde shapefiles."""
    __tablename__ = "hechos_delictuales"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # --- Identificación ---
    id_sumario = Column(String(100), index=True)         # ID_N_SRIO
    jurisdiccion = Column(String(100), index=True)       # JURIS_HECH
    dependencia_interviniente = Column(String(100))      # DPCIA_INT

    # --- Temporal ---
    fecha_hecho = Column(Date, index=True)               # FECHA_HECH (parseado)
    fecha_hecho_texto = Column(String(100))              # FECHA_HECH (original)
    dia_hecho = Column(String(30), index=True)           # DIA_HECHO
    hora_hecho = Column(Time, nullable=True)             # HORA_HECH (parseado)
    hora_hecho_texto = Column(String(30))                # HORA_HECH (original)
    franja_horaria = Column(String(60), index=True)      # FRAN_HORAR
    mes = Column(String(30))                             # MES_DENU

    # --- Ubicación ---
    predio_urbano = Column(String(10))                   # PRDA_URBAN
    direccion_hecho = Column(String(300))                # DIREC_HECH
    lugar_hecho = Column(String(100), index=True)        # LUGR_HECHO
    detalle_lugar = Column(String(100))                  # DET_LUG_HE

    # --- Delito ---
    delito = Column(String(150), index=True)             # DELITO
    codigo_delito = Column(String(10), index=True)       # Extraído de DELITO
    modalidad = Column(String(150), index=True)          # MODUS_OPER
    vehiculo_utilizado = Column(String(100))             # VEHIC_UTIL
    detalle_vehiculo = Column(String(200))               # DET_VEHIC
    arma_utilizada = Column(String(100), index=True)     # ARMA_UTILI
    detalle_arma = Column(String(200))                   # DET_ARMA
    elementos_sustraidos = Column(String(200))           # ELEMN_SUST
    detalle_elementos = Column(Text)                     # DET_ELE_SU
    resena_hecho = Column(Text)                          # RESEN_HECH

    # --- Víctima ---
    sexo_victima = Column(String(30))                    # SEXO_VICTI
    edad_victima = Column(String(20))                    # EDAD_VICTI
    nombre_victima = Column(String(200))                 # AP_NOM_VIC
    dni_victima = Column(String(30))                     # DNI_VICTIM
    direccion_victima = Column(String(300))              # DIREC_VICT
    vinculo_victima = Column(String(100))                # VIN_DE_VIC

    # --- Denunciante ---
    nombre_denunciante = Column(String(200))             # AP_NOM_DEN
    dni_denunciante = Column(String(30))                 # DNI_DENUNC
    sexo_denunciante = Column(String(30))                # SEXO_DENUN
    edad_denunciante = Column(String(20))                # EDAD_DENUN
    direccion_denunciante = Column(String(300))          # DIREC_DENU

    # --- Causante ---
    nombre_causante = Column(String(300))                # AP_NOM_CAU
    sexo_causante = Column(String(50))                   # SEXO_CAUS
    edad_causante = Column(String(30))                   # EDAD_CAUSA
    dni_causante = Column(String(30))                    # DNI_CAUSAN
    direccion_causante = Column(String(300))             # DIREC_CAUS
    descripcion_causante = Column(Text)                  # DESC_CAUS
    situacion_causante = Column(String(100))             # SITUA_CAUS

    # --- Resolución ---
    hecho_resuelto = Column(String(10))                  # HECH_RESUE
    resolucion_hecho = Column(String(100))               # Resol_Hech

    # --- Elementos de seguridad ---
    elem_seguridad = Column(String(100))                 # ELEM_SECU
    det_elem_seg_1 = Column(String(200))                 # DET_EL_SE1
    det_elem_seg_2 = Column(String(200))                 # DET_EL_SE2
    det_elem_seg_3 = Column(String(200))                 # DET_EL_SE3

    # --- Geoespacial ---
    x = Column(Float)                                   # X (longitud)
    y = Column(Float)                                   # Y (latitud)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)

    # --- Metadatos ---
    comisaria_origen = Column(String(100), index=True)   # Derivado del archivo fuente
    regional = Column(String(50), index=True)            # Derivado del mapeo
    fecha_actualizacion = Column(String(50))             # fecha_actu
    fecha_importacion = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_hechos_regional_fecha", "regional", "fecha_hecho"),
        Index("ix_hechos_comisaria_fecha", "comisaria_origen", "fecha_hecho"),
        Index("ix_hechos_delito_modal", "delito", "modalidad"),
        Index("ix_hechos_geom", "geom", postgresql_using="gist"),
    )


class Jurisdiccion(Base):
    """Polígonos de jurisdicciones importados desde KML."""
    __tablename__ = "jurisdicciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), index=True)
    regional = Column(String(50), index=True)
    geom = Column(Geometry("MULTIPOLYGON", srid=4326))

    __table_args__ = (
        Index("ix_jurisdicciones_geom", "geom", postgresql_using="gist"),
    )


class Importacion(Base):
    """Registro de importaciones realizadas."""
    __tablename__ = "importaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    archivo = Column(String(500))
    comisaria = Column(String(100))
    regional = Column(String(50))
    registros_importados = Column(Integer, default=0)
    registros_error = Column(Integer, default=0)
    fecha_importacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(30), default="completado")  # completado, error, en_progreso
    mensaje = Column(Text, nullable=True)
