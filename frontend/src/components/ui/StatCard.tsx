import { ReactNode } from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: ReactNode;
  trend?: { value: number; label: string };
  color?: 'blue' | 'red' | 'gold' | 'green' | 'purple';
}

const colorMap = {
  blue: 'bg-blue-50 text-policia-azul border-blue-200',
  red: 'bg-red-50 text-policia-rojo border-red-200',
  gold: 'bg-yellow-50 text-yellow-700 border-yellow-200',
  green: 'bg-green-50 text-green-700 border-green-200',
  purple: 'bg-purple-50 text-purple-700 border-purple-200',
};

const iconBg = {
  blue: 'bg-policia-azul/10 text-policia-azul',
  red: 'bg-policia-rojo/10 text-policia-rojo',
  gold: 'bg-yellow-100 text-yellow-700',
  green: 'bg-green-100 text-green-700',
  purple: 'bg-purple-100 text-purple-700',
};

export default function StatCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  color = 'blue',
}: StatCardProps) {
  return (
    <div
      className={`rounded-xl border p-5 ${colorMap[color]} transition-shadow hover:shadow-md`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium opacity-70 uppercase tracking-wider">
            {title}
          </p>
          <p className="text-3xl font-bold mt-1">
            {typeof value === 'number' ? value.toLocaleString('es-AR') : value}
          </p>
          {subtitle && <p className="text-xs mt-1 opacity-60">{subtitle}</p>}
          {trend && (
            <p
              className={`text-xs mt-2 font-medium ${
                trend.value >= 0 ? 'text-red-600' : 'text-green-600'
              }`}
            >
              {trend.value >= 0 ? '▲' : '▼'} {Math.abs(trend.value).toFixed(1)}%{' '}
              {trend.label}
            </p>
          )}
        </div>
        {icon && (
          <div className={`p-3 rounded-xl ${iconBg[color]}`}>{icon}</div>
        )}
      </div>
    </div>
  );
}
