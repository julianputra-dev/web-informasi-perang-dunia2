/**
 * Section dampak Perang Dunia II.
 */
export default function ImpactSection() {
  return (
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
  );
}
