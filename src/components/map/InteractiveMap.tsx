/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import worldData1939 from '@/src/data/geojson/world-1939.json';
import { supabase } from '@/src/lib/supabase';
import { getShiftedGeoJSON, WORLD_COPIES } from './map-utils';
import type { HistoricalEvent } from '@/src/types';

// Mock data untuk informasi negara

/**
 * Komponen peta interaktif Leaflet yang menampilkan batas negara tahun 1939
 * dan peristiwa sejarah berdasarkan tahun yang dipilih.
 */
export default function InteractiveMap({ currentYear }: { currentYear: number }) {
  const [events, setEvents] = useState<HistoricalEvent[]>([]);

  useEffect(() => {
    async function fetchEvents() {
      const { data, error } = await supabase
        .from('historical_events')
        .select('*');

      if (error) {
        console.error('Gagal mengambil data:', error);
      } else if (data) {
        setEvents(data);
      }
    }

    fetchEvents();
  }, []);

  // Filter peristiwa berdasarkan tahun aktif (disiapkan untuk fitur mendatang)
  const _filteredEvents = events.filter(event => event.tahun === currentYear);

  const onEachFeature = (feature: any, layer: any) => {
    const props = feature.properties;
    if (!props || !props.name) return;

    let popupContent = '';
    
    // Semua data kini diambil langsung dari properties GeoJSON!
    if (props.leader || props.ideology || props.alliance) {
      let badgeStyle = "background-color: #f1f5f9; color: #475569;"; // Default abu-abu (Netral)
      const lowerAlliance = (props.alliance || '').toLowerCase();
      if (lowerAlliance.includes('komintern') || lowerAlliance.includes('soviet') || lowerAlliance.includes('komunis')) {
        badgeStyle = "background-color: #fee2e2; color: #991b1b;"; // Merah (Komintern)
      } else if (lowerAlliance.includes('poros') || lowerAlliance.includes('axis')) {
        badgeStyle = "background-color: #1e293b; color: #f8fafc;"; // Hitam/Charcoal (Poros)
      } else if (lowerAlliance.includes('sekutu') || lowerAlliance.includes('allies')) {
        badgeStyle = "background-color: #dbeafe; color: #1e40af;"; // Biru (Sekutu)
      } else if (lowerAlliance.includes('jepang')) {
        badgeStyle = "background-color: #fef08a; color: #854d0e;"; // Kuning Emas (Faksi Jepang)
      } else if (lowerAlliance.includes('tiongkok')) {
        badgeStyle = "background-color: #ffedd5; color: #c2410c;"; // Oranye Terang (Front Persatuan Tiongkok)
      }

      const flagUrl = props.flagUrl || `/flags/${props.name.toLowerCase().replace(/ /g, '_')}.jpeg`;
      const allianceLabel = props.alliance === 'neutral' ? 'Netral' : props.alliance || 'Netral';

      popupContent = `
        <div style="min-width: 260px; font-family: sans-serif;">
          <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: bold; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">${props.name}</h3>
          <div style="display: flex; gap: 12px; align-items: flex-start;">
            <div style="flex-shrink: 0; width: 90px;">
              <img src="${flagUrl}" alt="Bendera ${props.name}" onerror="this.onerror=null;this.src='/flags/default.jpeg';" style="width: 100%; height: auto; border: 1px solid #cbd5e1; border-radius: 4px; object-fit: cover; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />
            </div>
            <div style="flex-grow: 1; font-size: 12px; line-height: 1.5; color: #334155;">
              <div style="margin-bottom: 6px;">
                <strong style="color: #64748b; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Pemimpin</strong> 
                <span style="font-weight: 500;">${props.leader || "Tidak diketahui"}</span>
              </div>
              <div style="margin-bottom: 6px;">
                <strong style="color: #64748b; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Ideologi</strong> 
                <span style="font-weight: 500;">${props.ideology || "Tidak diketahui"}</span>
              </div>
              <div>
                <strong style="color: #64748b; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Aliansi</strong> 
                <span style="${badgeStyle} padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700; display: inline-block;">${allianceLabel}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    } else {
      // Tampilkan nama negara secara default jika data spesifik belum ada
      popupContent = `<div style="font-weight: bold; font-family: sans-serif;">${countryName}</div>`;
    }

    // Event listener untuk klik (Toggle popup)
    layer.on('click', function(e: any) {
      if (layer.getPopup() && layer.isPopupOpen()) {
        layer.closePopup();
        layer.unbindPopup();
      } else {
        layer.bindPopup(popupContent).openPopup(e.latlng);
      }
    });

    // Menutup popup saat double click
    layer.on('dblclick', function() {
      if (layer.getPopup() && layer.isPopupOpen()) {
        layer.closePopup();
        layer.unbindPopup();
      }
    });
  };

  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden border border-gray-300 shadow-lg relative z-0">
      <MapContainer
        center={[30.0, 150.0]}
        zoom={2}
        minZoom={2}
        maxBounds={[
          [-90, -540],
          [90, 540]
        ]}
        maxBoundsViscosity={1.0}
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.esri.com/">Esri</a>'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
        />

        {/* Merender batas negara di tiga salinan bumi */}
        {WORLD_COPIES.map((offset) => (
          <GeoJSON
            key={`geojson-${offset}`}
            data={getShiftedGeoJSON(worldData1939, offset)}
            style={(feature) => ({
              color: feature?.properties?.color || '#3388ff',
              weight: 2,
              opacity: 1,
              fillOpacity: feature?.properties?.fillOpacity !== undefined
                ? feature.properties.fillOpacity
                : 0.5
            })}
            onEachFeature={onEachFeature}
          />
        ))}
      </MapContainer>
    </div>
  );
}

// Cache bust 1789547599656

// Cache bust 1789547786205
