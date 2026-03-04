/* ---- Filtros ---- */
export interface FiltrosInforme {
  regional?: string;
  comisaria?: string;
  fecha_desde?: string;
  fecha_hasta?: string;
  delito?: string;
}

export interface FiltrosComparativo {
  regional?: string;
  comisaria?: string;
  fecha_desde_1?: string;
  fecha_hasta_1?: string;
  fecha_desde_2?: string;
  fecha_hasta_2?: string;
}

/* ---- Informes ---- */
export interface FilaInforme {
  [key: string]: unknown;
  categoria: string;
  subcategoria?: string;
  cantidad: number;
  porcentaje: number;
}

export interface InformeResponse {
  titulo: string;
  total: number;
  filas: FilaInforme[];
  filtros_aplicados: Record<string, string>;
}

export interface ComparativoFila {
  categoria: string;
  cantidad_periodo1: number;
  cantidad_periodo2: number;
  diferencia: number;
  porcentaje_cambio?: number;
}

export interface ComparativoResponse {
  titulo: string;
  periodo1: string;
  periodo2: string;
  total_periodo_1: number;
  total_periodo_2: number;
  filas: FilaInforme[];
}

export interface InformeCompleto {
  delitos_modalidades: InformeResponse;
  dias_semana: InformeResponse;
  franja_horaria: InformeResponse;
  movilidad: InformeResponse;
  armas: InformeResponse;
  ambito: InformeResponse;
  jurisdicciones: InformeResponse;
}

/* ---- Mapa ---- */
export interface PuntoMapa {
  id: number;
  latitud: number;
  longitud: number;
  delito: string;
  modalidad?: string;
  fecha?: string;
  hora?: string;
  direccion?: string;
  jurisdiccion?: string;
}

export interface PuntosMapaResponse {
  total: number;
  puntos: PuntoMapa[];
}

export interface JurisdiccionFeature {
  type: 'Feature';
  properties: {
    id: number;
    nombre: string;
    regional: string;
  };
  geometry: GeoJSON.Geometry;
}

export interface JurisdiccionesGeoJSON {
  type: 'FeatureCollection';
  features: JurisdiccionFeature[];
}

/* ---- Filtros disponibles ---- */
export interface RegionalInfo {
  codigo: string;
  nombre: string;
  total_comisarias: number;
}

export interface ComisariaInfo {
  codigo: string;
  nombre: string;
  regional: string;
}

export interface FiltrosDisponibles {
  regionales: RegionalInfo[];
  delitos?: string[];
  fecha_min?: string;
  fecha_max?: string;
}

/* ---- Importación ---- */
export interface ImportacionInfo {
  id: number;
  archivo_origen: string;
  comisaria: string;
  regional: string;
  registros_importados: number;
  registros_error: number;
  estado: string;
  fecha_importacion: string;
  mensaje?: string;
}

export interface EstadoImportacion {
  total_registros: number;
  total_comisarias_importadas: number;
  total_comisarias_disponibles: number;
  importaciones: ImportacionInfo[];
}

/* ---- Dashboard ---- */
export interface DashboardResponse {
  total_hechos: number;
  total_comisarias: number;
  hechos_mes_actual: number;
  top_delito?: string;
  top_delito_cantidad: number;
  jurisdicciones_activas: number;
  delitos_top: FilaInforme[];
  por_dia: FilaInforme[];
  por_franja: FilaInforme[];
  ultima_importacion?: string;
  hechos_por_mes: { anio: number; mes: number; cantidad: number }[];
}

/* ---- Tabs ---- */
export type TipoInforme =
  | 'delitos_modalidades'
  | 'dias_semana'
  | 'franja_horaria'
  | 'movilidad'
  | 'armas'
  | 'ambito'
  | 'jurisdicciones'
  | 'comparativo';

export const TIPOS_INFORME: { key: TipoInforme; label: string }[] = [
  { key: 'delitos_modalidades', label: 'Delitos y Modalidades' },
  { key: 'dias_semana', label: 'Días de la Semana' },
  { key: 'franja_horaria', label: 'Franja Horaria' },
  { key: 'movilidad', label: 'Movilidad' },
  { key: 'armas', label: 'Armas' },
  { key: 'ambito', label: 'Ámbito' },
  { key: 'jurisdicciones', label: 'Jurisdicciones' },
  { key: 'comparativo', label: 'Comparativo' },
];
