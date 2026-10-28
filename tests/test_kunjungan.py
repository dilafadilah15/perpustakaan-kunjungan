import unittest
from datetime import datetime, timedelta

from app.repositories import MemoryKunjunganRepository
from app.services import KunjunganService


class TestKunjunganService(unittest.TestCase):
    def setUp(self):
        # Dijalankan sebelum setiap test.
        # Penyimpanan baru memastikan test saling terpisah.
        self.repository = MemoryKunjunganRepository()
        self.service = KunjunganService(self.repository)

        self.data = {
            "nim": "60200123001",
            "nama": "Ahmad",
            "program_studi": "Sistem Informasi",
            "tujuan": "Membaca",
        }

    def test_tambah_kunjungan(self):
        sebelum = datetime.now()
        hasil = self.service.tambah_kunjungan(**self.data)
        sesudah = datetime.now()

        self.assertEqual(hasil.id, 1)
        self.assertEqual(hasil.nim, self.data["nim"])
        self.assertEqual(hasil.nama, "Ahmad")

        # Waktu otomatis berada dalam rentang proses penambahan.
        self.assertLessEqual(sebelum, hasil.waktu_kunjungan)
        self.assertLessEqual(hasil.waktu_kunjungan, sesudah)

        tersimpan = self.service.ambil_kunjungan(hasil.id)
        self.assertEqual(tersimpan, hasil)

    def test_kunjungan_berulang_memiliki_id_berbeda(self):
        # Mahasiswa yang sama boleh datang lebih dari sekali.
        pertama = self.service.tambah_kunjungan(**self.data)
        kedua = self.service.tambah_kunjungan(**self.data)

        self.assertNotEqual(pertama.id, kedua.id)
        self.assertEqual(len(self.service.lihat_kunjungan()), 2)

    def test_isian_kosong_ditolak(self):
        # Coba setiap isian wajib dengan teks berisi spasi saja.
        for kolom in self.data:
            with self.subTest(kolom=kolom):
                data_salah = {**self.data, kolom: "   "}

                with self.assertRaises(ValueError):
                    self.service.tambah_kunjungan(**data_salah)

        self.assertEqual(self.service.lihat_kunjungan(), [])

    def test_nim_huruf_ditolak(self):
        self.data["nim"] = "ABC123"

        with self.assertRaises(ValueError):
            self.service.tambah_kunjungan(**self.data)

        self.assertEqual(self.service.lihat_kunjungan(), [])

    def test_tujuan_tidak_valid_ditolak(self):
        self.data["tujuan"] = "Bermain"

        with self.assertRaises(ValueError):
            self.service.tambah_kunjungan(**self.data)

    def test_cari_nama_dan_nim(self):
        kunjungan = self.service.tambah_kunjungan(**self.data)

        # Pencarian nama tidak membedakan huruf besar dan kecil.
        self.assertEqual(
            self.service.lihat_kunjungan(kata_kunci="AHMAD"),
            [kunjungan],
        )

        self.assertEqual(
            self.service.lihat_kunjungan(kata_kunci=self.data["nim"]),
            [kunjungan],
        )

        self.assertEqual(
            self.service.lihat_kunjungan(kata_kunci="Budi"),
            [],
        )

    def test_filter_tanggal(self):
        kunjungan = self.service.tambah_kunjungan(**self.data)
        tanggal = kunjungan.waktu_kunjungan.date()

        self.assertEqual(
            self.service.lihat_kunjungan(tanggal=tanggal),
            [kunjungan],
        )

        self.assertEqual(
            self.service.lihat_kunjungan(
                tanggal=tanggal - timedelta(days=1)
            ),
            [],
        )

    def test_ubah_menjaga_id_dan_waktu(self):
        awal = self.service.tambah_kunjungan(**self.data)
        data_baru = {**self.data, "tujuan": "Belajar"}

        hasil = self.service.ubah_kunjungan(awal.id, **data_baru)

        self.assertEqual(hasil.tujuan, "Belajar")
        self.assertEqual(hasil.id, awal.id)
        self.assertEqual(hasil.waktu_kunjungan, awal.waktu_kunjungan)
        self.assertEqual(
            self.service.ambil_kunjungan(awal.id).tujuan,
            "Belajar",
        )

    def test_ubah_tidak_valid_menjaga_data_lama(self):
        awal = self.service.tambah_kunjungan(**self.data)
        data_salah = {**self.data, "nama": ""}

        with self.assertRaises(ValueError):
            self.service.ubah_kunjungan(awal.id, **data_salah)

        tersimpan = self.service.ambil_kunjungan(awal.id)
        self.assertEqual(tersimpan.nama, "Ahmad")
        self.assertEqual(tersimpan.tujuan, "Membaca")

    def test_hapus_kunjungan(self):
        kunjungan = self.service.tambah_kunjungan(**self.data)
        self.service.hapus_kunjungan(kunjungan.id)

        self.assertEqual(self.service.lihat_kunjungan(), [])

        with self.assertRaises(LookupError):
            self.service.ambil_kunjungan(kunjungan.id)

    def test_operasi_pada_id_tidak_ada(self):
        with self.assertRaises(LookupError):
            self.service.ambil_kunjungan(999)

        with self.assertRaises(LookupError):
            self.service.ubah_kunjungan(999, **self.data)

        with self.assertRaises(LookupError):
            self.service.hapus_kunjungan(999)


if __name__ == "__main__":
    unittest.main()