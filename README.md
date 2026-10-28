# Sistem Pencatatan Kunjungan Perpustakaan

Backend Python untuk mencatat dan mengelola kunjungan mahasiswa
ke perpustakaan.

## Fitur

1. Mencatat kunjungan dengan ID dan waktu otomatis.
2. Melihat daftar kunjungan dari yang terbaru.
3. Mencari berdasarkan nama atau NIM dan memfilter tanggal.
4. Mengubah catatan tanpa mengubah ID dan waktu kunjungan.
5. Menghapus catatan kunjungan.

## Teknologi

- Python 3.10 atau lebih baru.
- FastAPI untuk membuat API.
- Pydantic untuk validasi data API.
- Uvicorn untuk menjalankan server.
- unittest untuk pengujian otomatis.
- Git untuk mencatat riwayat perubahan kode.

## Struktur Proyek

- app/models.py: bentuk objek data kunjungan.
- app/schemas.py: bentuk input dan respons API.
- app/repositories.py: kontrak dan implementasi penyimpanan.
- app/services.py: aturan dan logika kunjungan.
- app/routers.py: endpoint API.
- app/main.py: titik masuk aplikasi dan penanganan error.
- tests/test_kunjungan.py: unit test logika kunjungan.

## Aturan Data

- NIM, nama, program studi, dan tujuan wajib diisi.
- NIM berupa teks yang hanya berisi angka 0–9.
- Tujuan: Membaca, Belajar, Mencari Referensi, atau Lainnya.
- Satu mahasiswa boleh memiliki beberapa catatan kunjungan.
- ID dan waktu dibuat otomatis.
- Perubahan catatan mempertahankan ID dan waktu awal.
- Waktu kunjungan mengikuti waktu lokal komputer server.

## Penyimpanan

Data disimpan sementara dalam dictionary Python.

Data akan hilang ketika proses aplikasi berhenti atau dimuat ulang.
Aplikasi ini ditujukan untuk demonstrasi dengan satu proses server.

## Menyiapkan Lingkungan

Jalankan perintah dari folder utama proyek menggunakan PowerShell.

Buat lingkungan Python jika belum tersedia:

```powershell
python -m venv .venv
```

Aktifkan lingkungan:

```powershell
.\.venv\Scripts\Activate.ps1
```

Pasang pustaka:

```powershell
python -m pip install -r requirements.txt
```

## Menjalankan Aplikasi

```powershell
python -m uvicorn app.main:app --reload
```

Buka dokumentasi interaktif:

http://127.0.0.1:8000/docs

Untuk menghentikan server, tekan Ctrl + C pada terminal.

## Menjalankan Unit Test

```powershell
python -m unittest discover -s tests -v
```

Pengujian memakai penyimpanan terpisah dan tidak membutuhkan server aktif.

## Endpoint

| Metode | Endpoint | Fungsi |
|---|---|---|
| POST | /api/v1/kunjungan | Menambah kunjungan |
| GET | /api/v1/kunjungan | Daftar, pencarian, dan filter tanggal |
| GET | /api/v1/kunjungan/{id_kunjungan} | Detail kunjungan |
| PUT | /api/v1/kunjungan/{id_kunjungan} | Mengubah keempat isian lengkap |
| DELETE | /api/v1/kunjungan/{id_kunjungan} | Menghapus kunjungan |

## Penerapan Desain

Kode dipisahkan berdasarkan tanggung jawabnya untuk mendukung
modularitas dan prinsip Single Responsibility.

KunjunganService menerima kontrak KunjunganRepository dari luar,
sehingga logika kunjungan tidak bergantung langsung pada detail
penyimpanan dictionary. Ini menerapkan Dependency Inversion.

Kontrak repository memungkinkan penambahan implementasi penyimpanan
lain tanpa mengubah logika service, selama perilaku kontraknya dipenuhi.