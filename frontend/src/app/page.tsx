'use client';

import { useEffect, useState } from 'react';
import { fetchDashboard } from '@/lib/api';
import type { DashboardResponse } from '@/lib/types';
import StatCard from '@/components/ui/StatCard';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import BarChartCard from '@/components/charts/BarChartCard';
import PieChartCard from '@/components/charts/PieChartCard';
import { AlertTriangle, TrendingUp, MapPin, Calendar } from 'lucide-react';

export default function DashboardPage() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner fullPage text="Cargando dashboard..." />;

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <AlertTriangle className="w-12 h-12 text-yellow-500" />
        <p className="text-gray-500">
          No se pudo cargar el dashboard. Verifique que el servidor esté activo.
        </p>
        <p className="text-xs text-gray-400">{error}</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Hechos"
          value={data.total_hechos}
          icon={<AlertTriangle className="w-6 h-6" />}
          color="blue"
        />
        <StatCard
          title="Hechos del Mes"
          value={data.hechos_mes_actual}
          icon={<Calendar className="w-6 h-6" />}
          color="gold"
        />
        <StatCard
          title="Delito Más Frecuente"
          value={data.top_delito ?? '—'}
          subtitle={`${data.top_delito_cantidad?.toLocaleString('es-AR') ?? 0} casos`}
          icon={<TrendingUp className="w-6 h-6" />}
          color="red"
        />
        <StatCard
          title="Jurisdicciones Activas"
          value={data.jurisdicciones_activas}
          icon={<MapPin className="w-6 h-6" />}
          color="green"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {data.delitos_top && data.delitos_top.length > 0 && (
          <BarChartCard
            data={data.delitos_top}
            title="Top 10 Delitos"
            horizontal
          />
        )}
        {data.delitos_top && data.delitos_top.length > 0 && (
          <PieChartCard
            data={data.delitos_top}
            title="Distribución de Delitos"
          />
        )}
      </div>

      {data.por_dia && data.por_dia.length > 0 && (
        <BarChartCard
          data={data.por_dia}
          title="Hechos por Día de la Semana"
          color="#1a237e"
        />
      )}

      {data.por_franja && data.por_franja.length > 0 && (
        <BarChartCard
          data={data.por_franja}
          title="Hechos por Franja Horaria"
          color="#8B0000"
        />
      )}
    </div>
  );
}
