import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import type { FilaInforme } from '@/lib/types';

export function exportToPdf(
  data: FilaInforme[],
  titulo: string,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  _columns?: any[]
) {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

  // Header
  doc.setFillColor(26, 35, 126); // policia-azul
  doc.rect(0, 0, 210, 35, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('POLICÍA DE TUCUMÁN', 105, 14, { align: 'center' });

  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.text('Sección Análisis Delictual', 105, 21, { align: 'center' });

  doc.setFontSize(10);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(218, 165, 32); // dorado
  doc.text(titulo.toUpperCase(), 105, 30, { align: 'center' });

  // Date
  doc.setTextColor(100, 100, 100);
  doc.setFontSize(8);
  doc.setFont('helvetica', 'normal');
  doc.text(
    `Generado: ${new Date().toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })}`,
    195,
    42,
    { align: 'right' }
  );

  // Table
  const head = [['Categoría', 'Cantidad', '%']];
  const body = data.map(d => [
    String(d.categoria ?? ''),
    Number(d.cantidad ?? 0).toLocaleString('es-AR'),
    `${Number(d.porcentaje ?? 0).toFixed(1)}%`,
  ]);

  // Total row
  const totalQty = data.reduce((s, d) => s + Number(d.cantidad ?? 0), 0);
  body.push(['TOTAL', totalQty.toLocaleString('es-AR'), '100.0%']);

  autoTable(doc, {
    startY: 46,
    head,
    body,
    headStyles: {
      fillColor: [26, 35, 126],
      textColor: [255, 255, 255],
      fontSize: 9,
      fontStyle: 'bold',
    },
    bodyStyles: {
      fontSize: 8,
      textColor: [50, 50, 50],
    },
    alternateRowStyles: {
      fillColor: [245, 245, 255],
    },
    footStyles: {
      fillColor: [26, 35, 126],
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      fontSize: 9,
    },
    didParseCell: data => {
      // Bold the last row (TOTAL)
      if (data.row.index === body.length - 1) {
        data.cell.styles.fillColor = [240, 240, 240];
        data.cell.styles.fontStyle = 'bold';
        data.cell.styles.textColor = [26, 35, 126];
      }
    },
    margin: { left: 15, right: 15 },
    styles: {
      cellPadding: 3,
      lineColor: [200, 200, 200],
      lineWidth: 0.1,
    },
  });

  // Footer
  const pageCount = doc.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(7);
    doc.setTextColor(150, 150, 150);
    doc.text(
      `Página ${i} de ${pageCount} — Sistema de Informes Delictuales — Policía de Tucumán`,
      105,
      290,
      { align: 'center' }
    );
  }

  const filename = `${titulo.replace(/[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑ\s]/g, '').trim()}_${new Date().toISOString().slice(0, 10)}.pdf`;
  doc.save(filename);
}
