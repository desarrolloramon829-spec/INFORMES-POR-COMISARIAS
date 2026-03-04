import * as XLSX from 'xlsx';
import type { FilaInforme } from '@/lib/types';

export function exportToExcel(data: FilaInforme[], titulo: string) {
  const rows = data.map(d => ({
    Categoría: d.categoria ?? '',
    Cantidad: Number(d.cantidad ?? 0),
    Porcentaje: `${Number(d.porcentaje ?? 0).toFixed(1)}%`,
    ...(d.subcategoria ? { Subcategoría: d.subcategoria } : {}),
  }));

  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(rows);

  // Auto-width columns
  const colWidths = Object.keys(rows[0] ?? {}).map(key => ({
    wch:
      Math.max(
        key.length,
        ...rows.map(
          r => String((r as Record<string, unknown>)[key] ?? '').length
        )
      ) + 2,
  }));
  ws['!cols'] = colWidths;

  XLSX.utils.book_append_sheet(wb, ws, 'Informe');

  const filename = `${titulo.replace(/[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑ\s]/g, '').trim()}_${new Date().toISOString().slice(0, 10)}.xlsx`;
  XLSX.writeFile(wb, filename);
}
