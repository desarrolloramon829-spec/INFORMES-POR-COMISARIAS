'use client';

import { useState, useCallback } from 'react';
import FilterPanel, { type FiltrosState } from '@/components/FilterPanel';
import ReportTable from '@/components/ReportTable';
import BarChartCard from '@/components/charts/BarChartCard';
import PieChartCard from '@/components/charts/PieChartCard';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { fetchInforme, fetchInformeComparativo } from '@/lib/api';
import type { FilaInforme, TipoInforme } from '@/lib/types';
import { createColumnHelper } from '@tanstack/react-table';
import { Download, Printer, FileSpreadsheet } from 'lucide-react';

const TABS: { tipo: TipoInforme; label: string }[] = [
  { tipo: 'delitos_modalidades', label: 'Delitos y Modalidades' },
  { tipo: 'dias_semana', label: 'Días de la Semana' },
  { tipo: 'franja_horaria', label: 'Franja Horaria' },
  { tipo: 'movilidad', label: 'Movilidad' },
  { tipo: 'armas', label: 'Armas' },
  { tipo: 'ambito', label: 'Ámbito' },
  { tipo: 'jurisdicciones', label: 'Jurisdicciones' },
  { tipo: 'comparativo', label: 'Comparativo' },
];

const columnHelper = createColumnHelper<FilaInforme>();

function buildColumns(tipo: TipoInforme) {
  const base = [
    columnHelper.accessor('categoria', {
      header: () => getCategoryHeader(tipo),
      cell: info => info.getValue() ?? '—',
    }),
    columnHelper.accessor('cantidad', {
      header: 'Cantidad',
      cell: info => Number(info.getValue() ?? 0).toLocaleString('es-AR'),
    }),
    columnHelper.accessor('porcentaje', {
      header: '%',
      cell: info => `${Number(info.getValue() ?? 0).toFixed(1)}%`,
    }),
  ];
  return base;
}

function getCategoryHeader(tipo: TipoInforme): string {
  switch (tipo) {
    case 'delitos_modalidades':
      return 'Delito / Modalidad';
    case 'dias_semana':
      return 'Día';
    case 'franja_horaria':
      return 'Franja';
    case 'movilidad':
      return 'Vehículo';
    case 'armas':
      return 'Arma';
    case 'ambito':
      return 'Lugar';
    case 'jurisdicciones':
      return 'Jurisdicción';
    case 'comparativo':
      return 'Período';
    default:
      return 'Categoría';
  }
}

function getChartTitle(tipo: TipoInforme): string {
  switch (tipo) {
    case 'delitos_modalidades':
      return 'Distribución de Delitos';
    case 'dias_semana':
      return 'Hechos por Día de la Semana';
    case 'franja_horaria':
      return 'Hechos por Franja Horaria';
    case 'movilidad':
      return 'Vehículos Utilizados';
    case 'armas':
      return 'Armas Utilizadas';
    case 'ambito':
      return 'Lugar del Hecho';
    case 'jurisdicciones':
      return 'Hechos por Jurisdicción';
    case 'comparativo':
      return 'Comparación entre Períodos';
    default:
      return 'Gráfico';
  }
}

export default function InformesPage() {
  const [tab, setTab] = useState<TipoInforme>('delitos_modalidades');
  const [filtros, setFiltros] = useState<FiltrosState>({
    comisaria: '',
    regional: '',
    fecha_desde: '',
    fecha_hasta: '',
    delito: '',
  });
  const [data, setData] = useState<FilaInforme[]>([]);
  const [loading, setLoading] = useState(false);
  const [titulo, setTitulo] = useState('');
  const [total, setTotal] = useState(0);
  const [view, setView] = useState<'table' | 'chart' | 'both'>('both');

  const loadReport = useCallback(async () => {
    setLoading(true);
    try {
      if (tab === 'comparativo') {
        const res = await fetchInformeComparativo({
          comisaria: filtros.comisaria || undefined,
          fecha_desde_1: filtros.fecha_desde || undefined,
          fecha_hasta_1: filtros.fecha_hasta || undefined,
        });
        setData(res.filas);
        setTitulo(res.titulo);
        setTotal(res.total_periodo_1 + res.total_periodo_2);
      } else {
        const res = await fetchInforme(tab, {
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
      console.error(e);
      setData([]);
    } finally {
      setLoading(false);
    }
  }, [tab, filtros]);

  const handlePrint = () => window.print();

  const handleExportExcel = async () => {
    const { exportToExcel } = await import('@/lib/exportExcel');
    exportToExcel(data, titulo || 'informe');
  };

  const handleExportPdf = async () => {
    const { exportToPdf } = await import('@/lib/exportPdf');
    exportToPdf(data, titulo || 'informe', buildColumns(tab));
  };

  const columns = buildColumns(tab);

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-1 flex flex-wrap gap-1">
        {TABS.map(({ tipo, label }) => (
          <button
            key={tipo}
            onClick={() => setTab(tipo)}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              tab === tipo
                ? 'bg-policia-azul text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Filters */}
      <FilterPanel
        filtros={filtros}
        onChange={setFiltros}
        onApply={loadReport}
        loading={loading}
        showDelito={tab !== 'delitos_modalidades' && tab !== 'comparativo'}
      />

      {/* Toolbar */}
      {data.length > 0 && (
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">
              {titulo} — {total.toLocaleString('es-AR')} hechos
            </span>
          </div>
          <div className="flex items-center gap-2">
            {/* View Toggle */}
            <div className="flex bg-gray-100 rounded-lg p-0.5">
              {(['table', 'chart', 'both'] as const).map(v => (
                <button
                  key={v}
                  onClick={() => setView(v)}
                  className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                    view === v
                      ? 'bg-white shadow-sm text-policia-azul'
                      : 'text-gray-500'
                  }`}
                >
                  {v === 'table'
                    ? 'Tabla'
                    : v === 'chart'
                      ? 'Gráfico'
                      : 'Ambos'}
                </button>
              ))}
            </div>
            {/* Export */}
            <button
              onClick={handleExportExcel}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-green-700 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
            >
              <FileSpreadsheet className="w-4 h-4" />
              Excel
            </button>
            <button
              onClick={handleExportPdf}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-red-700 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
            >
              <Download className="w-4 h-4" />
              PDF
            </button>
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Printer className="w-4 h-4" />
              Imprimir
            </button>
          </div>
        </div>
      )}

      {/* Content */}
      {loading ? (
        <LoadingSpinner text="Generando informe..." />
      ) : data.length > 0 ? (
        <div
          className={
            view === 'both'
              ? 'grid grid-cols-1 xl:grid-cols-2 gap-6'
              : 'space-y-6'
          }
        >
          {(view === 'table' || view === 'both') && (
            <ReportTable
              data={data}
              columns={columns}
              highlightMax="cantidad"
            />
          )}
          {(view === 'chart' || view === 'both') && (
            <div className="space-y-6">
              <BarChartCard
                data={data}
                title={getChartTitle(tab)}
                horizontal={
                  tab === 'delitos_modalidades' || tab === 'jurisdicciones'
                }
              />
              {tab === 'delitos_modalidades' && (
                <PieChartCard data={data} title="Proporción de Delitos" />
              )}
            </div>
          )}
        </div>
      ) : (
        !loading && (
          <div className="text-center py-20 text-gray-400">
            <p className="text-lg">Seleccione los filtros y presione Aplicar</p>
            <p className="text-sm mt-1">para generar el informe</p>
          </div>
        )
      )}
    </div>
  );
}
