'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

interface LineChartCardProps {
  data: Record<string, unknown>[];
  title: string;
  xKey: string;
  lines: { key: string; color: string; name: string }[];
}

export default function LineChartCard({
  data,
  title,
  xKey,
  lines,
}: LineChartCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <h4 className="text-sm font-semibold text-gray-700 mb-3">{title}</h4>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey={xKey} fontSize={11} tick={{ fill: '#374151' }} />
          <YAxis fontSize={11} />
          <Tooltip labelStyle={{ fontWeight: 600 }} />
          <Legend
            iconType="line"
            iconSize={12}
            wrapperStyle={{ fontSize: 12 }}
          />
          {lines.map(l => (
            <Line
              key={l.key}
              type="monotone"
              dataKey={l.key}
              stroke={l.color}
              name={l.name}
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
