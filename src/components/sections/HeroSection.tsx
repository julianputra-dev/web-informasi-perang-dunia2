/**
 * Hero section — header utama halaman.
 */
export default function HeroSection() {
  return (
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
  );
}
