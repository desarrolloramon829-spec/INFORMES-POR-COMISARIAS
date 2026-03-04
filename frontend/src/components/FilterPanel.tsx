'use client';

import { useEffect, useState, useCallback } from 'react';
import {
  fetchRegionales,
  fetchComisarias,
  fetchDelitos,
  fetchRangoFechas,
} from '@/lib/api';
import type { RegionalInfo, ComisariaInfo } from '@/lib/types';
import { Filter, RotateCcw } from 'lucide-react';

export interface FiltrosState {
  comisaria: string;
  regional: string;
  fecha_desde: string;
  fecha_hasta: string;
  delito: string;
}

interface FilterPanelProps {
  filtros: FiltrosState;
  onChange: (filtros: FiltrosState) => void;
  onApply: () => void;
  loading?: boolean;
  showDelito?: boolean;
}

const INITIAL_FILTROS: FiltrosState = {
  comisaria: '',
  regional: '',
  fecha_desde: '',
  fecha_hasta: '',
  delito: '',
};

export default function FilterPanel({
  filtros,
  onChange,
  onApply,
  loading = false,
  showDelito = true,
}: FilterPanelProps) {
  const [regionales, setRegionales] = useState<RegionalInfo[]>([]);
  const [comisarias, setComisarias] = useState<ComisariaInfo[]>([]);
  const [delitos, setDelitos] = useState<string[]>([]);

  // Load initial data
  useEffect(() => {
    fetchRegionales().then(setRegionales).catch(console.error);
    fetchDelitos().then(setDelitos).catch(console.error);
    fetchRangoFechas()
      .then(r => {
        if (!filtros.fecha_desde && !filtros.fecha_hasta) {
          onChange({
            ...filtros,
            fecha_desde: r.fecha_desde ?? '',
            fecha_hasta: r.fecha_hasta ?? '',
          });
        }
      })
      .catch(console.error);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load comisarías when regional changes
  useEffect(() => {
    if (filtros.regional) {
      fetchComisarias(filtros.regional)
        .then(setComisarias)
        .catch(console.error);
    } else {
      setComisarias([]);
    }
  }, [filtros.regional]);

  const set = useCallback(
    (key: keyof FiltrosState, value: string) => {
      const next = { ...filtros, [key]: value };
      if (key === 'regional') {
        next.comisaria = '';
      }
      onChange(next);
    },
    [filtros, onChange]
  );

  const reset = () => onChange({ ...INITIAL_FILTROS });

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <div className="flex items-center gap-2 mb-4">
        <Filter className="w-4 h-4 text-policia-azul" />
        <h3 className="text-sm font-semibold text-gray-700">Filtros</h3>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {/* Regional */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Regional
          </label>
          <select
            value={filtros.regional}
            onChange={e => set('regional', e.target.value)}
            className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-policia-azul/30 focus:border-policia-azul"
          >
            <option value="">Todas</option>
            {regionales.map(r => (
              <option key={r.codigo} value={r.codigo}>
                {r.nombre}
              </option>
            ))}
          </select>
        </div>

        {/* Comisaría */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Comisaría
          </label>
          <select
            value={filtros.comisaria}
            onChange={e => set('comisaria', e.target.value)}
            className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-policia-azul/30 focus:border-policia-azul"
            disabled={!filtros.regional}
          >
            <option value="">Todas</option>
            {comisarias.map(c => (
              <option key={c.codigo} value={c.codigo}>
                {c.nombre}
              </option>
            ))}
          </select>
        </div>

        {/* Fecha Desde */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Desde
          </label>
          <input
            type="date"
            value={filtros.fecha_desde}
            onChange={e => set('fecha_desde', e.target.value)}
            className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-policia-azul/30 focus:border-policia-azul"
          />
        </div>

        {/* Fecha Hasta */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Hasta
          </label>
          <input
            type="date"
            value={filtros.fecha_hasta}
            onChange={e => set('fecha_hasta', e.target.value)}
            className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-policia-azul/30 focus:border-policia-azul"
          />
        </div>

        {/* Delito */}
        {showDelito && (
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">
              Delito
            </label>
            <select
              value={filtros.delito}
              onChange={e => set('delito', e.target.value)}
              className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-policia-azul/30 focus:border-policia-azul"
            >
              <option value="">Todos</option>
              {delitos.map(d => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2 mt-4">
        <button
          onClick={onApply}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-policia-azul text-white text-sm font-medium rounded-lg hover:bg-policia-azul/90 transition-colors disabled:opacity-50"
        >
          {loading ? (
            <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Filter className="w-4 h-4" />
          )}
          Aplicar
        </button>
        <button
          onClick={reset}
          className="flex items-center gap-2 px-4 py-2 text-gray-500 text-sm font-medium rounded-lg hover:bg-gray-100 transition-colors"
        >
          <RotateCcw className="w-4 h-4" />
          Limpiar
        </button>
      </div>
    </div>
  );
}
