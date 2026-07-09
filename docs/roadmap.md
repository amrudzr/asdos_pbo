# Development Roadmap: Sistem Automasi Penilaian Tugas PBO

Berdasarkan Product Requirements Document (PRD), berikut adalah peta jalan (roadmap) pengembangan sistem yang dirancang dalam beberapa fase agar implementasi lebih terstruktur.

## Fase 1: Inisialisasi Proyek & Ekstraksi Dasar
**Fokus:** Menyiapkan struktur proyek dan memastikan file tugas dapat dibaca serta diekstrak.
* **Tugas 1.1:** Setup repository dan inisiasi struktur proyek (CLI tool/scripting).
* **Tugas 1.2:** Setup board dan manajemen tugas di Jira.
* **Tugas 1.3:** Pembuatan modul *Batch Extraction* untuk menangani file `.gfar` dan `.zip`.
* **Tugas 1.4:** Implementasi error handling (`Try-Catch`) untuk file *corrupt* atau terproteksi *password*, beserta mekanisme pencatatan ke *error log*.
* **Tugas 1.5:** Implementasi ekstraksi identitas (NIM) dari nama file atau folder menggunakan Regex untuk digunakan sebagai *Primary Key*.

## Fase 2: Modul Kompilasi & Mesin Validasi Plagiarisme
**Fokus:** Memastikan kode berjalan tanpa *error* dan membangun pendeteksi kemiripan *source code* secara otomatis dan akurat.
* **Tugas 2.1:** Pembuatan modul kompilasi otomatis (`src/compiler.py`) untuk mengecek *syntax error* menggunakan `javac` (mendukung injeksi `.jar` eksternal).
* **Tugas 2.2:** Pembuatan fitur pembaca dan pemroses *source code* dari file yang telah terekstrak untuk modul plagiarisme.
* **Tugas 2.3:** Integrasi algoritma komparasi teks (misalnya Tokenisasi/AST) atau *tool* eksternal seperti MOSS.
* **Tugas 2.4:** Pembuatan fitur *exclude* / pengecualian terhadap file *template* standar dosen untuk menghindari *False Positive*.
* **Tugas 2.5:** Penentuan ambang batas (*threshold*) kemiripan, misalnya menetapkan *flag* plagiat jika persentase kemiripan > 80%.

## Fase 3: Modul Perhitungan Nilai (Scoring Engine) & Input Parameter
**Fokus:** Mengkalkulasi nilai akhir berdasarkan aturan bisnis mutlak dan denda keterlambatan.
* **Tugas 3.1:** Pembuatan *prompt* untuk menerima input pengguna berupa waktu *deadline* dan waktu pengumpulan.
* **Tugas 3.2:** Pembuatan *parser* dan validasi *timestamp* khusus (`[Hari], [DD] [Bulan] [YYYY], [H]:[MM] [AM/PM]`).
* **Tugas 3.3:** Penambahan validasi batas wajar (*sanity check*) untuk keterlambatan yang melebihi 4 minggu.
* **Tugas 3.4:** Implementasi logika *Base Score*: Orisinal lengkap (90), Orisinal kurang lengkap (80-85), Plagiat (69), dan Gagal Kompilasi (0-50).
* **Tugas 3.5:** Implementasi logika *Late Penalty* (pemotongan 1 poin per minggu keterlambatan) yang dikurangi dari nilai dasar.

## Fase 4: Modul Reporting, Integrasi Spreadsheet, & Testing
**Fokus:** Menghasilkan rekapitulasi data akhir ke dalam spreadsheet dan memastikan sistem stabil.
* **Tugas 4.1:** Pembuatan modul output berupa tabel konsol yang interaktif.
* **Tugas 4.2:** Integrasi ekspor laporan secara langsung ke **Spreadsheet** (Google Sheets API atau Excel/openpyxl), beserta *fallback* ke format **CSV**. Kolom: Nama/NIM, Nilai Dasar, Denda Poin, dan Nilai Akhir.
* **Tugas 4.3:** Memastikan semua pesan untuk pengguna (*error message*, log, notifikasi) telah dilokalisasi ke dalam Bahasa Indonesia sesuai PRD, dengan tetap mempertahankan penulisan *source code* dalam Bahasa Inggris.
* **Tugas 4.4:** *End-to-End Testing* menggunakan *dummy data* untuk memvalidasi performa (peningkatan > 70% kecepatan) dan akurasi skor.
