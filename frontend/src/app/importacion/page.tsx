'use client';

import { useEffect, useState, useCallback } from 'react';
import {
  fetchEstadoImportacion,
  importarTodo,
  importarRegional,
  limpiarDatos,
  fetchRegionales,
} from '@/lib/api';
import type { EstadoImportacion, RegionalInfo } from '@/lib/types';
import StatCard from '@/components/ui/StatCard';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import {
  DatabaseBackup,
  Play,
  Trash2,
  CheckCircle2,
  XCircle,
  Clock,
  HardDrive,
  AlertTriangle,
} from 'lucide-react';

export default function ImportacionPage() {
  const [estado, setEstado] = useState<EstadoImportacion | null>(null);
  const [regionales, setRegionales] = useState<RegionalInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [importing, setImporting] = useState(false);
  const [importingRegional, setImportingRegional] = useState<string | null>(
    null
  );
  const [log, setLog] = useState<string[]>([]);

  const refresh = useCallback(async () => {
    try {
      const [est, regs] = await Promise.all([
        fetchEstadoImportacion(),
        fetchRegionales(),
      ]);
      setEstado(est);
      setRegionales(regs);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const addLog = (msg: string) =>
    setLog(prev => [
      ...prev,
      `[${new Date().toLocaleTimeString('es-AR')}] ${msg}`,
    ]);

  const handleImportAll = async () => {
    if (
      !confirm(
        '¿Importar TODOS los shapefiles? Esto puede tardar varios minutos.'
      )
    )
      return;
    setImporting(true);
    addLog('Iniciando importación completa...');
    try {
      const res = await importarTodo();
      addLog(`✅ Importación completa: ${res.mensaje ?? JSON.stringify(res)}`);
      await refresh();
    } catch (e: unknown) {
      addLog(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setImporting(false);
    }
  };

  const handleImportRegional = async (regional: string) => {
    setImportingRegional(regional);
    addLog(`Importando regional: ${regional}...`);
    try {
      const res = await importarRegional(regional);
      addLog(`✅ ${regional}: ${res.mensaje ?? JSON.stringify(res)}`);
      await refresh();
    } catch (e: unknown) {
      addLog(
        `❌ Error ${regional}: ${e instanceof Error ? e.message : String(e)}`
      );
    } finally {
      setImportingRegional(null);
    }
  };

  const handleClean = async () => {
    if (
      !confirm(
        '¿Eliminar TODOS los datos importados? Esta acción no se puede deshacer.'
      )
    )
      return;
    addLog('Limpiando datos...');
    try {
      const res = await limpiarDatos();
      addLog(`🗑️ ${res.mensaje ?? 'Datos eliminados'}`);
      await refresh();
    } catch (e: unknown) {
      addLog(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    }
  };

  if (loading) return <LoadingSpinner fullPage text="Cargando estado..." />;

  return (
    <div className="space-y-6">
      {/* Status Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          title="Total Registros"
          value={estado?.total_registros ?? 0}
          icon={<HardDrive className="w-6 h-6" />}
          color="blue"
        />
        <StatCard
          title="Importaciones"
          value={estado?.importaciones?.length ?? 0}
          icon={<DatabaseBackup className="w-6 h-6" />}
          color="green"
        />
        <StatCard
          title="Última Actualización"
          value={
            estado?.importaciones?.[0]?.fecha_importacion
              ? new Date(
                  estado.importaciones[0].fecha_importacion
                ).toLocaleDateString('es-AR')
              : '—'
          }
          icon={<Clock className="w-6 h-6" />}
          color="gold"
        />
      </div>

      {/* Actions */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
          <DatabaseBackup className="w-5 h-5 text-policia-azul" />
          Importación de Datos
        </h3>

        <div className="flex flex-wrap gap-3 mb-6">
          <button
            onClick={handleImportAll}
            disabled={importing}
            className="flex items-center gap-2 px-5 py-2.5 bg-policia-azul text-white font-medium rounded-lg hover:bg-policia-azul/90 transition-colors disabled:opacity-50"
          >
            {importing ? (
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Play className="w-4 h-4" />
            )}
            Importar Todo
          </button>

          <button
            onClick={handleClean}
            disabled={importing}
            className="flex items-center gap-2 px-5 py-2.5 bg-policia-rojo text-white font-medium rounded-lg hover:bg-policia-rojo/90 transition-colors disabled:opacity-50"
          >
            <Trash2 className="w-4 h-4" />
            Limpiar Datos
          </button>
        </div>

        {/* Regional Buttons */}
        <h4 className="text-sm font-semibold text-gray-600 mb-3">
          Importar por Regional
        </h4>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
          {regionales.map(r => (
            <button
              key={r.codigo}
              onClick={() => handleImportRegional(r.codigo)}
              disabled={importing || importingRegional !== null}
              className={`flex items-center justify-center gap-1.5 px-3 py-2 text-sm font-medium rounded-lg border transition-colors ${
                importingRegional === r.codigo
                  ? 'bg-policia-azul text-white border-policia-azul'
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'
              } disabled:opacity-50`}
            >
              {importingRegional === r.codigo ? (
                <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : null}
              {r.nombre}
            </button>
          ))}
        </div>
      </div>

      {/* Import History */}
      {estado?.importaciones && estado.importaciones.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">
            Historial de Importaciones
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 text-gray-600">
                  <th className="px-4 py-2 text-left">Comisaría</th>
                  <th className="px-4 py-2 text-left">Archivo</th>
                  <th className="px-4 py-2 text-right">Registros</th>
                  <th className="px-4 py-2 text-left">Estado</th>
                  <th className="px-4 py-2 text-left">Fecha</th>
                </tr>
              </thead>
              <tbody>
                {estado.importaciones.map((imp, i) => (
                  <tr
                    key={i}
                    className="border-b border-gray-100 hover:bg-gray-50"
                  >
                    <td className="px-4 py-2 font-medium">{imp.comisaria}</td>
                    <td className="px-4 py-2 text-gray-500 text-xs truncate max-w-[200px]">
                      {imp.archivo_origen}
                    </td>
                    <td className="px-4 py-2 text-right">
                      {imp.registros_importados?.toLocaleString('es-AR')}
                    </td>
                    <td className="px-4 py-2">
                      {imp.estado === 'completado' ? (
                        <span className="flex items-center gap-1 text-green-600">
                          <CheckCircle2 className="w-4 h-4" /> OK
                        </span>
                      ) : imp.estado === 'error' ? (
                        <span className="flex items-center gap-1 text-red-600">
                          <XCircle className="w-4 h-4" /> Error
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-yellow-600">
                          <AlertTriangle className="w-4 h-4" /> {imp.estado}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2 text-gray-500 text-xs">
                      {imp.fecha_importacion
                        ? new Date(imp.fecha_importacion).toLocaleString(
                            'es-AR'
                          )
                        : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Console Log */}
      {log.length > 0 && (
        <div className="bg-gray-900 rounded-xl p-4 text-xs font-mono text-green-400 max-h-60 overflow-y-auto">
          {log.map((l, i) => (
            <div key={i}>{l}</div>
          ))}
        </div>
      )}
    </div>
  );
}
