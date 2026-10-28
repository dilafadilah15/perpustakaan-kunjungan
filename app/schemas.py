from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Pilihan tujuan yang boleh dikirim melalui API.
TujuanKunjungan = Literal[
    "Membaca",
    "Belajar",
    "Mencari Referensi",
    "Lainnya",
]


class KunjunganInput(BaseModel):
    """Data yang dikirim saat menambah atau mengubah kunjungan."""

    # Menghapus spasi di awal dan akhir isian teks.
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    nim: str = Field(min_length=1, pattern=r"^[0-9]+$")
    nama: str = Field(min_length=1)
    program_studi: str = Field(min_length=1)
    tujuan: TujuanKunjungan


class KunjunganResponse(BaseModel):
    """Data kunjungan yang dikembalikan oleh API."""

    # Memungkinkan pembacaan data dari objek Kunjungan di models.py.
    model_config = ConfigDict(from_attributes=True)

    id: int
    nim: str
    nama: str
    program_studi: str
    tujuan: TujuanKunjungan
    waktu_kunjungan: datetime