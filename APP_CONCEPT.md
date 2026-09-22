# Kerangka & Konsep Utama Aplikasi (WW2 History Web)

Dokumen ini berfungsi sebagai panduan dan konteks utama (guardrails) bagi AI dan developer agar pengembangan aplikasi tidak melenceng dari konsep aslinya.

## 🎯 Konsep Inti Aplikasi
Aplikasi ini adalah **Web Informasi dan Edukasi Sejarah Perang Dunia II (1938 - 1946)**. 
Tujuan utamanya adalah menyajikan kondisi geopolitik, batas wilayah negara, dan peristiwa sejarah secara interaktif.

1. **Titik Awal (Default State):** Saat pertama dimuat, web menyajikan kondisi dunia pada tahun **1938/1939**.
2. **Interaktivitas Waktu (Garis Waktu/Timeline):** Pengguna memiliki kebebasan untuk mengubah tahun melalui tuas (*slider*) dari tahun 1938 hingga 1946.
3. **Reaktivitas Peta (MAB - Map of the World):** Perubahan tahun pada *timeline* **wajib** mengakibatkan:
   - Perubahan batas wilayah negara di peta interaktif (berdasarkan kondisi geopolitik tahun tersebut).
   - Perubahan aliansi, warna negara, dan data pemimpin negara.
   - Perubahan titik-titik peristiwa penting (Historical Events) yang muncul di atas peta.

## 🏗️ Arsitektur & Tech Stack
- **Framework Utama:** Next.js (App Router) dengan TypeScript.
- **Styling:** Tailwind CSS (pertahankan desain modern, rapi, dan informatif).
- **Peta Interaktif (MAB):** Leaflet & React-Leaflet (`react-leaflet`).
- **Database (BaaS):** Supabase (Digunakan untuk menyimpan daftar kejadian historis/peristiwa dan koordinatnya).
- **Format Data Peta:** GeoJSON (`src/data/geojson/`). Data batas wilayah dan atribut negara dipasok melalui file GeoJSON.

## ⚙️ Cara Kerja Fitur Utama (Alur Data)
1. **State Tahun (`src/components/sections/TimelineSection.tsx`):**
   Terdapat *state* React (misal `tahun`) yang dikendalikan oleh input *slider*. State ini bertindak sebagai "sumber kebenaran" (*source of truth*) untuk periode waktu yang sedang diamati.

2. **Komponen Peta (`src/components/map/InteractiveMap.tsx`):**
   - Komponen ini menerima *props* `currentYear` (tahun saat ini).
   - Peta menggunakan data **GeoJSON** untuk merender poligon (batas wilayah negara).
   - Data negara (nama pemimpin, kubu/aliansi, ideologi, bendera) dirender berdasarkan *properties* negara yang terikat dengan tahun tersebut.
   - Peta direplikasi (di-*shift* koordinat longitudenya menggunakan `WORLD_COPIES`) agar bisa digeser terus-menerus tanpa terpotong (Infinite Panning).

3. **Data Events (`src/types/index.ts` - `HistoricalEvent`):**
   - Aplikasi menarik data dari Supabase yang memiliki struktur (ID, nama, deskripsi, tahun, lat, lng). 
   - Event yang ditampilkan di peta harus di-filter agar *hanya* memunculkan event yang terjadi pada tahun yang sedang dipilih (`currentYear`).

## 🛑 Aturan Ketat untuk AI (AI Guardrails)
1. **DILARANG** mengubah fokus utama web menjadi selain Perang Dunia II (1938-1946).
2. **WAJIB** mempertahankan kaitan antara komponen *Timeline* (Garis Waktu) dan komponen *Map* (Peta). Jangan memisahkan fungsionalitas keduanya. Perubahan *state* tahun harus selalu di-passing ke komponen peta.
3. **PENGELOLAAN GEOJSON:** Jika menambahkan data tahun baru (misal batas wilayah 1941), jangan merusak format struktur map yang sudah ada (harus sesuai dengan `MapFeatureProperties`). 
4. **PERFORMA PETA:** Karena interaksi map dengan layer GeoJSON cukup berat, pastikan logika *re-render* dioptimasi (gunakan efek yang tepat atau batasi iterasi data yang tidak perlu saat tuas tahun digeser).
5. **KONSISTENSI UI/UX:** Gunakan palet warna yang kohesif (Blok Poros, Sekutu, Komintern, Netral) yang sudah ada di konfigurasi atau komponen.

> Dokumen ini harus selalu dibaca dan dipahami sebelum mengimplementasikan fitur logika besar atau mengubah struktur dari komponen Peta dan Timeline.
