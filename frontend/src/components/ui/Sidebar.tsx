'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  FileBarChart2,
  Map,
  DatabaseBackup,
  Shield,
} from 'lucide-react';

const NAV_ITEMS = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/informes', label: 'Informes', icon: FileBarChart2 },
  { href: '/mapa', label: 'Mapa Delictual', icon: Map },
  { href: '/importacion', label: 'Importación', icon: DatabaseBackup },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-policia-azul text-white flex flex-col print:hidden">
      {/* Logo / Branding */}
      <div className="flex flex-col items-center gap-2 px-4 py-6 border-b border-white/10">
        <Shield className="w-12 h-12 text-policia-dorado" />
        <div className="text-center">
          <p className="text-sm font-bold leading-tight">POLICÍA DE TUCUMÁN</p>
          <p className="text-[10px] text-policia-dorado mt-1 uppercase tracking-wider">
            Sección Análisis Delictual
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4">
        <ul className="space-y-1 px-3">
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
            const isActive =
              href === '/' ? pathname === '/' : pathname.startsWith(href);
            return (
              <li key={href}>
                <Link
                  href={href}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-white/15 text-policia-dorado'
                      : 'text-white/70 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-white/10">
        <p className="text-[10px] text-white/40 text-center">
          v1.0.0 — Sistema de Informes
        </p>
      </div>
    </aside>
  );
}
