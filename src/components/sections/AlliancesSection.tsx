/**
 * Section kubu-kubu yang terlibat dalam Perang Dunia II.
 */
export default function AlliancesSection() {
  return (
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
  );
}
