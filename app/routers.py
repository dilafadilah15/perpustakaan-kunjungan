from datetime import date

from fastapi import APIRouter, Response, status

from app.repositories import MemoryKunjunganRepository
from app.schemas import KunjunganInput, KunjunganResponse
from app.services import KunjunganService


router = APIRouter(
    prefix="/api/v1/kunjungan",
    tags=["Kunjungan"],
)

# Satu penyimpanan dan service dipakai bersama oleh endpoint.
repository = MemoryKunjunganRepository()
service = KunjunganService(repository)


@router.post(
    "",
    response_model=KunjunganResponse,
    status_code=status.HTTP_201_CREATED,
)
def tambah_kunjungan(payload: KunjunganInput):
    """Mencatat kunjungan baru."""

    # Mengubah input Pydantic menjadi dictionary,
    # lalu meneruskannya sebagai argumen fungsi.
    return service.tambah_kunjungan(**payload.model_dump())


@router.get("", response_model=list[KunjunganResponse])
def lihat_kunjungan(
    kata_kunci: str = "",
    tanggal: date | None = None,
):
    """Melihat daftar kunjungan, dengan pencarian dan filter opsional."""

    return service.lihat_kunjungan(
        kata_kunci=kata_kunci,
        tanggal=tanggal,
    )


@router.get("/{id_kunjungan}", response_model=KunjunganResponse)
def ambil_kunjungan(id_kunjungan: int):
    """Melihat satu catatan berdasarkan ID."""

    return service.ambil_kunjungan(id_kunjungan)


@router.put("/{id_kunjungan}", response_model=KunjunganResponse)
def ubah_kunjungan(
    id_kunjungan: int,
    payload: KunjunganInput,
):
    """Mengubah data kunjungan dengan mengirim keempat isian lengkap."""

    return service.ubah_kunjungan(
        id_kunjungan=id_kunjungan,
        **payload.model_dump(),
    )


@router.delete(
    "/{id_kunjungan}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def hapus_kunjungan(id_kunjungan: int):
    """Menghapus catatan berdasarkan ID."""

    service.hapus_kunjungan(id_kunjungan)

    # Penghapusan berhasil tanpa mengembalikan isi respons.
    return Response(status_code=status.HTTP_204_NO_CONTENT)