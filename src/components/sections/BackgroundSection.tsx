/**
 * Section latar belakang dan awal mula Perang Dunia II.
 */
export default function BackgroundSection() {
  return (
    <section className="bg-white p-8 md:p-12 rounded-2xl shadow-sm border border-slate-200">
      <h2 className="text-3xl font-bold mb-6 border-b pb-4 text-slate-900">Latar Belakang &amp; Awal Mula</h2>
      <div className="grid md:grid-cols-2 gap-8 text-slate-600 text-lg leading-relaxed">
        <p>
          Perang Dunia II berakar dari ketidakstabilan Eropa pasca Perang Dunia I dan Perjanjian Versailles yang memberatkan Jerman. Kondisi ekonomi yang hancur dan krisis global pada 1930-an memfasilitasi kebangkitan rezim fasis dan totaliter, terutama di Jerman, Italia, dan Jepang.
        </p>
        <p>
          Perang secara resmi pecah pada tanggal <strong>1 September 1939</strong>, ketika Jerman Nazi yang dipimpin Adolf Hitler menginvasi Polandia. Hal ini memicu Inggris dan Prancis untuk menyatakan perang terhadap Jerman, menyeret dunia ke dalam konflik mematikan yang berlangsung hingga tahun 1945.
        </p>
      </div>
    </section>
  );
}
