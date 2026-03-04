'use client';

import { usePathname } from 'next/navigation';
import { Bell } from 'lucide-react';

const PAGE_TITLES: Record<string, string> = {
  '/': 'Dashboard',
  '/informes': 'Informes Delictuales',
  '/mapa': 'Mapa Delictual',
  '/importacion': 'Importación de Datos',
};

export default function Header() {
  const pathname = usePathname();
  const title =
    PAGE_TITLES[pathname] ??
    Object.entries(PAGE_TITLES).find(([k]) => pathname.startsWith(k))?.[1] ??
    'Sistema de Informes';

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 print:hidden">
      <h1 className="text-xl font-bold text-policia-azul">{title}</h1>
      <div className="flex items-center gap-4">
        <span className="text-xs text-gray-400">
          {new Date().toLocaleDateString('es-AR', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          })}
        </span>
        <button
          className="relative p-2 rounded-full hover:bg-gray-100 transition-colors"
          title="Notificaciones"
        >
          <Bell className="w-5 h-5 text-gray-500" />
        </button>
      </div>
    </header>
  );
}
