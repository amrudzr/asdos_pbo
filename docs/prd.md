# Product Requirements Document (PRD)
**Sistem Automasi Penilaian Tugas PBO (Pemrograman Berorientasi Objek)**

## 1. Latar Belakang & Ringkasan Eksekutif
Sebagai Asisten Dosen (Asdos) mata kuliah PBO, terdapat tanggung jawab mengoreksi tugas proyek mahasiswa (berupa arsip aplikasi Greenfoot `.gfar` dan arsip Eclipse `.zip`) secara rutin. Proses saat ini masih dilakukan sepenuhnya manual—mulai dari ekstraksi file satu per satu, pengecekan orisinalitas kode secara visual (yang rentan dengan bias dan inkonsistensi), hingga pelacakan dan perhitungan denda poin keterlambatan. Proses manual ini memakan waktu yang sangat tidak efisien mengingat tingginya volume mahasiswa. 

Sistem Automasi Penilaian Tugas PBO ini dirancang sebagai sebuah *workflow automation* (berupa skrip atau *micro-tool*) untuk merampingkan proses evaluasi, sehingga Asdos dapat menghemat banyak waktu yang sebelumnya terbuang pada tugas repetitif.

## 2. Objektif Produk
* **Otomasi Proses Ekstraksi:** Membuka dan mengekstrak berkas arsip tugas mahasiswa secara *batch*.
* **Verifikasi Kode Otomatis:** Memastikan *source code* mahasiswa dapat dikompilasi (*compile*) tanpa *error syntax* untuk menjamin kode dapat dijalankan.
* **Standardisasi Validasi Orisinalitas:** Mendeteksi kemiripan *source code* antar mahasiswa secara otomatis, untuk menghilangkan bias dari pengecekan manual.
* **Otomasi Perhitungan Nilai:** Mengkalkulasi nilai akhir berdasarkan standar aturan bisnis mutlak (mencakup kelengkapan fitur, orisinalitas, dan pemotongan denda keterlambatan).
* **Integrasi Nilai Langsung:** Mengirimkan hasil akhir kalkulasi nilai langsung ke dalam *spreadsheet* (Google Sheets atau Excel) untuk menghilangkan proses pemindahan data secara manual.

## 3. Target Pengguna
* **Asisten Dosen (Asdos) PBO:** Pengguna yang membutuhkan alat (*tools*) bantu untuk mempercepat proses *grading* tugas secara massal, adil, dan objektif.

## 4. Kebutuhan Fungsional (Functional Requirements)
1. **Modul Ekstraksi Massal:** Sistem harus mampu mengekstrak file berekstensi `.gfar` dan arsip `.zip` dalam jumlah banyak secara bersamaan ke struktur direktori yang terbaca.
2. **Modul Input Parameter (Manual):** Sistem harus memfasilitasi pengguna untuk melakukan input manual terkait **waktu *deadline*** dan **waktu pengumpulan tugas** (*timestamp*) dari masing-masing mahasiswa untuk keperluan perhitungan denda.
3. **Modul Kompilasi & Verifikasi Kode:** Sistem harus dapat melakukan kompilasi otomatis (*compilation check*) terhadap file `.java` mahasiswa untuk memastikan tidak ada *syntax error* dan kode dapat berjalan.
4. **Modul Pendeteksi Plagiarisme:** Sistem harus mampu membandingkan kode dari seluruh mahasiswa untuk mendeteksi tingkat kemiripan (bisa diimplementasikan menggunakan algoritma komparasi teks atau tool seperti MOSS).
5. **Modul Kalkulasi Nilai:** Sistem harus dapat mengeksekusi logika nilai berdasarkan "Scoring Rules" (lihat section 6) untuk menghasilkan skor akhir masing-masing siswa.
6. **Modul *Reporting* & Integrasi Spreadsheet:** Sistem harus mengeluarkan rekapitulasi data *output* yang terstruktur dan langsung menuliskan (*export*) hasilnya ke dalam *spreadsheet* (seperti Google Sheets melalui API, atau MS Excel) sehingga tidak diperlukan *copy-paste*. Sebagai cadangan, sistem tetap mencetak tabel di konsol dan *file* CSV.

## 5. Kebutuhan Non-Fungsional (Technical Constraints)
1. **Bahasa Pemrograman / Penamaan Variabel:** Seluruh penulisan kode untuk logika automasi, penamaan variabel, fungsi, dsb. *wajib* menggunakan bahasa Inggris.
2. **Kualitas dan Pemeliharaan Kode:** Penulisan komentar (comments) dalam kode sangat diperbolehkan untuk mempermudah perbaikan (*maintenance*) dan menjelaskan alur skrip di masa depan.
3. **Lokalisasi Output Pengguna:** Segala bentuk *interface*, notifikasi aplikasi, pesan *error*, log peringatan, dan hasil rekapitulasi nilai untuk pengguna (Asdos) *wajib* menggunakan bahasa Indonesia.
4. **Manajemen Proyek & Tugas:** Pelacakan pengembangan fitur (task tracking) dan penanganan *issue* terkait pembuatan sistem ini dikelola menggunakan platform *issue tracking* internal tim.

## 6. Aturan Bisnis (Scoring Rules Engine)
Sistem harus menghitung nilai berdasarkan ketentuan mutlak berikut ini:

### A. Penentuan Nilai Dasar (Base Score)
| Kriteria / Kondisi Proyek Mahasiswa | Nilai Dasar |
| :--- | :--- |
| **Unik/Beda** (Orisinal) **AND** Memiliki penjelasan yang sesuai | **90** |
| **Unik/Beda** (Orisinal) **TAPI** Fitur kurang lengkap / Penjelasan kurang | **80 - 85** *(Angka ditentukan berdasarkan kelengkapan fitur dari proyek)* |
| **Gagal Kompilasi** (*Syntax Error*) | **0 - 50** *(Bergantung kebijakan, program tidak bisa jalan)* |
| **Sama/Mirip** (*Plagiarism detected*) | **69** *(Pukul rata 69, baik terdapat penjelasan maupun tidak)* |

### B. Modifier Denda Keterlambatan (Late Penalty)
* Untuk mahasiswa yang **terlambat**, penentuan *Nilai Dasar* tetap berpatokan pada tabel di atas.
* Setiap keterlambatan dikenakan denda berupa **pengurangan 1 poin per minggu**, dihitung dari selisih waktu pengumpulan dengan batas waktu *deadline* yang ditentukan (yang diinput manual).
* **Formula Final:** `Nilai Akhir = Nilai Dasar - (Total Minggu Keterlambatan * 1)`

## 7. Metrik Kesuksesan (Success Metrics)
* Waktu yang dibutuhkan asdos untuk memvalidasi plagiarisme dan menghitung nilai berkurang secara signifikan (misalnya > 70% lebih cepat).
* Terhapusnya kesalahan manusia (*human error*) dalam merekap nilai denda keterlambatan.

## 8. Mitigasi Risiko & Penanganan Kesalahan (Error Handling)
Agar *output* yang dihasilkan sistem akurat, efektif, dan efisien, beberapa potensi kesalahan berikut harus ditangani sejak fase pengembangan:

1. **Ekstraksi File Gagal / Corrupt**
   * **Risiko:** File arsip `.gfar` atau `.zip` mahasiswa rusak (*corrupt*), terproteksi *password*, atau strukturnya berantakan (tidak ada *root folder*).
   * **Mitigasi:** Implementasikan penanganan *error* (`Try-Catch`) pada modul ekstraksi. Jika satu file bermasalah, skrip tidak boleh terhenti (*crash*). File tersebut diabaikan, dicatat ke dalam *error log* khusus, lalu sistem lanjut memproses file mahasiswa berikutnya.

2. **Positif Palsu (*False Positive*) pada Deteksi Plagiarisme**
   * **Risiko:** Sistem menganggap dua *project* mirip karena menggunakan *template* kode (*boilerplate*) atau *library* standar bawaan tugas.
   * **Mitigasi:** Sistem harus mendukung pengecualian (*exclude*) *file* standar dosen sebelum membandingkan kode. Lebih baik gunakan metode tokenisasi/AST (*Abstract Syntax Tree*) ketimbang komparasi teks sederhana. Tetapkan ambang batas wajar (misal: flag plagiat hanya jika kemiripan > 80%).

3. **Inkonsistensi Nilai pada Range 80-85**
   * **Risiko:** Menilai "kelengkapan fitur" butuh konteks semantik yang sulit diotomasi. Jika dipaksa acak, akan merugikan mahasiswa.
   * **Mitigasi:** Modul kalkulasi dapat memberikan *flag* penanda **"REVIEW MANUAL"** untuk skor di kategori ini, atau secara otomatis memberi *default score* (misal 80) yang kemudian bisa *di-override* oleh Asdos secara manual jika terbukti fiturnya sangat lengkap.

4. **Format Input Waktu Keterlambatan (*Timestamp*) yang Tidak Valid**
   * **Risiko:** Asdos salah atau *typo* (salah *copy-paste*) memasukkan format *timestamp* dari *web*, sehingga denda keterlambatan melonjak tajam menjadi tidak masuk akal.
   * **Mitigasi:** Validasi dan *parsing* input *timestamp* secara otomatis disesuaikan secara khusus (*tailor-made*) dengan format bawaan dari web Asdos, yaitu `[Hari], [DD] [Bulan] [YYYY], [H]:[MM] [AM/PM]` (contoh: `Monday, 20 April 2026, 7:43 PM`). Skrip akan membaca pola ini alih-alih format ISO baku. Tambahkan pembatasan (*sanity check*): jika total keterlambatan lebih dari 4 minggu, sistem menampilkan *prompt* konfirmasi sebelum melanjutkan.

5. **Kesalahan Konversi Identitas Mahasiswa (Parsing Error)**
   * **Risiko:** Mahasiswa tidak menamai file `.zip` sesuai aturan, sehingga rekapan nilai berantakan dan nama tertukar.
   * **Mitigasi:** Sistem menggunakan aturan berbasis pola (*Regular Expression* / Regex) untuk secara cerdas mengekstrak NIM dari nama file/folder. NIM tersebut dijadikan pengenal unik (*Primary Key*) dalam *spreadsheet*.

6. **Kegagalan Koneksi ke API Spreadsheet**
   * **Risiko:** Gagal menulis data rekapitulasi ke Google Sheets atau Excel karena masalah otentikasi, koneksi internet terputus, atau file *spreadsheet* sedang dikunci/terbuka.
   * **Mitigasi:** Terapkan blok *Try-Catch* saat mencoba menulis ke *spreadsheet*. Jika gagal, tampilkan *error* yang jelas kepada pengguna dan hasilkan *fallback* berupa file CSV lokal agar data tidak hilang.

7. **Kompilasi Gagal Karena *Missing Dependency***
   * **Risiko:** Kode mahasiswa dianggap gagal kompilasi karena bergantung pada *library* bawaan seperti Greenfoot API, namun tidak dikenali oleh skrip yang berjalan di latar.
   * **Mitigasi:** Saat menjalankan modul kompilasi (`javac`), skrip harus sudah disuplai argumen *classpath* yang merujuk pada *library* pendukung (`greenfoot.jar`, dll) agar kompilasi berjalan dalam *environment* yang sesuai.
