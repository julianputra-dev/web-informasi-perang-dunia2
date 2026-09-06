'use client';

import dynamic from 'next/dynamic';
import { useState } from 'react';

// Memuat komponen Map secara dinamis
const DynamicMap = dynamic(() => import('@/src/components/Map'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] flex items-center justify-center bg-slate-800 text-white rounded-xl animate-pulse">
      Menghubungkan ke satelit arsip sejarah...
    </div>
  )
});

export default function Home() {
  const [tahun, setTahun] = useState(1939);

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      {/* 1. HERO SECTION */}
      <header className="bg-slate-900 text-white py-20 px-6 text-center shadow-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 tracking-tight">
            Arsip Interaktif Perang Dunia II
          </h1>
          <p className="text-lg md:text-xl text-slate-300 leading-relaxed">
            Menelusuri jejak konflik terbesar dalam sejarah umat manusia. 
            Pelajari latar belakang, negara yang terlibat, dan jelajahi peristiwa penting melalui peta interaktif historis.
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12 space-y-20">
        
        {/* 2. LATAR BELAKANG */}
        <section className="bg-white p-8 md:p-12 rounded-2xl shadow-sm border border-slate-200">
          <h2 className="text-3xl font-bold mb-6 border-b pb-4 text-slate-900">Latar Belakang & Awal Mula</h2>
          <div className="grid md:grid-cols-2 gap-8 text-slate-600 text-lg leading-relaxed">
            <p>
              Perang Dunia II berakar dari ketidakstabilan Eropa pasca Perang Dunia I dan Perjanjian Versailles yang memberatkan Jerman. Kondisi ekonomi yang hancur dan krisis global pada 1930-an memfasilitasi kebangkitan rezim fasis dan totaliter, terutama di Jerman, Italia, dan Jepang.
            </p>
            <p>
              Perang secara resmi pecah pada tanggal <strong>1 September 1939</strong>, ketika Jerman Nazi yang dipimpin Adolf Hitler menginvasi Polandia. Hal ini memicu Inggris dan Prancis untuk menyatakan perang terhadap Jerman, menyeret dunia ke dalam konflik mematikan yang berlangsung hingga tahun 1945.
            </p>
          </div>
        </section>

        {/* 3. PETA INTERAKTIF & SLIDER */}
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

          {/* Render Peta */}
          <DynamicMap currentYear={tahun} />
        </section>

        {/* 4. BLOK NEGARA */}
        <section>
          <h2 className="text-3xl font-bold mb-8 text-center text-slate-900">Kubu yang Terlibat</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {/* Blok Sekutu */}
            <div className="bg-blue-50 p-8 rounded-2xl border border-blue-100 shadow-sm">
              <h3 className="text-2xl font-bold text-blue-900 mb-4 flex items-center gap-2">
                <span className="w-4 h-4 rounded-full bg-blue-600 inline-block"></span> Blok Sekutu
              </h3>
              <p className="text-blue-800 mb-4">
                Aliansi negara-negara yang bersatu untuk menghentikan agresi Blok Poros. Kekuatan utama sekutu dijuluki &quot;The Big Three&quot;.
              </p>
              <ul className="list-disc list-inside text-blue-900 font-medium space-y-1">
                <li>Uni Soviet</li>
                <li>Amerika Serikat</li>
                <li>Britania Raya</li>
                <li>Tiongkok</li>
                <li>Prancis (Pasukan Pembebasan)</li>
              </ul>
            </div>

            {/* Blok Poros */}
            <div className="bg-red-50 p-8 rounded-2xl border border-red-100 shadow-sm">
              <h3 className="text-2xl font-bold text-red-900 mb-4 flex items-center gap-2">
                <span className="w-4 h-4 rounded-full bg-red-600 inline-block"></span> Blok Poros
              </h3>
              <p className="text-red-800 mb-4">
                Aliansi militer yang dipelopori oleh perjanjian Pakta Tripartit. Bertujuan untuk memperluas wilayah kekuasaan hegemonik mereka.
              </p>
              <ul className="list-disc list-inside text-red-900 font-medium space-y-1">
                <li>Jerman Nazi</li>
                <li>Kekaisaran Jepang</li>
                <li>Kerajaan Italia</li>
                <li>Rumania</li>
                <li>Hungaria</li>
              </ul>
            </div>
          </div>
        </section>

        {/* 5. DAMPAK PERANG */}
        <section className="bg-slate-900 text-white p-8 md:p-12 rounded-2xl shadow-lg">
          <h2 className="text-3xl font-bold mb-6 border-b border-slate-700 pb-4">Dampak Peperangan</h2>
          <p className="text-slate-300 text-lg leading-relaxed mb-6">
            Perang Dunia II adalah konflik paling mematikan dalam sejarah, mengakibatkan diperkirakan 70 hingga 85 juta korban jiwa, yang merupakan sekitar 3% dari populasi dunia tahun 1940.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h4 className="font-bold text-xl mb-2 text-blue-400">Geopolitik Baru</h4>
              <p className="text-sm text-slate-400">Runtuhnya kekaisaran Eropa tradisional dan munculnya dua negara adidaya baru: Amerika Serikat dan Uni Soviet, yang memicu Perang Dingin.</p>
            </div>
            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h4 className="font-bold text-xl mb-2 text-blue-400">PBB Didirikan</h4>
              <p className="text-sm text-slate-400">Pembentukan Perserikatan Bangsa-Bangsa (PBB) pada tahun 1945 untuk mendorong kerja sama internasional dan mencegah konflik masa depan.</p>
            </div>
            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h4 className="font-bold text-xl mb-2 text-blue-400">Dekolonisasi</h4>
              <p className="text-sm text-slate-400">Melemahnya kekuatan negara-negara Eropa mendorong gelombang kemerdekaan bagi banyak negara terjajah di Asia dan Afrika, termasuk Indonesia.</p>
            </div>
          </div>
        </section>

      </main>

      {/* FOOTER */}
      <footer className="bg-slate-100 border-t border-slate-200 py-8 text-center text-slate-500 mt-12">
        <p>© {new Date().getFullYear()} Arsip Sejarah PD2. Dibuat untuk tujuan edukasi.</p>
      </footer>
    </div>
  );
}