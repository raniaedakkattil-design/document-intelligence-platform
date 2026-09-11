import json
import mimetypes
from pathlib import Path

from google import genai

from app.core.config import settings


class ExtractionError(Exception):
    """Raised when AI document extraction fails."""


client = genai.Client(api_key=settings.GEMINI_API_KEY)


EXTRACTION_PROMPT = """
You are a financial document extraction system.

Analyze the uploaded financial document carefully.

The document belongs to this category:

{document_type}

Extract ALL meaningful information visible in the document.

Important rules:

1. Do not invent information.
2. Do not infer values that are not visible.
3. If a value is missing or unreadable, use null.
4. Preserve the actual values from the document.
5. Treat values in parentheses as negative numbers.
6. Extract all visible financial line items.
7. Extract all visible table rows and columns.
8. Extract comparative periods/years when present.
9. Extract headers, dates, parties, currency and other meaningful information.
10. For invoices, extract every visible line item.
11. For financial statements, extract every visible financial line item.
12. Include evidence text and page number whenever possible.

Return ONLY valid JSON.

Use this general structure:

{{
    "document_type": "{document_type}",
    "header_fields": {{}},
    "financial_fields": {{}},
    "fields": {{}},
    "tables": [],
    "evidence": []
}}

For fields whose exact structure is not known beforehand, use clear key-value pairs.

For tables, use structured arrays of objects.

For each important extracted value in evidence, use:

{{
    "field": "field_name",
    "value": "value",
    "source_text": "supporting text from document",
    "page_number": 1
}}

Do not include Markdown.
Do not wrap the JSON in ```json.
Return only the JSON object.
"""


def extract_document(
    file_bytes: bytes,
    filename: str,
    document_type: str,
) -> dict:
    """
    Send a document to Gemini for multimodal structured extraction.
    """

    try:
        mime_type, _ = mimetypes.guess_type(filename)

        if mime_type is None:
            extension = Path(filename).suffix.lower()

            if extension == ".pdf":
                mime_type = "application/pdf"
            elif extension in {".jpg", ".jpeg"}:
                mime_type = "image/jpeg"
            elif extension == ".png":
                mime_type = "image/png"
            else:
                raise ExtractionError(
                    "Unable to determine document MIME type."
                )

        prompt = EXTRACTION_PROMPT.format(
            document_type=document_type
        )

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=[
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": file_bytes,
                    }
                },
                prompt,
            ],
        )

        response_text = response.text.strip()

        # Remove accidental Markdown code fences.
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")
            response_text = response_text.strip()

        try:
            extracted = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise ExtractionError(
                "Gemini returned an invalid JSON response."
            ) from exc

        if not isinstance(extracted, dict):
            raise ExtractionError(
                "Gemini response is not a JSON object."
            )

        return extracted

    except ExtractionError:
        raise

    except Exception as exc:
        raise ExtractionError(
            f"Document extraction failed: {str(exc)}"
        ) from exc