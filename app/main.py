from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import router


app = FastAPI(
    title="Sistem Pencatatan Kunjungan Perpustakaan",
    description="Backend sederhana untuk mengelola catatan kunjungan.",
    version="1.0.0",
)

# Menghubungkan endpoint kunjungan dengan aplikasi.
app.include_router(router)


@app.get("/")
def beranda():
    """Menampilkan informasi bahwa aplikasi berjalan."""

    return {
        "nama": "Sistem Pencatatan Kunjungan Perpustakaan",
        "status": "berjalan",
    }


@app.exception_handler(ValueError)
async def tangani_input_salah(request: Request, exc: ValueError):
    """Menangani pelanggaran aturan input dari service."""

    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(LookupError)
async def tangani_data_tidak_ditemukan(
    request: Request,
    exc: LookupError,
):
    """Menangani pencarian, perubahan, atau penghapusan data yang tidak ada."""

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )