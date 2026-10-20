# ITB Fun Run 2026 — Marketing Report

Dashboard statis responsif untuk evaluasi aktivitas marketing RFID Total Solution sebagai penyedia race timing system. Tidak memakai framework, build step, atau dependency eksternal.

## Lihat secara lokal

Jalankan server lokal dari folder repo:

```bash
python -m http.server 8000
```

Lalu buka <http://localhost:8000>. (Membuka `index.html` langsung via `file://` tidak mendukung `fetch()` untuk membaca `data.json` di beberapa browser.)

## Ganti dengan data aktual

Edit `data.json`; struktur ringkas:

- `kpis`: nilai kartu ringkasan. `value: null` menampilkan `—` saat data belum tersedia.
- `awareness`: jangkauan dan impresi menurut `channel` dan `period`.
- `engagement`: interaksi menurut `channel` dan `period`.
- `activities`: aktivitas pada tiap tahap acara.
- `evaluation`: poin evaluasi berbasis temuan.
- `nextSteps`: rekomendasi tindak lanjut.
- `sources`, `periodLabel`: catatan sumber dan periode.
- `isIllustrative`: ubah ke `false` hanya setelah angka dan copy contoh diganti dengan data yang tervalidasi. Jika `true`, banner data ilustrasi ditampilkan.

Periode pada data grafis harus konsisten dengan daftar `periods`. Jangkauan, impresi, interaksi, dan partisipasi punya definisi masing-masing—jangan dijumlahkan menjadi satu angka tanpa dasar yang jelas. Jangan gunakan jangkauan sebagai pengganti brand recall.

## Publikasikan lewat GitHub Pages

1. Buat repository kosong di GitHub dengan nama pilihan.
2. Dari folder project, jalankan:

   ```bash
   git init
   git add index.html data.json README.md tests .gitignore
   git commit -m "Create ITB Fun Run 2026 marketing report"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPOSITORY.git
   git push -u origin main
   ```

3. Di GitHub, buka **Settings → Pages**. Pada **Build and deployment**, pilih **Deploy from a branch**, branch `main`, folder `/(root)`, lalu **Save**.
4. Tunggu deployment selesai; URL halaman tampil di bagian Pages.

Ganti URL remote dengan URL repository yang benar. Jangan publish sebelum placeholder/ilustrasi diganti atau report memang dimaksudkan sebagai mockup.

## Smoke test

```bash
python -m unittest discover -s tests -v
```

Lisensi: internal draft; tambahkan lisensi sesuai kebutuhan sebelum distribusi publik.
