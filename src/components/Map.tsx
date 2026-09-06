/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import borders1939 from '../data/germany_1939.json';
import { supabase } from '../lib/supabase';

interface HistoricalEvent {
  id: number;
  nama_peristiwa: string;
  deskripsi: string;
  tahun: number;
  lat: number;
  lng: number;
}

const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Fungsi untuk menggeser garis bujur (longitude) wilayah negara sejauh offset yang ditentukan
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function getShiftedGeoJSON(geojsonData: any, offset: number) {
  if (offset === 0) return geojsonData;
  
  const clonedData = JSON.parse(JSON.stringify(geojsonData));
  
  clonedData.features.forEach((feature: any) => {
    if (feature.geometry.type === 'Polygon') {
      feature.geometry.coordinates.forEach((ring: any) => {
        ring.forEach((coord: any) => { coord[0] += offset; });
      });
    } else if (feature.geometry.type === 'MultiPolygon') {
      feature.geometry.coordinates.forEach((polygon: any) => {
        polygon.forEach((ring: any) => {
          ring.forEach((coord: any) => { coord[0] += offset; });
        });
      });
    }
  });
  
  return clonedData;
}

export default function Map({ currentYear }: { currentYear: number }) {
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

  const filteredEvents = events.filter(event => event.tahun === currentYear);
  const worldCopies = [-360, 0, 360];

  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden border border-gray-300 shadow-lg relative z-0">
      <MapContainer
        center={[30.0, 150.0]}
        zoom={2}
        minZoom={2}
        maxBounds={[
          [-90, -540], // Batas dinding paling kiri
          [90, 540]    // Batas dinding paling kanan
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
        {worldCopies.map((offset) => (
          <GeoJSON 
            key={`geojson-${offset}`}
            data={getShiftedGeoJSON(borders1939, offset)} 
            style={(feature) => ({
              color: feature?.properties?.color || '#3388ff',
              weight: 2,
              opacity: 1,
              fillOpacity: feature?.properties?.fillOpacity !== undefined ? feature.properties.fillOpacity : 0.5
            })}
          />
        ))}

        {/* Merender titik peristiwa di tiga salinan bumi */}
        {/*
        {filteredEvents.map((event) => 
          worldCopies.map((offset) => (
            <Marker 
              key={`${event.id}-${offset}`} 
              position={[event.lat, event.lng + offset]} 
              icon={customIcon}
            >
              <Popup>
                <div className="p-1">
                  <h3 className="font-bold text-lg mb-1">{event.nama_peristiwa}</h3>
                  <p className="text-sm text-gray-600 mb-2">Tahun: {event.tahun}</p>
                  <p className="text-sm">{event.deskripsi}</p>
                </div>
              </Popup>
            </Marker>
          ))
        )}
        */}
      </MapContainer>
    </div>
  );
}