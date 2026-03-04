'use client';

import { useState, useCallback } from 'react';
import { fetchInforme, fetchInformeComparativo } from '@/lib/api';
import type { FilaInforme, InformeResponse, TipoInforme } from '@/lib/types';
import type { FiltrosState } from '@/components/FilterPanel';

export function useInforme() {
  const [data, setData] = useState<FilaInforme[]>([]);
  const [titulo, setTitulo] = useState('');
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(
    async (tipo: TipoInforme, filtros: FiltrosState) => {
      setLoading(true);
      setError(null);
      try {
        if (tipo === 'comparativo') {
          const res = await fetchInformeComparativo({
            comisaria: filtros.comisaria || undefined,
            fecha_desde_1: filtros.fecha_desde || undefined,
            fecha_hasta_1: filtros.fecha_hasta || undefined,
          });
          setData(res.filas);
          setTitulo(res.titulo);
          setTotal(res.total_periodo_1 + res.total_periodo_2);
        } else {
          const res = await fetchInforme(tipo, {
            comisaria: filtros.comisaria || undefined,
            fecha_desde: filtros.fecha_desde || undefined,
            fecha_hasta: filtros.fecha_hasta || undefined,
            delito: filtros.delito || undefined,
          });
          setData(res.filas);
          setTitulo(res.titulo);
          setTotal(res.total);
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
        setData([]);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { data, titulo, total, loading, error, fetch };
}
