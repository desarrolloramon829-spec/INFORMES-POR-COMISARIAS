/**
 * Cliente API tipado para el backend FastAPI.
 */
import type {
  FiltrosInforme,
  FiltrosComparativo,
  InformeResponse,
  InformeCompleto,
  ComparativoResponse,
  PuntosMapaResponse,
  JurisdiccionesGeoJSON,
  FiltrosDisponibles,
  RegionalInfo,
  ComisariaInfo,
  EstadoImportacion,
  DashboardResponse,
  TipoInforme,
} from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API Error ${res.status}: ${error}`);
  }
  return res.json();
}

function postJSON<T>(url: string, body: unknown): Promise<T> {
  return fetchJSON<T>(url, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/* ---- Dashboard ---- */
export const api = {
  dashboard: () => fetchJSON<DashboardResponse>('/dashboard'),

  /* ---- Informes ---- */
  informeDelitosModalidades: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/delitos-modalidades', f),

  informeDiasSemana: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/dias-semana', f),

  informeFranjaHoraria: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/franja-horaria', f),

  informeMovilidad: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/movilidad', f),

  informeArmas: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/armas', f),

  informeAmbito: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/ambito', f),

  informeJurisdicciones: (f: FiltrosInforme) =>
    postJSON<InformeResponse>('/informes/jurisdicciones', f),

  informeComparativo: (f: FiltrosComparativo) =>
    postJSON<ComparativoResponse>('/informes/comparativo', f),

  informeCompleto: (f: FiltrosInforme) =>
    postJSON<InformeCompleto>('/informes/completo', f),

  /* ---- Mapa ---- */
  puntosMapa: (f: FiltrosInforme, limite = 5000) =>
    postJSON<PuntosMapaResponse>(`/mapa/puntos?limite=${limite}`, f),

  jurisdicciones: () =>
    fetchJSON<JurisdiccionesGeoJSON>('/mapa/jurisdicciones'),

  /* ---- Filtros ---- */
  filtrosDisponibles: () =>
    fetchJSON<FiltrosDisponibles>('/filtros/disponibles'),

  regionales: () => fetchJSON<RegionalInfo[]>('/filtros/regionales'),

  comisarias: (regional?: string) =>
    fetchJSON<ComisariaInfo[]>(
      `/filtros/comisarias${regional ? `?regional=${regional}` : ''}`
    ),

  delitos: () => fetchJSON<string[]>('/filtros/delitos'),

  rangoFechas: () =>
    fetchJSON<{ fecha_min: string | null; fecha_max: string | null }>(
      '/filtros/rango-fechas'
    ),

  /* ---- Datos / Importación ---- */
  estadoImportacion: () => fetchJSON<EstadoImportacion>('/datos/estado'),

  importarDatos: (regional?: string) =>
    postJSON<{
      mensaje: string;
      total_registros_importados: number;
      detalle: unknown[];
    }>('/datos/importar', { regional: regional || null }),

  importarRegional: (regionalKey: string) =>
    postJSON<{ mensaje: string; exitosos: number; total_registros: number }>(
      `/datos/importar/${regionalKey}`,
      {}
    ),

  limpiarDatos: (regional?: string) =>
    fetchJSON<{ mensaje: string }>(
      `/datos/limpiar${regional ? `?regional=${regional}` : ''}`,
      { method: 'DELETE' }
    ),
};

/* -------------------------------------------------------------------
 * Named exports — usados directamente por los componentes
 * ------------------------------------------------------------------ */

export const fetchDashboard = (): Promise<DashboardResponse> => api.dashboard();

export const fetchRegionales = (): Promise<RegionalInfo[]> => api.regionales();

export const fetchComisarias = (regional?: string): Promise<ComisariaInfo[]> =>
  api.comisarias(regional);

export const fetchDelitos = (): Promise<string[]> => api.delitos();

export const fetchRangoFechas = async (): Promise<{
  fecha_desde: string;
  fecha_hasta: string;
}> => {
  const r = await api.rangoFechas();
  return {
    fecha_desde: r.fecha_min ?? '',
    fecha_hasta: r.fecha_max ?? '',
  };
};

export const fetchPuntosMapa = (
  filtros: Partial<FiltrosInforme>,
  limite = 5000
): Promise<PuntosMapaResponse> => api.puntosMapa(filtros as FiltrosInforme, limite);

export const fetchEstadoImportacion = (): Promise<EstadoImportacion> =>
  api.estadoImportacion();

export const importarTodo = (): Promise<{
  mensaje: string;
  total_registros_importados: number;
  detalle: unknown[];
}> => api.importarDatos();

export const importarRegional = (
  regional: string
): Promise<{ mensaje: string; exitosos: number; total_registros: number }> =>
  api.importarRegional(regional);

export const limpiarDatos = (): Promise<{ mensaje: string }> =>
  api.limpiarDatos();

export const fetchInformeComparativo = (
  f: FiltrosComparativo
): Promise<ComparativoResponse> => api.informeComparativo(f);

export async function fetchInforme(
  tipo: TipoInforme,
  filtros: Partial<FiltrosInforme>
): Promise<InformeResponse> {
  const f = filtros as FiltrosInforme;
  switch (tipo) {
    case 'delitos_modalidades':
      return api.informeDelitosModalidades(f);
    case 'dias_semana':
      return api.informeDiasSemana(f);
    case 'franja_horaria':
      return api.informeFranjaHoraria(f);
    case 'movilidad':
      return api.informeMovilidad(f);
    case 'armas':
      return api.informeArmas(f);
    case 'ambito':
      return api.informeAmbito(f);
    case 'jurisdicciones':
      return api.informeJurisdicciones(f);
    default:
      return api.informeDelitosModalidades(f);
  }
}
