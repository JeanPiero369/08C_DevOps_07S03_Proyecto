import io
import logging

from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)

PDF_MAGIC = b"%PDF-"
CHUNK_SIZE = 64 * 1024


class PDFTooLargeError(ValueError):
    """El PDF supera el tamaño máximo permitido (se responde 413)."""


async def read_upload_limited(upload, max_bytes: int) -> bytes:
    """Lee un UploadFile por bloques y corta en cuanto supera max_bytes (D-01).

    Evita cargar en memoria archivos arbitrariamente grandes antes de validarlos.
    """
    data = bytearray()
    while True:
        chunk = await upload.read(CHUNK_SIZE)
        if not chunk:
            break
        data.extend(chunk)
        if len(data) > max_bytes:
            raise PDFTooLargeError(f"El PDF supera el tamaño máximo de {max_bytes // (1024 * 1024)} MB.")
    return bytes(data)


def validate_pdf(file_content: bytes, max_pages: int) -> int:
    """Comprueba que sea un PDF legible y con <= max_pages páginas; devuelve el número de páginas.

    Se usa antes de enviar el PDF a Gemini (D-01): evita gastar cuota con archivos
    inválidos o enormes.
    """
    if not file_content.startswith(PDF_MAGIC):
        raise ValueError("El archivo no es un PDF válido.")
    try:
        num_pages = len(PdfReader(io.BytesIO(file_content)).pages)
    except (PdfReadError, ValueError, KeyError, TypeError) as e:
        logger.warning("PDF ilegible: %s", e)
        raise ValueError("El archivo no es un PDF válido.") from e
    if num_pages > max_pages:
        raise ValueError(f"El PDF tiene {num_pages} páginas; el máximo es {max_pages}.")
    return num_pages


class PDFExtractor:
    """
    Clase para extraer texto de archivos PDF (pypdf; antes PyPDF2 3.0.1, CVE-2023-36464).
    """

    @staticmethod
    async def extract_text_from_pdf(file_content: bytes, max_pages: int = 30) -> str:
        """
        Extrae el texto de un archivo PDF proporcionado como bytes.

        Raises:
            ValueError: si el contenido no es un PDF válido o supera max_pages.
        """
        validate_pdf(file_content, max_pages)
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += (page.extract_text() or "") + "\n\n"
        return text
