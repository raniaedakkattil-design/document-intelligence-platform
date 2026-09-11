from pathlib import Path
from typing import BinaryIO

import fitz  # PyMuPDF


SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_PAGES = 3


class DocumentValidationError(Exception):
    """Raised when an uploaded document fails validation."""


def validate_document(
    file: BinaryIO,
    filename: str,
    content_type: str | None = None,
) -> dict:
    """
    Validate an uploaded PDF/JPG/PNG before extraction.

    Returns a structured validation result.
    Raises DocumentValidationError for invalid files.
    """

    extension = Path(filename).suffix.lower()

    # ---------------------------------------------------------
    # 1. File extension validation
    # ---------------------------------------------------------
    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentValidationError(
            "UNSUPPORTED_FILE_TYPE: Only PDF / JPG / PNG documents are supported."
        )

    # ---------------------------------------------------------
    # 2. Read uploaded bytes
    # ---------------------------------------------------------
    file.seek(0)
    file_bytes = file.read()

    if not file_bytes:
        raise DocumentValidationError(
            "EMPTY_FILE: The uploaded file is empty."
        )

    # ---------------------------------------------------------
    # 3. PDF validation
    # ---------------------------------------------------------
    if extension == ".pdf":
        try:
            pdf = fitz.open(stream=file_bytes, filetype="pdf")

            if pdf.page_count == 0:
                pdf.close()
                raise DocumentValidationError(
                    "INVALID_DOCUMENT: PDF contains no pages."
                )

            if pdf.page_count > MAX_PAGES:
                page_count = pdf.page_count
                pdf.close()

                raise DocumentValidationError(
                    f"PAGE_LIMIT_EXCEEDED: PDF contains {page_count} pages. "
                    f"Maximum allowed is {MAX_PAGES}."
                )

            # Try accessing every page to detect malformed PDFs.
            for page_number in range(pdf.page_count):
                pdf.load_page(page_number)

            page_count = pdf.page_count
            pdf.close()

        except DocumentValidationError:
            raise

        except Exception as exc:
            raise DocumentValidationError(
                f"CORRUPTED_FILE: Unable to read PDF document."
            ) from exc

        return {
            "file_type": content_type or "application/pdf",
            "is_supported": True,
            "is_readable": True,
            "page_count": page_count,
            "status": "PASS",
        }

    # ---------------------------------------------------------
    # 4. Image validation
    # ---------------------------------------------------------
    try:
        from PIL import Image

        image = Image.open(__import__("io").BytesIO(file_bytes))

        # Force Pillow to actually read the image.
        image.verify()

    except Exception as exc:
        raise DocumentValidationError(
            "CORRUPTED_FILE: Unable to read image document."
        ) from exc

    return {
        "file_type": content_type or "image/*",
        "is_supported": True,
        "is_readable": True,
        "page_count": 1,
        "status": "PASS",
    }