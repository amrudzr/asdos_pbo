# Tutorial Penggunaan Sistem Automasi Penilaian Tugas PBO

Aplikasi ini dirancang khusus untuk Asisten Dosen (Asdos) agar dapat dengan mudah dan otomatis menilai tugas mahasiswa pada mata kuliah Pemrograman Berorientasi Objek (PBO). Dengan sistem ini, kamu bisa menghitung denda keterlambatan, mencatat status program (*compile*), mengecek plagiarisme, hingga mengekspor laporan nilai akhir dengan cepat.

---

## Daftar Isi
1. [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
2. [Langkah-Langkah Penggunaan](#langkah-langkah-penggunaan)
   - [Tahap 1: Pengaturan Deadline](#tahap-1-pengaturan-deadline)
   - [Tahap 2: Memasukkan Data Mahasiswa](#tahap-2-memasukkan-data-mahasiswa)
   - [Tahap 3: Konfirmasi Penilaian](#tahap-3-konfirmasi-penilaian)
3. [Cara Menyimpan Laporan (Ekspor)](#cara-menyimpan-laporan-ekspor)
4. [Pertanyaan yang Sering Muncul (FAQ)](#pertanyaan-yang-sering-muncul-faq)
5. [Kontak Bantuan](#kontak-bantuan)

---

## Cara Menjalankan Aplikasi

Aplikasi ini berjalan melalui layar *console* atau *terminal* di komputer kamu.
1. Buka folder tempat aplikasi ini disimpan (misalnya `asdos_pbo`).
2. Buka aplikasi **Terminal** (Mac/Linux) atau **Command Prompt / PowerShell** (Windows).
3. Ketikkan perintah berikut lalu tekan **Enter**:
   ```bash
   python main.py
   ```
4. Jika berhasil, kamu akan melihat tulisan **"Sistem Automasi Penilaian Tugas PBO Siap!"** di layar.

---

## Langkah-Langkah Penggunaan

Setelah aplikasi berjalan, sistem akan memandumu tahap demi tahap. Ikuti panduan berikut:

### Tahap 1: Pengaturan Deadline
Sistem pertama kali akan menanyakan kapan batas waktu (deadline) pengumpulan tugas.
1. Masukkan waktu *deadline* dengan format bahasa Inggris, contohnya: **Monday, 20 April 2026, 7:43 PM**
2. Tekan **Enter**. Jika formatnya salah, sistem akan memberitahu dan memintamu mengulangi input.

### Tahap 2: Ekstraksi Otomatis File Tugas (.zip / .gfar)
Sistem akan meminta folder tempat kamu menyimpan seluruh arsip tugas mahasiswa (bisa berupa `.zip` maupun `.gfar` - format arsip khusus aplikasi Greenfoot).
1. Ketikkan nama folder tempat tugas disimpan (contoh: `raw_submissions`).
2. Sistem akan secara otomatis membongkar seluruh isi file mahasiswa tersebut ke dalam folder sementara (temp) dan membaca **NIM mahasiswa dari nama file**. 
*(Tips: Kosongkan dan langsung tekan Enter jika kamu ingin mengecek NIM dan tugas secara manual satu-per-satu).*

### Tahap 3: Penilaian dan Pengumpulan Waktu Kumpul
Sistem sekarang akan memandumu menilai secara otomatis (batch) per NIM yang berhasil diekstrak:
1. **Waktu Pengumpulan**: Masukkan waktu kapan mahasiswa tersebut mengumpulkan tugas, dengan format yang sama seperti saat memasukkan deadline.
2. *Jika kamu ingin melewati mahasiswa tertentu atau berhenti menilai, ketik huruf `q` dan tekan Enter.*

### Tahap 4: Konfirmasi Penilaian
Berdasarkan waktu kumpul, sistem akan otomatis menghitung keterlambatan. Jika terlambat, nilai akan dikurangi 1 poin per minggu.
1. **Peringatan Keterlambatan**: 
   *Contoh: Jika mahasiswa telat lebih dari 4 minggu, sistem akan memunculkan peringatan berwarna kuning. Ketik `y` jika kamu ingin lanjut menilai, atau `n` untuk membatalkan input anak tersebut.*
2. **Status Compile**: Sistem akan secara otomatis menguji coba file program (auto-compile) menggunakan Java (`javac`).
   - Kamu akan diminta memasukkan lokasi (path) folder tugas mahasiswa tersebut (secara default akan merujuk ke folder `submissions/[NIM]`).
   - Sistem akan mengecek semua file `.java` di dalam folder tersebut dan melakukan kompilasi. Jika gagal atau *error*, otomatis nilainya menjadi 0.
3. **Plagiarisme**: Jika program berhasil di-compile, sistem akan bertanya lagi, "Apakah terdeteksi plagiat (kemiripan > 80%)?".
   - Ketik `y` jika anak tersebut mencontek. (Otomatis nilai tertingginya dibatasi menjadi 69).
   - Ketik `n` jika karya orisinil.

Setelah semua pertanyaan dijawab, layar akan menampilkan teks **"Data ditambahkan!"** berwarna hijau, dan kamu bisa lanjut ke mahasiswa berikutnya.

---

## Cara Menyimpan Laporan (Ekspor)

Jika kamu sudah selesai memasukkan nilai seluruh mahasiswa (dengan mengetik `q` pada isian NIM), sistem akan menampilkan **Hasil Rekapitulasi** dalam bentuk tabel yang rapi di layar.

1. Setelah tabel muncul, sistem akan bertanya: "Apakah Anda ingin mengekspor data ke CSV?"
2. Ketik `y` lalu tekan **Enter** untuk menyimpan.
3. File akan tersimpan dengan nama **report_nilai.csv** di dalam folder yang sama dengan aplikasi. 
4. File CSV ini bisa kamu buka dengan mudah menggunakan Microsoft Excel atau Google Sheets.

---

## Pertanyaan yang Sering Muncul (FAQ)

**1. Bagaimana format waktu yang benar saat memasukkan deadline atau waktu kumpul?**
Format yang wajib digunakan adalah: `[Hari], [Tanggal] [Bulan] [Tahun], [Jam]:[Menit] [AM/PM]`.
Contoh yang benar: *Monday, 20 April 2026, 7:43 PM*

**2. Kalau saya salah ketik waktu, apakah sistem akan langsung *error*?**
Tidak. Sistem akan menampilkan tulisan "Error Parsing Waktu" berwarna merah dan memintamu mengetik ulang waktu dengan format yang benar.

**3. Apakah saya bisa mengedit nilai mahasiswa kalau saya salah jawab pertanyaan plagiat/compile?**
Saat ini sistem dirancang untuk mencatat per input. Jika kamu salah, selesaikan dulu laporannya (simpan ke CSV), lalu kamu bisa mengoreksi hasilnya secara manual langsung di dalam file Microsoft Excel.

**4. Berapa nilai yang didapat jika tugas mahasiswa tidak bisa di-compile?**
Sistem akan otomatis memberikan Nilai Dasar 0 jika program gagal dijalankan (*error*).

**5. Kok ada keterangan "REVIEW MANUAL" di tabel hasil saya?**
Itu berarti program berhasil dijalankan dan tidak mencontek, tapi nilai dasarnya diset standar (80). Kamu disarankan melihat kembali kode mahasiswa tersebut secara manual jika ingin memberi nilai lebih tinggi.

**6. Ke mana perginya file sementara sistem?**
Aplikasi ini sangat bersih! Setelah laporan selesai ditampilkan, sistem akan otomatis menghapus folder penyimpanan sementara (`temp`), sehingga komputermu tidak akan penuh oleh sampah file sisa penilaian.

---

## Kontak Bantuan

Jika kamu menemukan kendala saat menjalankan sistem ini, aplikasi tiba-tiba tertutup sendiri, atau butuh bantuan instalasi, silakan hubungi:

[Isi kontak koordinator Asdos PBO / Administrator Sistem di sini]
