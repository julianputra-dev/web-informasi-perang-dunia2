'use client';

import { useState } from 'react';

type CountryInfo = {
  name: string;
  leader: string;
  ideology: string;
  alliance: string;
  flagUrl: string;
};

// Mock data untuk uji coba
const countryData: Record<string, CountryInfo> = {
  jerman: {
    name: 'Jerman Nazi',
    leader: 'Adolf Hitler',
    ideology: 'Fasisme / Nazisme',
    alliance: 'Blok Poros (Axis)',
    flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Flag_of_the_German_Reich_%281935%E2%80%931945%29.svg/320px-Flag_of_the_German_Reich_%281935%E2%80%931945%29.svg.png',
  },
};

export default function CountrySearch() {
  const [searchTerm, setSearchTerm] = useState('');
  const [countryInfo, setCountryInfo] = useState<CountryInfo | null>(null);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    const key = value.toLowerCase().trim();
    if (countryData[key]) {
      setCountryInfo(countryData[key]);
    } else {
      setCountryInfo(null);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto relative z-10 mb-12">
      <div className="relative">
        <input
          type="text"
          value={searchTerm}
          onChange={handleSearch}
          placeholder="Ketik wilayah negara (contoh: Jerman)..."
          className="w-full px-6 py-4 rounded-full border-2 border-slate-300 focus:outline-none focus:border-blue-500 shadow-sm text-lg transition-colors bg-white text-slate-800"
        />
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {countryInfo && (
        <div className="absolute top-full mt-4 w-full bg-white rounded-2xl shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in slide-in-from-top-4 duration-300">
          <div className="p-6">
            <div className="flex items-start gap-6">
              <div className="w-1/3 shrink-0">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img 
                  src={countryInfo.flagUrl} 
                  alt={`Bendera ${countryInfo.name}`} 
                  className="w-full h-auto rounded border border-slate-200 shadow-sm object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'https://flagcdn.com/w320/de.png'; // fallback if wikipedia link breaks
                  }}
                />
              </div>
              <div className="w-2/3 space-y-3">
                <h3 className="text-2xl font-bold text-slate-900">{countryInfo.name}</h3>
                
                <div className="grid grid-cols-1 gap-2 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-500 w-24">Pemimpin:</span>
                    <span className="text-slate-800 font-medium">{countryInfo.leader}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-500 w-24">Ideologi:</span>
                    <span className="text-slate-800 font-medium">{countryInfo.ideology}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-500 w-24">Aliansi:</span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      {countryInfo.alliance}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
