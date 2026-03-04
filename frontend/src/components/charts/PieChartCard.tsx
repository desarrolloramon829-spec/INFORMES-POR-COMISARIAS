'use client';

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import type { FilaInforme } from '@/lib/types';

interface PieChartCardProps {
  data: FilaInforme[];
  title: string;
  dataKey?: string;
  categoryKey?: string;
  maxSlices?: number;
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
  '#be185d',
  '#65a30d',
];

export default function PieChartCard({
  data,
  title,
  dataKey = 'cantidad',
  categoryKey = 'categoria',
  maxSlices = 10,
}: PieChartCardProps) {
  const sorted = [...data].sort(
    (a, b) => Number(b[dataKey] ?? 0) - Number(a[dataKey] ?? 0)
  );

  const top = sorted.slice(0, maxSlices);
  const rest = sorted.slice(maxSlices);
  const restTotal = rest.reduce(
    (s, r) => s + Number(r[dataKey] ?? 0),
    0
  );

  const chartData = top.map((d) => ({
    name: String(d[categoryKey] ?? ''),
    value: Number(d[dataKey] ?? 0),
  }));

  if (restTotal > 0) {
    chartData.push({ name: 'Otros', value: restTotal });
  }

  const total = chartData.reduce((s, d) => s + d.value, 0);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <h4 className="text-sm font-semibold text-gray-700 mb-3">{title}</h4>
      <ResponsiveContainer width="100%" height={320}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            outerRadius={110}
            innerRadius={50}
            dataKey="value"
            nameKey="name"
            paddingAngle={2}
            label={({ name, value }) =>
              `${name}: ${((value / total) * 100).toFixed(1)}%`
            }
            labelLine={true}
            fontSize={10}
          >
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(v: number) => [
              `${v} (${((v / total) * 100).toFixed(1)}%)`,
              'Cantidad',
            ]}
          />
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: 11 }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
