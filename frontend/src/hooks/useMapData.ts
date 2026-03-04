'use client';

import { useState, useCallback } from 'react';
import { fetchPuntosMapa } from '@/lib/api';
import type { PuntoMapa } from '@/lib/types';

export function useMapData() {
  const [puntos, setPuntos] = useState<PuntoMapa[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(
    async (filtros: {
      comisaria?: string;
      fecha_desde?: string;
      fecha_hasta?: string;
      delito?: string;
    }) => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetchPuntosMapa(filtros);
        setPuntos(res.puntos);
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
        setPuntos([]);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { puntos, loading, error, fetch };
}
