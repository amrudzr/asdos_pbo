# Problem Statement: Sistem Automasi Penilaian Tugas PBO

## 1. Latar Belakang
Sebagai Asisten Dosen untuk mata kuliah Pemrograman Berorientasi Objek (PBO), terdapat tanggung jawab untuk mengoreksi dan menilai tugas proyek mahasiswa secara rutin. Proyek yang dikumpulkan berupa arsip dari aplikasi Greenfoot (format `.gfar`) dan Eclipse. Saat ini, proses ekstraksi file, pengecekan orisinalitas kode, serta perhitungan nilai akhir berdasarkan metrik kedisiplinan dan kelengkapan masih dilakukan secara manual. Hal ini memakan waktu yang sangat tidak efisien mengingat tingginya volume mahasiswa.

## 2. Identifikasi Masalah Utama
* **Ekstraksi Manual:** File `.gfar` dan arsip Eclipse harus diekstrak satu per satu untuk dapat membaca struktur kode dan dokumentasi mahasiswa.
* **Validasi Orisinalitas yang Bias:** Mengandalkan pengecekan visual (mata telanjang) untuk menentukan apakah sebuah *project* "sama/mirip dengan lainnya" sangat rentan terhadap kesalahan dan inkonsistensi.
* **Kalkulasi Denda Keterlambatan:** Melacak *timestamp* pengumpulan dari setiap mahasiswa dan menghitung denda poin per minggu secara manual memperlambat proses *grading*.
* **Manajemen Waktu:** Proses koreksi manual mengganggu alokasi waktu untuk tugas operasional atau pengembangan proyek lainnya.

## 3. Aturan Bisnis (Scoring Rules)
Sistem atau *script* otomasi yang akan dikembangkan harus mematuhi logika penilaian mutlak berikut:

| Kriteria / Kondisi | Nilai Dasar |
| :--- | :--- |
| Selesai tepat waktu **AND** Isi project unik/beda **AND** Ada penjelasan | `90` |
| Selesai tepat waktu (Tidak memenuhi kondisi spesifik lain) | `RAND(80, 85)` |
| Selesai tepat waktu **AND** Project sama/mirip **AND** Ada penjelasan | `69` |

**Modifier Keterlambatan:** * Setiap keterlambatan dihitung **-1 poin per minggu** setelah jam *deadline*. (Total Nilai = Nilai Dasar - Poin Denda).

## 4. Ekspektasi Solusi (Menuju PRD)
Dibutuhkan sebuah *workflow* otomasi (berupa *script* atau *micro-tool*) yang mampu:
1. Membaca dan mengekstrak *batch* file `.gfar` dan `.zip` secara massal.
2. Membantu mendeteksi tingkat kemiripan kode antar mahasiswa secara otomatis (misalnya mengintegrasikan logika algoritma komparasi teks atau MOSS).
3. Mengkalkulasi nilai akhir berdasarkan *Scoring Rules* dan menghasilkan *output* rekapitulasi nilai.

## 5. Batasan & Standar Teknis (Technical Constraints)
Untuk menjaga kebersihan *codebase* dan lokalisasi saat solusi ini dikembangkan:
* **Penamaan Variabel & Kode:** Seluruh variabel dan logika sistem (termasuk *script* otomasi) wajib menggunakan bahasa Inggris.
* **Kebersihan Kode:** Kode harus sepenuhnya bersih dari komentar (zero comments).
* **Lokalisasi Output:** Semua pesan validasi sistem, notifikasi error, dan pesan hasil rekapitulasi untuk *user* harus menggunakan bahasa Indonesia.
* **Manajemen Tugas:** *Tracking* pengembangan fitur untuk solusi otomasi ini akan dikelola menggunakan Jira (Hindari penggunaan GitHub Projects).