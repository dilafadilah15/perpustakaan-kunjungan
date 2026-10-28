from abc import ABC, abstractmethod

from app.models import Kunjungan


class KunjunganRepository(ABC):
    """Kontrak operasi penyimpanan data kunjungan."""

    @abstractmethod
    def simpan(self, kunjungan: Kunjungan) -> None:
        pass

    @abstractmethod
    def ambil_semua(self) -> list[Kunjungan]:
        pass

    @abstractmethod
    def cari_by_id(self, id_kunjungan: int) -> Kunjungan | None:
        pass

    @abstractmethod
    def hapus(self, id_kunjungan: int) -> bool:
        pass


class MemoryKunjunganRepository(KunjunganRepository):
    """Menyimpan data dalam dictionary selama aplikasi berjalan."""

    def __init__(self):
        # Setiap objek repository memiliki tempat penyimpanannya sendiri.
        self._data: dict[int, Kunjungan] = {}

    def simpan(self, kunjungan: Kunjungan) -> None:
        # ID menjadi kunci dictionary.
        # ID baru menambahkan data; ID yang sudah ada memperbarui data.
        self._data[kunjungan.id] = kunjungan

    def ambil_semua(self) -> list[Kunjungan]:
        # Mengubah kumpulan nilai dictionary menjadi list.
        return list(self._data.values())

    def cari_by_id(self, id_kunjungan: int) -> Kunjungan | None:
        # Mengembalikan None jika ID tidak ditemukan.
        return self._data.get(id_kunjungan)

    def hapus(self, id_kunjungan: int) -> bool:
        # Mengembalikan False jika data tidak ada.
        if id_kunjungan not in self._data:
            return False

        del self._data[id_kunjungan]
        return True