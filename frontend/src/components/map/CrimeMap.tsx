'use client';

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet.markercluster';
import type { PuntoMapa } from '@/lib/types';

// Fix default marker icons in Next.js
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)
  ._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

interface CrimeMapProps {
  puntos: PuntoMapa[];
  center?: [number, number];
  zoom?: number;
}

// Custom crime marker icon
function crimeIcon(delito: string) {
  const isRobo = delito.toLowerCase().includes('robo');
  const isHurto = delito.toLowerCase().includes('hurto');
  const color = isRobo ? '#8B0000' : isHurto ? '#DAA520' : '#1a237e';

  return L.divIcon({
    className: 'crime-marker',
    html: `<div style="
      width: 12px; height: 12px;
      background: ${color};
      border: 2px solid white;
      border-radius: 50%;
      box-shadow: 0 1px 4px rgba(0,0,0,0.4);
    "></div>`,
    iconSize: [12, 12],
    iconAnchor: [6, 6],
    popupAnchor: [0, -8],
  });
}

export default function CrimeMap({
  puntos,
  center = [-26.83, -65.2],
  zoom = 12,
}: CrimeMapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const clusterRef = useRef<any>(null);

  // Initialize map
  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center,
      zoom,
      zoomControl: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Update markers when puntos change
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    // Remove existing cluster
    if (clusterRef.current) {
      map.removeLayer(clusterRef.current);
    }

    // Create new cluster group
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const cluster = (L as any).markerClusterGroup({
      chunkedLoading: true,
      maxClusterRadius: 50,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      disableClusteringAtZoom: 17,
      iconCreateFunction: (c: { getChildCount(): number }) => {
        const count = c.getChildCount();
        let size = 'small';
        let radius = 30;
        if (count > 100) {
          size = 'large';
          radius = 50;
        } else if (count > 30) {
          size = 'medium';
          radius = 40;
        }
        return L.divIcon({
          html: `<div class="cluster-icon cluster-${size}">${count}</div>`,
          className: 'custom-cluster',
          iconSize: L.point(radius, radius),
        });
      },
    });

    // Add markers
    const markers = puntos
      .filter(p => p.latitud && p.longitud)
      .map(p => {
        const marker = L.marker([p.latitud, p.longitud], {
          icon: crimeIcon(p.delito ?? ''),
        });

        marker.bindPopup(
          `<div style="font-size:12px; min-width:180px;">
            <strong style="color:#1a237e;">${p.delito ?? 'Sin tipo'}</strong><br/>
            <span style="color:#666;">📅 ${p.fecha ?? '—'}</span><br/>
            <span style="color:#666;">🕐 ${p.hora ?? '—'}</span><br/>
            <span style="color:#666;">📍 ${p.direccion ?? '—'}</span><br/>
            <span style="color:#888; font-size:10px;">🏢 ${p.jurisdiccion ?? '—'}</span>
          </div>`,
          { closeButton: true }
        );

        return marker;
      });

    cluster.addLayers(markers);
    map.addLayer(cluster);
    clusterRef.current = cluster;

    // Fit bounds if there are points
    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds(), { padding: [50, 50] });
    }
  }, [puntos]);

  return (
    <>
      <style jsx global>{`
        .custom-cluster {
          background: transparent !important;
          border: none !important;
        }
        .cluster-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          color: white;
          font-weight: 700;
          font-size: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        .cluster-small {
          background: rgba(26, 35, 126, 0.8);
          width: 30px;
          height: 30px;
        }
        .cluster-medium {
          background: rgba(218, 165, 32, 0.85);
          width: 40px;
          height: 40px;
          font-size: 13px;
        }
        .cluster-large {
          background: rgba(139, 0, 0, 0.85);
          width: 50px;
          height: 50px;
          font-size: 14px;
        }
      `}</style>
      <div ref={mapContainerRef} className="w-full h-full min-h-[500px]" />
    </>
  );
}
