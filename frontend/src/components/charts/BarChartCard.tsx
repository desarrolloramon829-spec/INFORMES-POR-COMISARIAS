'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import type { FilaInforme } from '@/lib/types';

interface BarChartCardProps {
  data: FilaInforme[];
  title: string;
  dataKey?: string;
  categoryKey?: string;
  color?: string;
  horizontal?: boolean;
  maxBars?: number;
}

const COLORS = [
  '#1a237e',
  '#8B0000',
  '#DAA520',
  '#2563eb',
  '#dc2626',
  '#059669',
  '#7c3aed',
  '#ea580c',
  '#0891b2',
  '#4f46e5',
];

export default function BarChartCard({
  data,
  title,
  dataKey = 'cantidad',
  categoryKey = 'categoria',
  color,
  horizontal = false,
  maxBars = 15,
}: BarChartCardProps) {
  const chartData = data.slice(0, maxBars).map((d) => ({
    name: String(d[categoryKey] ?? ''),
    value: Number(d[dataKey] ?? 0),
    pct: d.porcentaje ?? 0,
  }));

  if (horizontal) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <h4 className="text-sm font-semibold text-gray-700 mb-3">{title}</h4>
        <ResponsiveContainer
          width="100%"
          height={Math.max(300, chartData.length * 32)}
        >
          <BarChart data={chartData} layout="vertical" margin={{ left: 120 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" fontSize={11} />
            <YAxis
              type="category"
              dataKey="name"
              width={110}
              fontSize={11}
              tick={{ fill: '#374151' }}
            />
            <Tooltip
              formatter={(v: number) => [v, 'Cantidad']}
              labelStyle={{ fontWeight: 600 }}
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {chartData.map((_, i) => (
                <Cell key={i} fill={color ?? COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <h4 className="text-sm font-semibold text-gray-700 mb-3">{title}</h4>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis
            dataKey="name"
            fontSize={11}
            angle={-35}
            textAnchor="end"
            height={80}
            tick={{ fill: '#374151' }}
          />
          <YAxis fontSize={11} />
          <Tooltip
            formatter={(v: number) => [v, 'Cantidad']}
            labelStyle={{ fontWeight: 600 }}
          />
          <Bar dataKey="value" radius={[4, 4, 0, 0]}>
            {chartData.map((_, i) => (
              <Cell key={i} fill={color ?? COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
