'use client';

import dynamic from 'next/dynamic';
import { useState } from 'react';

const DynamicMap = dynamic(() => import('@/src/components/map/InteractiveMap'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] flex items-center justify-center bg-slate-800 text-white rounded-xl animate-pulse">
      Menghubungkan ke satelit arsip sejarah...
    </div>
  )
});

/**
 * Section timeline interaktif — berisi slider tahun dan peta.
 * Komponen ini client-side karena menggunakan state untuk tahun.
 */
export default function TimelineSection() {
  const [tahun, setTahun] = useState(1939);

  return (
    <section id="peta-interaktif" className="scroll-mt-12">
      <div className="mb-6">
        <h2 className="text-3xl font-bold mb-2 text-slate-900">Jelajahi Garis Waktu</h2>
        <p className="text-slate-600">Geser tuas di bawah ini untuk melihat peristiwa besar yang terjadi pada tahun tersebut.</p>
      </div>
      
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 mb-6">
        <div className="flex items-center justify-between mb-4">
          <label className="text-2xl font-black text-slate-800">Tahun: {tahun}</label>
          <span className="text-sm font-semibold text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
            Era Perang
          </span>
        </div>
        <input 
          type="range" 
          min="1938" 
          max="1946" 
          step="1" 
          value={tahun} 
          onChange={(e) => setTahun(parseInt(e.target.value))}
          className="w-full h-3 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
        />
        <div className="flex justify-between text-xs font-bold text-slate-400 mt-2 px-1">
          <span>1938</span>
          <span>1942</span>
          <span>1946</span>
        </div>
      </div>

      <DynamicMap currentYear={tahun} />
    </section>
  );
}
