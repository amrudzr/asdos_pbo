# System Architecture & Tech Stack

Dokumen ini menjelaskan pilihan *tech stack*, arsitektur perangkat lunak, serta *library* yang akan digunakan untuk membangun **Sistem Automasi Penilaian Tugas PBO**.

## 1. Pemilihan Teknologi Utama (Tech Stack)
Mengingat aplikasi ini berupa *workflow automation* dan *CLI (Command-Line Interface)*, bahasa pemrograman yang paling ideal adalah **Python (versi 3.10+)**. 
Alasan pemilihan Python:
* Sangat kuat dalam manipulasi teks, *Regular Expression*, dan pengolahan *file system*.
* Memiliki banyak *library* bawaan (*standard library*) untuk CSV, file *ZIP*, dan operasi manipulasi waktu (*datetime*).
* Ekosistem CLI yang sangat kaya untuk membuat tampilan terminal yang interaktif dan rapi.

## 2. Struktur Arsitektur (Modular Design)
Aplikasi akan dibagi menjadi beberapa modul independen (*Separation of Concerns*) agar kode mudah dipelihara dan di-tes.

```text
asdos_pbo/
├── main.py                     # Entry point (CLI runner)
├── requirements.txt            # Daftar dependency
├── src/
│   ├── config.py               # Konstanta, format regex, aturan base score
│   ├── extractor.py            # Modul unzip .gfar dan .zip
│   ├── parser.py               # Parsing NIM dari nama file & parsing waktu
│   ├── compiler.py             # Modul untuk mengecek kompilasi file .java
│   ├── grader.py               # Logika kalkulasi Base Score & Late Penalty
│   ├── plagiarism.py           # Mesin pendeteksi kemiripan kode antar mahasiswa
│   └── reporter.py             # Export ke CSV, Spreadsheet, dan print tabel konsol
└── tests/                      # Unit test untuk setiap modul
```

## 3. Libraries dan Tools
Berikut adalah daftar *library* yang akan digunakan (baik bawaan maupun eksternal):

### A. Core / Standard Library (Built-in Python)
* `zipfile`: Untuk mengekstrak `.gfar` dan `.zip`. (Catatan: file `.gfar` dari Greenfoot pada dasarnya adalah format *zip archive*).
* `re`: Modul *Regular Expression* untuk mengekstrak identitas/NIM mahasiswa dari nama *folder* atau *file*, serta untuk *parsing* pola string.
* `csv`: Untuk pembuatan laporan *output* ke dalam bentuk tabel CSV.
* `datetime` & `time`: Untuk memproses logika denda, menghitung selisih minggu antara waktu *deadline* dan pengumpulan.
* `difflib`: Untuk melakukan komparasi teks (*SequenceMatcher*) jika menggunakan pendekatan deteksi kemiripan teks biasa.

### B. Eksternal Libraries (Third-party)
* **`rich`**: *Library* eksternal untuk membuat antarmuka CLI (teks di terminal) menjadi jauh lebih cantik, berwarna, dan interaktif. *Rich* akan menangani:
  * Tabel konsol untuk pratinjau nilai (Reporting).
  * *Prompt* input dari *user*.
  * Progress bar saat proses ekstraksi dan *scanning* massal.
  * *Error tracking* di log.
* **`javalang`** (Opsional/Direkomendasikan): *Library* *parser* bahasa Java murni di Python. Sangat berguna untuk membaca *source code* `.java` milik mahasiswa menjadi susunan AST (*Abstract Syntax Tree*). Dengan begini, deteksi plagiarisme bisa lebih akurat karena sistem tidak mempedulikan perbedaan spasi, baris baru, ataupun komentar kode, melainkan struktur logika kode itu sendiri.
* **`openpyxl` / `gspread`**: *Library* untuk membaca dan menulis data langsung ke file Microsoft Excel atau Google Sheets secara otomatis (Spreadsheet Integration).

## 4. Alur Data (Data Flow)
1. **Input (Prompt):** Sistem meminta *Asdos* memasukkan *Deadline Tugas* melalui terminal.
2. **Read & Extract:** Sistem membaca folder induk yang berisi ratusan file `.zip` / `.gfar`. Menggunakan modul `extractor`, file tersebut diurai ke folder `/temp`.
3. **Parsing:** Modul `parser` mengambil NIM dari tiap folder tugas dan membaca *timestamp* pengumpulan.
4. **Compilation:** Modul `compiler` mencoba melakukan kompilasi (`javac`) untuk memverifikasi tidak ada *syntax error*.
5. **Validation:** `plagiarism.py` membandingkan semua file `.java` (kecuali *exclude list*) milik setiap mahasiswa dengan satu sama lain.
6. **Scoring:** Modul `grader` mengkalkulasi Base Score (90/80/69/0-50 jika gagal kompilasi) dan memotong *late penalty*.
7. **Reporting:** Data akhir dikompilasi oleh `reporter`, ditampilkan dalam tabel warna-warni menggunakan *rich*, diekspor langsung ke *Spreadsheet* (Excel/GSheets), dan file laporan `report_nilai.csv` sebagai cadangan.
8. **Cleanup:** Sistem menghapus kembali folder `/temp` agar bersih (opsional).
