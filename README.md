# Sistema de Informes Delictuales — Policía de Tucumán

Sistema integral para la **Sección de Análisis Delictual** de la Policía de Tucumán.  
Lee ~120 shapefiles QGIS desde la unidad de red Z:, importa a PostgreSQL+PostGIS, y genera informes estadísticos con tablas, gráficos y mapa interactivo.

## Funcionalidades

- **8 tipos de informes**: Delitos/Modalidades, Días de la semana, Franja horaria, Movilidad, Armas, Ámbito, Jurisdicciones, Comparativo
- **Mapa interactivo**: Leaflet con clusters de marcadores y puntos delictuales georeferenciados
- **Dashboard**: Resumen ejecutivo con cards y gráficos de tendencia
- **Exportación**: PDF con membrete institucional y Excel
- **Importación**: Lectura automática de shapefiles desde Z:\MAPA DEL DELITO
- **Filtros**: Por regional, comisaría, rango de fechas y tipo de delito

## Stack Tecnológico

| Capa          | Tecnología                             |
| ------------- | -------------------------------------- |
| Frontend      | Next.js 14 + TypeScript + Tailwind CSS |
| Gráficos      | Recharts                               |
| Tablas        | @tanstack/react-table                  |
| Mapas         | Leaflet + MarkerCluster                |
| Backend       | Python 3.13 + FastAPI                  |
| ORM           | SQLAlchemy + GeoAlchemy2               |
| Shapefiles    | GeoPandas                              |
| Base de datos | PostgreSQL 16 + PostGIS 3.4 (Docker)   |

## Estructura del Proyecto

```
├── backend/
│   ├── app/
│   │   ├── config.py          # Configuración y mapeo de comisarías
│   │   ├── database.py        # Engine SQLAlchemy
│   │   ├── models.py          # Modelos ORM (HechoDelictual, etc.)
│   │   ├── schemas.py         # Schemas Pydantic
│   │   ├── main.py            # App FastAPI
│   │   ├── utils/
│   │   │   └── date_parser.py # Parseo de fechas y limpieza
│   │   ├── services/
│   │   │   ├── shapefile_reader.py  # Lectura e importación de .shp
│   │   │   └── data_processor.py    # Generación de informes
│   │   └── routers/
│   │       ├── informes.py    # Endpoints de informes
│   │       ├── mapa.py        # Endpoints de mapa
│   │       ├── datos.py       # Endpoints de importación
│   │       └── filtros.py     # Endpoints de filtros
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/               # Páginas Next.js (App Router)
│   │   ├── components/        # Componentes React
│   │   ├── lib/               # API client, tipos, exportación
│   │   └── hooks/             # Custom hooks
│   └── package.json
├── docker-compose.yml         # PostgreSQL + PostGIS
├── run.bat                    # Iniciar todo el sistema
├── setup.bat                  # Setup inicial
└── .env.example
```

## Requisitos Previos

- **Python 3.11+** (recomendado 3.13)
- **Node.js 18+**
- **Docker Desktop** (para PostgreSQL)
- Acceso a la unidad **Z:\MAPA DEL DELITO**

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/desarrolloramon829-spec/INFORMES-POR-COMISARIAS.git
cd "INFORMES POR COMISARIAS"

# 2. Ejecutar setup automático
setup.bat

# 3. Iniciar el sistema
run.bat
```

## Acceso

| Servicio          | URL                        |
| ----------------- | -------------------------- |
| Frontend          | http://localhost:3000      |
| Backend API       | http://localhost:8000      |
| Documentación API | http://localhost:8000/docs |

## Flujo de Uso

1. Abrir el sistema en el navegador
2. Ir a **Importación** → Importar datos desde los shapefiles
3. Ir a **Dashboard** para ver resumen general
4. Ir a **Informes** → Seleccionar tipo, filtros y generar
5. Exportar a PDF o Excel según necesidad
6. Ir a **Mapa** para visualización geográfica

---

_Sección de Análisis Delictual — Policía de Tucumán_
