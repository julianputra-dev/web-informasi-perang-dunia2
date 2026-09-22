import HeroSection from '@/src/components/sections/HeroSection';
import BackgroundSection from '@/src/components/sections/BackgroundSection';
import TimelineSection from '@/src/components/sections/TimelineSection';
import AlliancesSection from '@/src/components/sections/AlliancesSection';
import ImpactSection from '@/src/components/sections/ImpactSection';
import Footer from '@/src/components/sections/Footer';

/**
 * Halaman utama — Arsip Interaktif Perang Dunia II.
 * Setiap section dipisah menjadi komponen tersendiri untuk kemudahan maintenance.
 */
export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      <HeroSection />

      <main className="max-w-7xl mx-auto px-6 py-12 space-y-20">
        <BackgroundSection />
        <TimelineSection />
        <AlliancesSection />
        <ImpactSection />
      </main>

      <Footer />
    </div>
  );
}