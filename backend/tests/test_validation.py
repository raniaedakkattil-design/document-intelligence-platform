from io import BytesIO

import pytest
from PIL import Image

from app.services.document_validation_service import (
    DocumentValidationError,
    validate_document,
)


def test_unsupported_file():
    fake_file = BytesIO(b"hello")

    with pytest.raises(DocumentValidationError) as exc:
        validate_document(
            fake_file,
            "document.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    assert "UNSUPPORTED_FILE_TYPE" in str(exc.value)


def test_empty_file():
    empty_file = BytesIO(b"")

    with pytest.raises(DocumentValidationError) as exc:
        validate_document(
            empty_file,
            "empty.pdf",
            "application/pdf",
        )

    assert "EMPTY_FILE" in str(exc.value)


def test_valid_image():
    # Create a genuinely valid PNG image in memory.
    image = Image.new("RGB", (100, 100), "white")

    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    result = validate_document(
        image_bytes,
        "test.png",
        "image/png",
    )

    assert result["is_supported"] is True
    assert result["is_readable"] is True
    assert result["page_count"] == 1
    assert result["status"] == "PASS"