from dataclasses import dataclass
from datetime import datetime


@dataclass
class Kunjungan:
    id: int
    nim: str
    nama: str
    program_studi: str
    tujuan: str
    waktu_kunjungan: datetime