"""Configuración central del sistema."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://delitos_user:delitos_pass@localhost:5432/delitos_tucuman"
    SHAPES_BASE_PATH: str = r"Z:\MAPA DEL DELITO\MAPAS DEL DELITO POR JURISDICCIONES"
    SHAPE_ENCODING: str = "latin-1"
    KML_PATH: str = r"Z:\MAPA DEL DELITO\jurisdicciones.kml"
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()

# Establecer encoding para shapefiles globalmente
os.environ["SHAPE_ENCODING"] = settings.SHAPE_ENCODING

# ---------------------------------------------------------------------------
# REGIONALES: mapeo completo de regionales → comisarías → rutas de shapefiles
# Cada ruta es RELATIVA a SHAPES_BASE_PATH
# ---------------------------------------------------------------------------

REGIONALES: dict[str, dict[str, list[dict[str, str]]]] = {
    "NORTE_URN": {
        "nombre": "Unidad Regional Norte (URN)",
        "comisarias": [
            {"nombre": "Trancas", "carpeta": "CRIA TRANCAS-URN-2020", "archivo": "MAPA DELICTUAL CRIA TRANCAS-URN-2020"},
            {"nombre": "Chuscha", "carpeta": "CRIA CHUSCHA-URN-2020", "archivo": "MAPA DELICTUAL CRIA CHUSCHA-URN-2020"},
            {"nombre": "Choromoro", "carpeta": "CRIA CHOROMORO-URN-2020", "archivo": "MAPA DELICTUAL CRIA CHOROMORO-URN-2020"},
            {"nombre": "Vipos", "carpeta": "CRIA VIPOS-URN-2020", "archivo": "MAPA DELICTUAL CRIA VIPOS-URN-2020"},
            {"nombre": "Tapia", "carpeta": "CRIA TAPIA-URN-2020", "archivo": "MAPA DELICTUAL CRIA TAPIA-URN-2020"},
            {"nombre": "San Pedro de Colalao", "carpeta": "CRIA SAN PEDRO DE COLALAO-URN-2020", "archivo": "MAPA DELICTUAL CRIA SAN PEDRO DE COLALAO-URN-2020"},
            {"nombre": "Yerba Buena", "carpeta": "CRIA YERBA BUENA-URN-2020", "archivo": "MAPA DELICTUAL CRIA YERBA BUENA-URN-2020"},
            {"nombre": "Marti Coll", "carpeta": "CRIA MARTI COLL-URN-2020", "archivo": "MAPA DELICTUAL CRIA MARTI COLL-URN-2020"},
            {"nombre": "San José", "carpeta": "CRIA SAN JOSE-URN-2020", "archivo": "MAPA DELICTUAL CRIA SAN JOSE-URN-2020"},
            {"nombre": "El Corte", "carpeta": "CRIA EL CORTE-URN-2020", "archivo": "MAPA DELICTUAL CRIA EL CORTE-URN-2020"},
            {"nombre": "San Javier", "carpeta": "CRIA SAN JAVIER-URN-2020", "archivo": "MAPA DELICTUAL CRIA SAN JAVIER-URN-2020"},
            {"nombre": "Villa Carmela", "carpeta": "CRIA VILLA CARMELA-URN-URC-2020", "archivo": "MAPA DELICTUAL CRIA VILLA CARMELA-URN-URC-2020"},
            {"nombre": "Raco", "carpeta": "CRIA RACO-URN-2020", "archivo": "MAPA DELICTUAL CRIA RACO-URN-2020"},
            {"nombre": "Los Nogales", "carpeta": "CRIA LOS NOGALES-URN-2020", "archivo": "MAPA DELICTUAL CRIA LOS NOGALES-URN-2020"},
            {"nombre": "El Cadillal", "carpeta": "CRIA EL CADILLAL-URN-2020", "archivo": "MAPA DELICTUAL CRIA EL CADILLAL-URN-2020"},
            {"nombre": "Las Talitas", "carpeta": "CRIA LAS TALITAS-URN-2020", "archivo": "MAPA DELICTUAL CRIA LAS TALITAS-URN-2020"},
            {"nombre": "V. Mariano Moreno", "carpeta": "CRIA V MARIANO MORENO-URN-2020", "archivo": "MAPA DELICTUAL CRIA V MARIANO MORENO-URN-2020"},
            {"nombre": "El Colmenar", "carpeta": "CRIA EL COLMENAR-URN-2020", "archivo": "MAPA DELICTUAL CRIA EL COLMENAR-URN-2020"},
            {"nombre": "Los Pocitos", "carpeta": "CRIA LOS POCITOS-URN-2020", "archivo": "MAPA DELICTUAL CRIA LOS POCITOS-URN-2020"},
            {"nombre": "Lomas de Tafí", "carpeta": "CRIA LOMAS DE TAFI-URN-2020", "archivo": "MAPA DELICTUAL CRIA LOMAS DE TAFI-URN-2020"},
            {"nombre": "Villa Obrera", "carpeta": "CRIA VILLA OBRERA-URN-2020", "archivo": "MAPA DELICTUAL CRIA VILLA OBRERA-URN-2020"},
            {"nombre": "Tafí Viejo", "carpeta": "CRIA TAFI VIEJO-URN-2020", "archivo": "MAPA DELICTUAL CRIA TAFI VIEJO-URN-2020"},
        ],
    },
    "CAPITAL_URC": {
        "nombre": "Unidad Regional Capital (URC)",
        "comisarias": [
            {"nombre": "Comisaría 1ª", "carpeta": "CRIA1-URC- 2020", "archivo": "MAPA DELICTUAL CRIA1-URC-2020"},
            {"nombre": "Comisaría 2ª", "carpeta": "CRIA2-URC-2020", "archivo": "MAPA DELICTUAL CRIA2-URC-2020"},
            {"nombre": "Comisaría 3ª", "carpeta": "CRIA3-URC-2020", "archivo": "MAPA DELICTUAL CRIA3-URC-2020"},
            {"nombre": "Comisaría 4ª", "carpeta": "CRIA4-URC-2020", "archivo": "MAPA DELICTUAL CRIA4-URC-2020"},
            {"nombre": "Comisaría 5ª", "carpeta": "CRIA5-URC-2020", "archivo": "MAPA DELICTUAL CRIA5-URC-2020"},
            {"nombre": "Comisaría 6ª", "carpeta": "CRIA6-URC-2020", "archivo": "MAPA DELICTUAL CRIA6-URC-2020"},
            {"nombre": "Comisaría 7ª", "carpeta": "CRIA7-URC-2020", "archivo": "MAPA DELICTUAL CRIA7-URC-2020"},
            {"nombre": "Comisaría 8ª", "carpeta": "CRIA8-URC-2020", "archivo": "MAPA DELICTUAL CRIA8-URC-2020"},
            {"nombre": "Comisaría 9ª", "carpeta": "CRIA9-URC-2020", "archivo": "MAPA DELICTUAL CRIA9-URC-2020"},
            {"nombre": "Comisaría 10ª", "carpeta": "CRIA10-URC-2020", "archivo": "MAPA DELICTUAL CRIA10-URC-2020"},
            {"nombre": "Comisaría 11ª", "carpeta": "CRIA11-URC-2020", "archivo": "MAPA DELICTUAL CRIA11-URC-2020"},
            {"nombre": "Comisaría 12ª", "carpeta": "CRIA12-URC-2020", "archivo": "MAPA DELICTUAL CRIA12-URC-2020"},
            {"nombre": "Comisaría 13ª", "carpeta": "CRIA13-URC-2020", "archivo": "MAPA DELICTUAL CRIA13-URC-2020"},
            {"nombre": "Comisaría 14ª", "carpeta": "CRIA14-URC-2020", "archivo": "MAPA DELICTUAL CRIA14-URC-2020"},
            {"nombre": "Comisaría 15ª", "carpeta": "CRIA15-URC-2020", "archivo": "MAPA DELICTUAL CRIA15-URC-2020"},
        ],
    },
    "ESTE_URE": {
        "nombre": "Unidad Regional Este (URE)",
        "comisarias": [
            {"nombre": "Burruyacú", "carpeta": "CRIA BURRUYACU-URE-2020", "archivo": "MAPA DELICTUAL CRIA BURRUYACU-URE-2020"},
            {"nombre": "El Bracho", "carpeta": "CRIA EL BRACHO-URE-2020", "archivo": "MAPA DELICTUAL CRIA EL BRACHO-URE-2020"},
            {"nombre": "Cruz Alta", "carpeta": "CRIA CRUZ ALTA-URE-2020", "archivo": "MAPA DELICTUAL CRIA CRUZ ALTA-URE-2020"},
            {"nombre": "Banda del Río Salí", "carpeta": "CRIA BANDA DEL RIO SALI-URE-2020", "archivo": "MAPA DELICTUAL CRIA BANDA DEL RIO SALI-URE-2020"},
            {"nombre": "Alderetes", "carpeta": "CRIA ALDERETES-URE-2020", "archivo": "MAPA DELICTUAL CRIA ALDERETES-URE-2020"},
            {"nombre": "Los Gutiérrez", "carpeta": "CRIA LOS GUTIERREZ-URE-2020", "archivo": "MAPA DELICTUAL CRIA LOS GUTIERREZ-URE-2020"},
            {"nombre": "Lastenia", "carpeta": "CRIA LASTENIA-URE-2020", "archivo": "MAPA DELICTUAL CRIA LASTENIA-URE-2020"},
            {"nombre": "Colombres", "carpeta": "CRIA COLOMBRES-URE-2020", "archivo": "MAPA DELICTUAL CRIA COLOMBRES-URE-2020"},
            {"nombre": "La Florida", "carpeta": "CRIA LA FLORIDA-URE-2020", "archivo": "MAPA DELICTUAL CRIA LA FLORIDA-URE-2020"},
            {"nombre": "Delfín Gallo", "carpeta": "CRIA DELFIN GALLO-URE-2020", "archivo": "MAPA DELICTUAL CRIA DELFIN GALLO-URE-2020"},
            {"nombre": "San Andrés", "carpeta": "CRIA SAN ANDRES-URE-2020", "archivo": "MAPA DELICTUAL CRIA SAN ANDRES-URE-2020"},
            {"nombre": "El Manantial", "carpeta": "CRIA EL MANANTIAL-URE-2020", "archivo": "MAPA DELICTUAL CRIA EL MANANTIAL-URE-2020"},
            {"nombre": "Los Ralos", "carpeta": "CRIA LOS RALOS-URE-2020", "archivo": "MAPA DELICTUAL CRIA LOS RALOS-URE-2020"},
            {"nombre": "San Miguel de Tucumán Este", "carpeta": "CRIA SMT ESTE-URE-2020", "archivo": "MAPA DELICTUAL CRIA SMT ESTE-URE-2020"},
            {"nombre": "Lules", "carpeta": "CRIA LULES-URE-2020", "archivo": "MAPA DELICTUAL CRIA LULES-URE-2020"},
            {"nombre": "San Pablo", "carpeta": "CRIA SAN PABLO-URE-2020", "archivo": "MAPA DELICTUAL CRIA SAN PABLO-URE-2020"},
            {"nombre": "Villa Quinteros", "carpeta": "CRIA VILLA QUINTEROS-URE-2020", "archivo": "MAPA DELICTUAL CRIA VILLA QUINTEROS-URE-2020"},
            {"nombre": "Famaillá", "carpeta": "CRIA FAMAILLA-URE-2020", "archivo": "MAPA DELICTUAL CRIA FAMAILLA-URE-2020"},
            {"nombre": "Monteros", "carpeta": "CRIA MONTEROS-URE-2020", "archivo": "MAPA DELICTUAL CRIA MONTEROS-URE-2020"},
            {"nombre": "Río Seco", "carpeta": "CRIA RIO SECO-URE-2020", "archivo": "MAPA DELICTUAL CRIA RIO SECO-URE-2020"},
            {"nombre": "Simoca", "carpeta": "CRIA SIMOCA-URE-2020", "archivo": "MAPA DELICTUAL CRIA SIMOCA-URE-2020"},
            {"nombre": "Monteagudo", "carpeta": "CRIA MONTEAGUDO-URE-2020", "archivo": "MAPA DELICTUAL CRIA MONTEAGUDO-URE-2020"},
            {"nombre": "Santa Rosa de Leales", "carpeta": "CRIA SANTA ROSA DE LEALES-URE-2020", "archivo": "MAPA DELICTUAL CRIA SANTA ROSA DE LEALES-URE-2020"},
            {"nombre": "Villa de Leales", "carpeta": "CRIA VILLA DE LEALES-URE-2020", "archivo": "MAPA DELICTUAL CRIA VILLA DE LEALES-URE-2020"},
            {"nombre": "Bella Vista", "carpeta": "CRIA BELLA VISTA-URE-2020", "archivo": "MAPA DELICTUAL CRIA BELLA VISTA-URE-2020"},
            {"nombre": "Aguilares", "carpeta": "CRIA AGUILARES-URE-2020", "archivo": "MAPA DELICTUAL CRIA AGUILARES-URE-2020"},
            {"nombre": "Juan B. Alberdi", "carpeta": "CRIA JUAN B ALBERDI-URE-2020", "archivo": "MAPA DELICTUAL CRIA JUAN B ALBERDI-URE-2020"},
            {"nombre": "La Cocha", "carpeta": "CRIA LA COCHA-URE-2020", "archivo": "MAPA DELICTUAL CRIA LA COCHA-URE-2020"},
            {"nombre": "Graneros", "carpeta": "CRIA GRANEROS-URE-2020", "archivo": "MAPA DELICTUAL CRIA GRANEROS-URE-2020"},
            {"nombre": "Lamadrid", "carpeta": "CRIA LAMADRID-URE-2020", "archivo": "MAPA DELICTUAL CRIA LAMADRID-URE-2020"},
            {"nombre": "Concepción (URE)", "carpeta": "CRIA CONCEPCION-URE-2020", "archivo": "MAPA DELICTUAL CRIA CONCEPCION-URE-2020"},
            {"nombre": "Chicligasta", "carpeta": "CRIA CHICLIGASTA-URE-2020", "archivo": "MAPA DELICTUAL CRIA CHICLIGASTA-URE-2020"},
            {"nombre": "Medinas", "carpeta": "CRIA MEDINAS-URE-2020", "archivo": "MAPA DELICTUAL CRIA MEDINAS-URE-2020"},
            {"nombre": "Santa Ana", "carpeta": "CRIA SANTA ANA-URE-2020", "archivo": "MAPA DELICTUAL CRIA SANTA ANA-URE-2020"},
            {"nombre": "San Felipe", "carpeta": "CRIA SAN FELIPE-URE-2020", "archivo": "MAPA DELICTUAL CRIA SAN FELIPE-URE-2020"},
            {"nombre": "Atahona", "carpeta": "CRIA ATAHONA-URE-2020", "archivo": "MAPA DELICTUAL CRIA ATAHONA-URE-2020"},
            {"nombre": "Ranchillos", "carpeta": "CRIA RANCHILLOS-URE-2020", "archivo": "MAPA DELICTUAL CRIA RANCHILLOS-URE-2020"},
            {"nombre": "Villa Belgrano", "carpeta": "CRIA VILLA BELGRANO-URE-2020", "archivo": "MAPA DELICTUAL CRIA VILLA BELGRANO-URE-2020"},
            {"nombre": "Pacará", "carpeta": "CRIA PACARA-URE-2020", "archivo": "MAPA DELICTUAL CRIA PACARA-URE-2020"},
            {"nombre": "Agua Dulce", "carpeta": "CRIA AGUA DULCE-URE-2020", "archivo": "MAPA DELICTUAL CRIA AGUA DULCE-URE-2020"},
            {"nombre": "Río Colorado", "carpeta": "CRIA RIO COLORADO-URE-2020", "archivo": "MAPA DELICTUAL CRIA RIO COLORADO-URE-2020"},
            {"nombre": "Los Sarmientos", "carpeta": "CRIA LOS SARMIENTOS-URE-2020", "archivo": "MAPA DELICTUAL CRIA LOS SARMIENTOS-URE-2020"},
            {"nombre": "Monte Bello", "carpeta": "CRIA MONTE BELLO-URE-2020", "archivo": "MAPA DELICTUAL CRIA MONTE BELLO-URE-2020"},
            {"nombre": "Campo El Quimil", "carpeta": "CRIA CAMPO EL QUIMIL-URE-2020", "archivo": "MAPA DELICTUAL CRIA CAMPO EL QUIMIL-URE-2020"},
        ],
    },
    "OESTE_URO": {
        "nombre": "Unidad Regional Oeste (URO)",
        "comisarias": [
            {"nombre": "Tafí del Valle", "carpeta": "CRIA TAFI DEL VALLE-URO-2020", "archivo": "MAPA DELICTUAL CRIA TAFI DEL VALLE-URO-2020"},
            {"nombre": "Amaicha del Valle", "carpeta": "CRIA AMAICHA DEL VALLE-URO-2020", "archivo": "MAPA DELICTUAL CRIA AMAICHA DEL VALLE-URO-2020"},
            {"nombre": "Colalao del Valle", "carpeta": "CRIA COLALAO DEL VALLE-URO-2020", "archivo": "MAPA DELICTUAL CRIA COLALAO DEL VALLE-URO-2020"},
            {"nombre": "El Mollar", "carpeta": "CRIA EL MOLLAR-URO-2020", "archivo": "MAPA DELICTUAL CRIA EL MOLLAR-URO-2020"},
            {"nombre": "Quilmes", "carpeta": "CRIA QUILMES-URO-2020", "archivo": "MAPA DELICTUAL CRIA QUILMES-URO-2020"},
            {"nombre": "El Siambón", "carpeta": "CRIA EL SIAMBON-URO-2020", "archivo": "MAPA DELICTUAL CRIA EL SIAMBON-URO-2020"},
            {"nombre": "Anfama", "carpeta": "CRIA ANFAMA-URO-2020", "archivo": "MAPA DELICTUAL CRIA ANFAMA-URO-2020"},
            {"nombre": "La Angostura", "carpeta": "CRIA LA ANGOSTURA-URO-2020", "archivo": "MAPA DELICTUAL CRIA LA ANGOSTURA-URO-2020"},
            {"nombre": "Los Sosa", "carpeta": "CRIA LOS SOSA-URO-2020", "archivo": "MAPA DELICTUAL CRIA LOS SOSA-URO-2020"},
            {"nombre": "Capitán Cáceres", "carpeta": "CRIA CAPITAN CACERES-URO-2020", "archivo": "MAPA DELICTUAL CRIA CAPITAN CACERES-URO-2020"},
            {"nombre": "Santa Lucía", "carpeta": "CRIA SANTA LUCIA-URO-2020", "archivo": "MAPA DELICTUAL CRIA SANTA LUCIA-URO-2020"},
            {"nombre": "Acheral", "carpeta": "CRIA ACHERAL-URO-2020", "archivo": "MAPA DELICTUAL CRIA ACHERAL-URO-2020"},
            {"nombre": "Alpachiri", "carpeta": "CRIA ALPACHIRI-URO-2020", "archivo": "MAPA DELICTUAL CRIA ALPACHIRI-URO-2020"},
            {"nombre": "Río Chico", "carpeta": "CRIA RIO CHICO-URO-2020", "archivo": "MAPA DELICTUAL CRIA RIO CHICO-URO-2020"},
            {"nombre": "Aguilar", "carpeta": "CRIA AGUILAR-URO-2020", "archivo": "MAPA DELICTUAL CRIA AGUILAR-URO-2020"},
            {"nombre": "León Rouges", "carpeta": "CRIA LEON ROUGES-URO-2020", "archivo": "MAPA DELICTUAL CRIA LEON ROUGES-URO-2020"},
            {"nombre": "Pueblo Viejo", "carpeta": "CRIA PUEBLO VIEJO-URO-2020", "archivo": "MAPA DELICTUAL CRIA PUEBLO VIEJO-URO-2020"},
            {"nombre": "Amberes", "carpeta": "CRIA AMBERES-URO-2020", "archivo": "MAPA DELICTUAL CRIA AMBERES-URO-2020"},
            {"nombre": "Teniente Berdina", "carpeta": "CRIA TENIENTE BERDINA-URO-2020", "archivo": "MAPA DELICTUAL CRIA TENIENTE BERDINA-URO-2020"},
            {"nombre": "Soldado Maldonado", "carpeta": "CRIA SOLDADO MALDONADO-URO-2020", "archivo": "MAPA DELICTUAL CRIA SOLDADO MALDONADO-URO-2020"},
            {"nombre": "Sargento Moya", "carpeta": "CRIA SARGENTO MOYA-URO-2020", "archivo": "MAPA DELICTUAL CRIA SARGENTO MOYA-URO-2020"},
            {"nombre": "Yerba Buena (URO)", "carpeta": "CRIA YERBA BUENA-URO-2020", "archivo": "MAPA DELICTUAL CRIA YERBA BUENA-URO-2020"},
        ],
    },
    "SUR_URS": {
        "nombre": "Unidad Regional Sur (URS)",
        "comisarias": [
            {"nombre": "Concepción", "carpeta": "CRIA CONCEPCION-URS-2020", "archivo": "MAPA DELICTUAL CRIA CONCEPCION-URS-2020"},
            {"nombre": "San Antonio", "carpeta": "CRIA SAN ANTONIO-URS-2020", "archivo": "MAPA DELICTUAL CRIA SAN ANTONIO-URS-2020"},
            {"nombre": "Arcadia", "carpeta": "CRIA ARCADIA-URS-2020", "archivo": "MAPA DELICTUAL CRIA ARCADIA-URS-2020"},
            {"nombre": "Alpachiri (URS)", "carpeta": "CRIA ALPACHIRI-URS-2020", "archivo": "MAPA DELICTUAL CRIA ALPACHIRI-URS-2020"},
            {"nombre": "Río Chico (URS)", "carpeta": "CRIA RIO CHICO-URS-2020", "archivo": "MAPA DELICTUAL CRIA RIO CHICO-URS-2020"},
            {"nombre": "Gastona", "carpeta": "CRIA GASTONA-URS-2020", "archivo": "MAPA DELICTUAL CRIA GASTONA-URS-2020"},
            {"nombre": "Atahona (URS)", "carpeta": "CRIA ATAHONA-URS-2020", "archivo": "MAPA DELICTUAL CRIA ATAHONA-URS-2020"},
            {"nombre": "Trinidad", "carpeta": "CRIA TRINIDAD-URS-2020", "archivo": "MAPA DELICTUAL CRIA TRINIDAD-URS-2020"},
            {"nombre": "Los Puestos", "carpeta": "CRIA LOS PUESTOS-URS-2020", "archivo": "MAPA DELICTUAL CRIA LOS PUESTOS-URS-2020"},
            {"nombre": "Ingenio La Trinidad", "carpeta": "CRIA INGENIO LA TRINIDAD-URS-2020", "archivo": "MAPA DELICTUAL CRIA INGENIO LA TRINIDAD-URS-2020"},
            {"nombre": "Medina", "carpeta": "CRIA MEDINA-URS-2020", "archivo": "MAPA DELICTUAL CRIA MEDINA-URS-2020"},
            {"nombre": "Yánima", "carpeta": "CRIA YANIMA-URS-2020", "archivo": "MAPA DELICTUAL CRIA YANIMA-URS-2020"},
            {"nombre": "Huasa Pampa", "carpeta": "CRIA HUASA PAMPA-URS-2020", "archivo": "MAPA DELICTUAL CRIA HUASA PAMPA-URS-2020"},
            {"nombre": "Villa Alberdi", "carpeta": "CRIA VILLA ALBERDI-URS-2020", "archivo": "MAPA DELICTUAL CRIA VILLA ALBERDI-URS-2020"},
            {"nombre": "Escaba", "carpeta": "CRIA ESCABA-URS-2020", "archivo": "MAPA DELICTUAL CRIA ESCABA-URS-2020"},
            {"nombre": "Cóncaran", "carpeta": "CRIA CONCARAN-URS-2020", "archivo": "MAPA DELICTUAL CRIA CONCARAN-URS-2020"},
            {"nombre": "La Ramada", "carpeta": "CRIA LA RAMADA-URS-2020", "archivo": "MAPA DELICTUAL CRIA LA RAMADA-URS-2020"},
            {"nombre": "Alto Verde", "carpeta": "CRIA ALTO VERDE-URS-2020", "archivo": "MAPA DELICTUAL CRIA ALTO VERDE-URS-2020"},
            {"nombre": "Iltico", "carpeta": "CRIA ILTICO-URS-2020", "archivo": "MAPA DELICTUAL CRIA ILTICO-URS-2020"},
            {"nombre": "Ingenio La Corona", "carpeta": "CRIA INGENIO LA CORONA-URS-2020", "archivo": "MAPA DELICTUAL CRIA INGENIO LA CORONA-URS-2020"},
            {"nombre": "Aguilares (URS)", "carpeta": "CRIA AGUILARES-URS-2020", "archivo": "MAPA DELICTUAL CRIA AGUILARES-URS-2020"},
            {"nombre": "Monteros (URS)", "carpeta": "CRIA MONTEROS-URS-2020", "archivo": "MAPA DELICTUAL CRIA MONTEROS-URS-2020"},
            {"nombre": "Villa Quinteros (URS)", "carpeta": "CRIA VILLA QUINTEROS-URS-2020", "archivo": "MAPA DELICTUAL CRIA VILLA QUINTEROS-URS-2020"},
            {"nombre": "Famaillá (URS)", "carpeta": "CRIA FAMAILLA-URS-2020", "archivo": "MAPA DELICTUAL CRIA FAMAILLA-URS-2020"},
            {"nombre": "Simoca (URS)", "carpeta": "CRIA SIMOCA-URS-2020", "archivo": "MAPA DELICTUAL CRIA SIMOCA-URS-2020"},
            {"nombre": "Santa Ana (URS)", "carpeta": "CRIA SANTA ANA-URS-2020", "archivo": "MAPA DELICTUAL CRIA SANTA ANA-URS-2020"},
            {"nombre": "Bella Vista (URS)", "carpeta": "CRIA BELLA VISTA-URS-2020", "archivo": "MAPA DELICTUAL CRIA BELLA VISTA-URS-2020"},
        ],
    },
}

# Shapes especiales (no pertenecen a una regional específica)
SHAPES_ESPECIALES: list[dict[str, str]] = [
    {"nombre": "Fincas", "carpeta": "FINCAS-2020", "archivo": "MAPA DELICTUAL FINCAS-2020"},
    {"nombre": "Abigeato", "carpeta": "ABIGEATO-2020", "archivo": "MAPA DELICTUAL ABIGEATO-2020"},
]


def obtener_ruta_shapefile(base_path: str, carpeta: str, archivo: str) -> str:
    """Construir la ruta completa al archivo .shp."""
    return str(Path(base_path) / carpeta / archivo / f"{archivo}.shp")


def listar_todas_comisarias() -> list[dict]:
    """Retorna lista plana de todas las comisarías con su regional."""
    resultado = []
    for regional_key, regional_data in REGIONALES.items():
        for cria in regional_data["comisarias"]:
            resultado.append({
                "regional": regional_key,
                "regional_nombre": regional_data["nombre"],
                "comisaria": cria["nombre"],
                "carpeta": cria["carpeta"],
                "archivo": cria["archivo"],
            })
    return resultado
