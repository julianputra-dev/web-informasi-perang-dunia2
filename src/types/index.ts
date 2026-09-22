/**
 * Shared TypeScript interfaces untuk proyek WW2 History Web.
 */

/** Peristiwa sejarah dari database Supabase */
export interface HistoricalEvent {
  id: number;
  nama_peristiwa: string;
  deskripsi: string;
  tahun: number;
  lat: number;
  lng: number;
}

/** Properties dari setiap feature di GeoJSON peta */
export interface MapFeatureProperties {
  name: string;
  alliance: 'axis' | 'allies' | 'comintern' | string;
  color: string;
  fillOpacity?: number;
  leader?: string;
  ideology?: string;
}
