from dataclasses import replace
from datetime import date, datetime

from app.models import Kunjungan
from app.repositories import KunjunganRepository


class KunjunganService:
    TUJUAN_VALID = (
        "Membaca",
        "Belajar",
        "Mencari Referensi",
        "Lainnya",
    )

    def __init__(self, repository: KunjunganRepository):
        # Penyimpanan diberikan dari luar agar service tidak terikat
        # pada satu jenis penyimpanan tertentu.
        self.repository = repository

        # Melanjutkan nomor ID terbesar jika sudah ada data.
        self._id_berikutnya = max(
            (data.id for data in repository.ambil_semua()),
            default=0,
        ) + 1

    def _validasi_data(
        self,
        nim: str,
        nama: str,
        program_studi: str,
        tujuan: str,
    ) -> tuple[str, str, str, str]:
        # Memastikan semua isian berupa teks.
        for nilai in (nim, nama, program_studi, tujuan):
            if not isinstance(nilai, str):
                raise ValueError("Semua isian harus berupa teks.")

        # Menghapus spasi berlebih di awal dan akhir.
        nim = nim.strip()
        nama = nama.strip()
        program_studi = program_studi.strip()
        tujuan = tujuan.strip()

        if not all((nim, nama, program_studi, tujuan)):
            raise ValueError("Semua isian wajib diisi.")

        if not nim.isascii() or not nim.isdigit():
            raise ValueError("NIM hanya boleh berisi angka 0–9.")

        if tujuan not in self.TUJUAN_VALID:
            raise ValueError("Tujuan kunjungan tidak valid.")

        return nim, nama, program_studi, tujuan

    def tambah_kunjungan(
        self,
        nim: str,
        nama: str,
        program_studi: str,
        tujuan: str,
    ) -> Kunjungan:
        nim, nama, program_studi, tujuan = self._validasi_data(
            nim, nama, program_studi, tujuan
        )

        # ID dan waktu dibuat otomatis oleh sistem.
        kunjungan = Kunjungan(
            id=self._id_berikutnya,
            nim=nim,
            nama=nama,
            program_studi=program_studi,
            tujuan=tujuan,
            waktu_kunjungan=datetime.now(),
        )

        self.repository.simpan(kunjungan)
        self._id_berikutnya += 1

        return kunjungan

    def lihat_kunjungan(
        self,
        kata_kunci: str = "",
        tanggal: date | None = None,
    ) -> list[Kunjungan]:
        data = self.repository.ambil_semua()
        kata_kunci = kata_kunci.strip().lower()

        # Pencarian berdasarkan sebagian nama atau NIM.
        if kata_kunci:
            data = [
                item
                for item in data
                if kata_kunci in item.nama.lower()
                or kata_kunci in item.nim
            ]

        # Filter tanggal dapat digunakan bersama pencarian.
        if tanggal is not None:
            data = [
                item
                for item in data
                if item.waktu_kunjungan.date() == tanggal
            ]

        # Catatan terbaru ditampilkan lebih dahulu.
        return sorted(
            data,
            key=lambda item: (item.waktu_kunjungan, item.id),
            reverse=True,
        )

    def ambil_kunjungan(self, id_kunjungan: int) -> Kunjungan:
        kunjungan = self.repository.cari_by_id(id_kunjungan)

        if kunjungan is None:
            raise LookupError("Data kunjungan tidak ditemukan.")

        return kunjungan

    def ubah_kunjungan(
        self,
        id_kunjungan: int,
        nim: str,
        nama: str,
        program_studi: str,
        tujuan: str,
    ) -> Kunjungan:
        kunjungan_lama = self.ambil_kunjungan(id_kunjungan)

        nim, nama, program_studi, tujuan = self._validasi_data(
            nim, nama, program_studi, tujuan
        )

        # Membuat objek pengganti tanpa mengubah ID dan waktu.
        kunjungan_baru = replace(
            kunjungan_lama,
            nim=nim,
            nama=nama,
            program_studi=program_studi,
            tujuan=tujuan,
        )

        self.repository.simpan(kunjungan_baru)
        return kunjungan_baru

    def hapus_kunjungan(self, id_kunjungan: int) -> None:
        berhasil = self.repository.hapus(id_kunjungan)

        if not berhasil:
            raise LookupError("Data kunjungan tidak ditemukan.")