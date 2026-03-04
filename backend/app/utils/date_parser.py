"""Utilidades para parseo de fechas y horas desde los shapefiles."""
import re
from datetime import date, time
from typing import Optional


# Días en español → número para reconstruir fechas
DIAS_ES = {
    "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2,
    "jueves": 3, "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6,
}

# Meses en español
MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}


def parsear_fecha(texto: Optional[str]) -> Optional[date]:
    """
    Parsea fecha desde formato del shapefile.
    Formatos soportados:
      - "miércoles 01-01-2025"
      - "01-01-2025"
      - "2025-01-01"
      - "01/01/2025"
    """
    if not texto or not isinstance(texto, str):
        return None

    texto = texto.strip()

    # Formato: "día_semana DD-MM-YYYY"
    match = re.match(r"^\w+\s+(\d{1,2})-(\d{1,2})-(\d{4})$", texto)
    if match:
        dia, mes, anio = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return date(anio, mes, dia)
        except ValueError:
            return None

    # Formato: "DD-MM-YYYY"
    match = re.match(r"^(\d{1,2})-(\d{1,2})-(\d{4})$", texto)
    if match:
        dia, mes, anio = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return date(anio, mes, dia)
        except ValueError:
            return None

    # Formato: "YYYY-MM-DD"
    match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", texto)
    if match:
        anio, mes, dia = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return date(anio, mes, dia)
        except ValueError:
            return None

    # Formato: "DD/MM/YYYY"
    match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", texto)
    if match:
        dia, mes, anio = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return date(anio, mes, dia)
        except ValueError:
            return None

    return None


def parsear_hora(texto: Optional[str]) -> Optional[time]:
    """
    Parsea hora desde formato "HH:MM:SS" o "HH:MM".
    """
    if not texto or not isinstance(texto, str):
        return None

    texto = texto.strip()
    match = re.match(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", texto)
    if match:
        h, m = int(match.group(1)), int(match.group(2))
        s = int(match.group(3)) if match.group(3) else 0
        if 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59:
            return time(h, m, s)
    return None


def extraer_codigo_delito(delito: Optional[str]) -> Optional[str]:
    """Extrae el código numérico del delito. Ej: '010-ROBO' → '010'."""
    if not delito or not isinstance(delito, str):
        return None
    match = re.match(r"^(\d+)-", delito.strip())
    return match.group(1) if match else None


def limpiar_campo(valor: Optional[str]) -> Optional[str]:
    """Limpia campos con valores especiales del shapefile."""
    if not valor or not isinstance(valor, str):
        return None
    valor = valor.strip()
    # Valores que representan 'sin dato'
    sin_dato = ["{#NO_CONSTA}", "NO CONSTA", "{}", "NaN", "nan", "None", ""]
    if valor in sin_dato:
        return None
    # Quitar llaves envolventes: "{MASCULINO}" → "MASCULINO"
    if valor.startswith("{") and valor.endswith("}"):
        valor = valor[1:-1]
    return valor if valor else None


def normalizar_dia(dia: Optional[str]) -> Optional[str]:
    """Normaliza nombre de día. 'miercoles' → 'Miércoles'."""
    if not dia or not isinstance(dia, str):
        return None
    dia_lower = dia.strip().lower()
    NORMALIZACION = {
        "lunes": "Lunes", "martes": "Martes",
        "miercoles": "Miércoles", "miércoles": "Miércoles",
        "jueves": "Jueves", "viernes": "Viernes",
        "sabado": "Sábado", "sábado": "Sábado",
        "domingo": "Domingo",
    }
    return NORMALIZACION.get(dia_lower, dia.strip().capitalize())


def normalizar_franja(franja: Optional[str]) -> Optional[str]:
    """Normaliza franja horaria. 'VESPERTINA_(09:00-12:59)' → 'Vespertina (09:00-12:59)'."""
    if not franja or not isinstance(franja, str):
        return None
    franja = franja.strip()
    franja = franja.replace("_", " ")
    # Capitalizar solo primera letra
    if franja:
        franja = franja[0].upper() + franja[1:].lower()
        # Re-capitalizar las reglas horarias entre paréntesis
        franja = re.sub(r"\((\d)", lambda m: f"({m.group(1)}", franja)
    return franja
