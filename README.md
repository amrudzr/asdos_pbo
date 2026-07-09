# ASDOS PBO - Sistem Otomatisasi Penilaian & Deteksi Plagiasi 🚀

Proyek ini adalah sistem otomatisasi penilaian dan pendeteksi plagiasi yang dirancang khusus untuk Asisten Dosen (Asdos) pada mata kuliah PBO (Pemrograman Berorientasi Objek). Sistem ini difokuskan pada penilaian tugas mahasiswa yang menggunakan framework **Greenfoot** (serta file `.zip` atau `.gfar`), melakukan validasi aset otomatis, mengekstrak file Java, dan mendeteksi tingkat kemiripan antar source code (plagiarisme).

## ✨ Fitur Utama

- **Ekstraksi Otomatis**: Mendukung dan dapat membongkar format file `.zip`, `.greenfoot`, dan `.gfar` (Greenfoot Archive) secara otomatis.
- **Validasi Aset Greenfoot Otomatis**: Melakukan pengecekan ketersediaan aset gambar (`images/`) dan suara (`sounds/`) yang wajib ada pada proyek game/aplikasi mahasiswa.
- **Deteksi Plagiasi Struktur (AST) Global**: Menggunakan `javalang` untuk menganalisis Abstract Syntax Tree (AST) secara otomatis (batch) terhadap seluruh tugas mahasiswa. Sistem dapat mendeteksi plagiarisme struktural dan menyoroti (*highlight*) bagian kode yang mirip, sambil memisahkan mana yang sekadar template dasar dosen (boilerplate).
- **Deteksi Komentar & Improvisasi Otomatis**: Secara cerdas menganalisis *source code* mahasiswa untuk mengecek ada tidaknya dokumentasi/komentar penjelasan yang menjadi poin tambahan.
- **Tabel Pelaporan Interaktif (Rich)**: Menampilkan antarmuka laporan penilaian dan rekap detail plagiasi secara visual menggunakan tabel di dalam CLI/Terminal.
- **Integrasi Langsung ke Excel Master**: Menghasilkan output nilai akhir yang bisa langsung diinput ke dalam *Sheet* khusus pada file Excel rekapitulasi penilaian utama, dikonfigurasi secara fleksibel melalui file `.env`. (Ekspor `.csv` standar tetap tersedia).

## 📋 Prasyarat Sistem

- **Python 3.8** atau versi yang lebih baru terinstal di perangkat Anda.
- **Git** (Opsional, untuk melakukan clone repository ini).

## 🛠 Panduan Instalasi

Disarankan untuk menggunakan *Virtual Environment* agar dependensi atau library sistem ini tidak bentrok dengan _environment_ global Python Anda.

1. **Clone repositori ini atau arahkan terminal ke folder proyek**:
   ```bash
   cd c:\projects\multi-platform\asdos_pbo
   ```

2. **Buat Virtual Environment (opsional namun sangat disarankan)**:
   ```bash
   # Di Windows
   python -m venv venv
   
   # Di macOS / Linux
   python3 -m venv venv
   ```

3. **Aktifkan Virtual Environment**:
   ```bash
   # Di Windows (Command Prompt)
   venv\Scripts\activate.bat
   
   # Di Windows (PowerShell)
   venv\Scripts\Activate.ps1
   
   # Di macOS / Linux
   source venv/bin/activate
   ```

4. **Instal seluruh Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```
   *Library utama yang akan diinstal meliputi `rich` (untuk UI CLI), `javalang` (untuk AST parser), dan `openpyxl` (untuk integrasi Excel).*

5. **Konfigurasi Path Excel (Opsional, jika butuh auto-input nilai)**:
   - Duplikat file `.env.example` dan ubah namanya menjadi `.env`.
   - Buka file `.env` tersebut dan ubah nilai `EXCEL_PATH` sesuai dengan lokasi file Excel tempat Anda merekap nilai (misalnya: `C:\Users\Nama\Documents\tugas.xlsx`).

## 🚀 Cara Penggunaan

1. **Siapkan Data Mahasiswa**: 
   Pastikan folder/direktori kumpulan tugas submission mahasiswa siap. (Anda bisa menyesuaikan lokasi atau path membaca data mahasiswa di dalam parameter `main.py`).

2. **Jalankan Skrip Utama**:
   Jalankan file `main.py` menggunakan Python untuk memulai proses _grading_ (penilaian).
   ```bash
   python main.py
   ```

3. **Ikuti Instruksi pada Layar**:
   Sistem akan secara otomatis mulai mengekstrak tugas satu persatu.
   Saat selesai, ia akan memunculkan "Laporan Detail Plagiarisme" dan "Laporan Hasil Penilaian Tugas PBO".
   
4. **Ekspor Hasil**:
   Pada langkah terakhir eksekusi, Anda akan ditanya apakah ingin mengekspor data tersebut ke dalam file CSV (tekan `y`). Selanjutnya, sistem juga akan menanyakan apakah Anda ingin mengupdate **file Excel Master** secara otomatis. Jika iya, Anda hanya perlu mengetikkan nama kolom tugas (misal: `nama tugas 1`), dan sistem akan mengisi nilai akhir secara presisi berdasarkan NIM mahasiswa.

## 📚 Pelajari Lebih Lanjut
Apabila Anda butuh memodifikasi _scoring logic_ atau aturan penilaian (seperti bobot skor `95` untuk penambahan komentar improvisasi atau `78` untuk format yang salah), Anda dapat memeriksa atau memodifikasi `main.py` dan `src/plagiarism.py`. Anda juga bisa membaca file [TUTORIAL.md](./TUTORIAL.md) untuk mempelajari struktur detail jika tersedia panduan ekstraksi.

---
*Dikelola dengan ❤️ untuk kelancaran tugas Asdos PBO.*
