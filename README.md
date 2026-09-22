# 🌍 Arsip Interaktif Perang Dunia II

Aplikasi web edukasi interaktif yang menyajikan sejarah Perang Dunia II melalui peta, garis waktu, dan arsip peristiwa penting dari tahun 1938–1946.

## ✨ Fitur

- **Peta Interaktif** — Visualisasi batas negara tahun 1939 menggunakan data GeoJSON historis
- **Garis Waktu** — Slider untuk menjelajahi peristiwa berdasarkan tahun
- **Informasi Edukatif** — Latar belakang, kubu yang terlibat, dan dampak perang

## 🛠 Tech Stack

| Teknologi | Kegunaan |
|-----------|----------|
| [Next.js](https://nextjs.org) | Framework React full-stack |
| [Leaflet](https://leafletjs.com) + [React Leaflet](https://react-leaflet.js.org) | Peta interaktif |
| [Supabase](https://supabase.com) | Database peristiwa sejarah |
| [Tailwind CSS](https://tailwindcss.com) | Styling |
| [TypeScript](https://typescriptlang.org) | Type safety |

## 📁 Struktur Proyek

```
src/
├── app/                    # Halaman Next.js (App Router)
│   ├── layout.tsx          # Root layout & metadata
│   └── page.tsx            # Halaman utama
├── components/
│   ├── map/                # Komponen peta
│   │   ├── InteractiveMap.tsx
│   │   └── map-utils.ts
│   └── sections/           # Section halaman utama
│       ├── HeroSection.tsx
│       ├── BackgroundSection.tsx
│       ├── TimelineSection.tsx
│       ├── AlliancesSection.tsx
│       ├── ImpactSection.tsx
│       └── Footer.tsx
├── data/
│   └── geojson/            # Data GeoJSON batas negara
│       └── world-1939.json
├── lib/
│   └── supabase.ts         # Supabase client
└── types/
    └── index.ts            # Shared TypeScript interfaces

scripts/
└── map-processing/         # Script untuk memproses data peta
    ├── extract_map.py
    └── data/               # Data mentah (di-gitignore)
```

## 🚀 Menjalankan Proyek

```bash
# Install dependencies
npm install

# Jalankan development server
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000) di browser.

## ⚙️ Environment Variables

Buat file `.env.local` dengan konfigurasi berikut:

```env
NEXT_PUBLIC_SUPABASE_URL=<url_supabase_anda>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key_supabase_anda>
```

## 📜 Lisensi

Dibuat untuk tujuan edukasi.
