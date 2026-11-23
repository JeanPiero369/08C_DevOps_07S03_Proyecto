"""Pruebas de los límites de PDF (D-01): tamaño, páginas y archivos inválidos."""
import asyncio
import io

import pytest
from pypdf import PdfWriter

from core.pdf.pdf_extractor import PDFTooLargeError, read_upload_limited, validate_pdf


def make_pdf(pages: int) -> bytes:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=200, height=200)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


class FakeUpload:
    """Imita UploadFile.read(n) por bloques."""

    def __init__(self, data: bytes):
        self._buf = io.BytesIO(data)

    async def read(self, n: int = -1) -> bytes:
        return self._buf.read(n)


def test_pdf_valido_dentro_del_limite():
    assert validate_pdf(make_pdf(3), max_pages=30) == 3


def test_pdf_con_demasiadas_paginas_es_rechazado():
    with pytest.raises(ValueError, match="máximo es 5"):
        validate_pdf(make_pdf(6), max_pages=5)


def test_archivo_que_no_es_pdf_es_rechazado():
    with pytest.raises(ValueError, match="no es un PDF"):
        validate_pdf(b"MZ\x90\x00 ejecutable disfrazado", max_pages=30)


def test_pdf_corrupto_es_rechazado():
    with pytest.raises(ValueError, match="no es un PDF"):
        validate_pdf(b"%PDF-1.7\n basura sin estructura", max_pages=30)


def test_lectura_corta_al_superar_el_tamaño():
    data = b"%PDF-" + b"x" * (2 * 1024 * 1024)
    with pytest.raises(PDFTooLargeError):
        asyncio.run(read_upload_limited(FakeUpload(data), max_bytes=1024 * 1024))


def test_lectura_dentro_del_tamaño():
    data = make_pdf(1)
    assert asyncio.run(read_upload_limited(FakeUpload(data), max_bytes=1024 * 1024)) == data
