from pathlib import Path

from google import genai

from app.core.config import settings

from app.schemas.extraction import (
    BalanceSheetExtraction,
    CashFlowExtraction,
    InvoiceExtraction,
    ProfitLossExtraction,
)


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
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

    response = client.models.generate_content(
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