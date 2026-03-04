'use client';

import dynamic from 'next/dynamic';
import { useState, useCallback } from 'react';
import FilterPanel, { type FiltrosState } from '@/components/FilterPanel';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { fetchPuntosMapa } from '@/lib/api';
import type { PuntoMapa } from '@/lib/types';

const CrimeMap = dynamic(() => import('@/components/map/CrimeMap'), {
  ssr: false,
  loading: () => <LoadingSpinner text="Cargando mapa..." />,
});

export default function MapaPage() {
  const [filtros, setFiltros] = useState<FiltrosState>({
    comisaria: '',
    regional: '',
    fecha_desde: '',
    fecha_hasta: '',
    delito: '',
  });
  const [puntos, setPuntos] = useState<PuntoMapa[]>([]);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const loadPoints = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchPuntosMapa({
        comisaria: filtros.comisaria || undefined,
        fecha_desde: filtros.fecha_desde || undefined,
        fecha_hasta: filtros.fecha_hasta || undefined,
        delito: filtros.delito || undefined,
      });
      setPuntos(data.puntos);
      setLoaded(true);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, [filtros]);

  return (
    <div className="space-y-4 h-full flex flex-col">
      <FilterPanel
        filtros={filtros}
        onChange={setFiltros}
        onApply={loadPoints}
        loading={loading}
      />

      {loaded && (
        <div className="text-sm text-gray-500">
          {puntos.length.toLocaleString('es-AR')} puntos cargados
        </div>
      )}

      <div className="flex-1 min-h-[500px] rounded-xl overflow-hidden shadow-sm border border-gray-200">
        <CrimeMap puntos={puntos} />
      </div>
    </div>
  );
}
