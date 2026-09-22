/**
 * Footer — bagian bawah halaman.
 */
export default function Footer() {
  return (
    <footer className="bg-slate-100 border-t border-slate-200 py-8 text-center text-slate-500 mt-12">
      <p>© {new Date().getFullYear()} Arsip Sejarah PD2. Dibuat untuk tujuan edukasi.</p>
    </footer>
  );
}
