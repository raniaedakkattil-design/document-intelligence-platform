from pathlib import Path
import time

from google import genai

from app.core.config import settings

from app.schemas.extraction import (
    BalanceSheetExtraction,
    CashFlowExtraction,
    InvoiceExtraction,
    ProfitLossExtraction,
)


client = genai.Client(api_key=settings.GEMINI_API_KEY)


MAX_RETRIES = 3
RETRY_DELAYS = [2, 4, 8]


def _is_retryable_error(exc: Exception) -> bool:
    """Return True for temporary Gemini rate-limit or availability errors."""

    error_text = str(exc).lower()

    retryable_codes = ["429", "503", "unavailable", "resource exhausted"]

    return any(code in error_text for code in retryable_codes)


def _generate_content_with_retry(*args, **kwargs):
    """Call Gemini with retry handling for temporary errors."""

    for attempt in range(MAX_RETRIES + 1):
        try:
            return client.models.generate_content(*args, **kwargs)

        except Exception as exc:
            if not _is_retryable_error(exc) or attempt == MAX_RETRIES:
                raise

            delay = RETRY_DELAYS[attempt]
            time.sleep(delay)


def ask_gemini(prompt: str) -> str:
    response = _generate_content_with_retry(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    return response.text


def extract_from_pdf(
    file_path: str,
    prompt: str,
    document_type: str,
) -> str:
    pdf_path = Path(file_path)

    uploaded_file = client.files.upload(file=pdf_path)

    schemas = {
        "invoice": InvoiceExtraction,
        "balance sheet": BalanceSheetExtraction,
        "profit and loss": ProfitLossExtraction,
        "cash flow": CashFlowExtraction,
    }

    schema = schemas.get(document_type.lower())

    if schema is None:
        raise ValueError(f"Unsupported document type: {document_type}")

    response = _generate_content_with_retry(
        model=settings.GEMINI_MODEL,
        contents=[
            uploaded_file,
            prompt,
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
        },
    )

    return response.text