import json
from pathlib import Path
from typing import BinaryIO

from app.services.document_validation_service import validate_document
from app.services.financial_validation_service import (
    validate_balance_sheet,
    validate_cash_flow,
    validate_invoice,
    validate_profit_and_loss,
)
from app.services.gemini_service import extract_from_pdf


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


EXTRACTION_PROMPTS = {
    "invoice": """
You are extracting information from an invoice.

Extract ALL meaningful visible information from the document.

Important rules:
- Do not invent or assume information.
- If information is missing or unclear, return null.
- Extract every visible invoice line item.
- Preserve quantities, prices, totals, tax information and payment information exactly.
- Preserve negative values if present.
- Include page number and source text when possible.
""",

    "balance sheet": """
You are extracting information from a Balance Sheet.

Extract ALL meaningful visible information from the document.

Important rules:
- Do not invent or assume information.
- If information is missing or unclear, return null.
- Extract every visible line item.
- Preserve both reporting periods exactly as shown.
- Preserve negative values correctly.
- Extract totals for Assets and Capital & Liabilities.
- Include page number and source text when possible.
""",

    "profit and loss": """
You are extracting information from a Profit and Loss Statement.

Extract ALL meaningful visible information from the document.

Important rules:
- Do not invent or assume information.
- If information is missing or unclear, return null.
- Extract every visible line item.
- Preserve both reporting periods exactly as shown.
- Preserve negative values correctly.
- Extract interest earned, other income, total income,
  interest expended, operating expenses, provisions,
  total expenditure, profit before minority,
  minority interest and net profit when present.
- Include page number and source text when possible.
""",

    "cash flow": """
You are extracting information from a Cash Flow Statement.

Extract ALL meaningful visible information from the document.

Important rules:
- Do not invent or assume information.
- If information is missing or unclear, return null.
- Extract every visible line item.
- Preserve both reporting periods exactly as shown.
- Preserve negative values correctly.
- Extract operating, investing, financing and foreign exchange
  cash flows, net cash increase, opening cash balance and
  closing cash balance when present.
- Include page number and source text when possible.
""",
}


def normalize_document_type(document_type: str) -> str:
    value = document_type.strip().lower()

    aliases = {
        "invoice": "invoice",
        "balance sheet": "balance sheet",
        "balance_sheet": "balance sheet",
        "profit and loss": "profit and loss",
        "profit & loss": "profit and loss",
        "profit_loss": "profit and loss",
        "cash flow": "cash flow",
        "cash flow statement": "cash flow",
        "cash_flows": "cash flow",
    }

    if value not in aliases:
        raise ValueError(
            f"Unsupported document type: {document_type}"
        )

    return aliases[value]


def run_validation(
    document_type: str,
    extracted: dict,
) -> list[dict]:
    if document_type == "balance sheet":
        return [
            validate_balance_sheet(
                total_assets=extracted.get(
                    "total_assets_period_1"
                ),
                total_capital_and_liabilities=extracted.get(
                    "total_capital_and_liabilities_period_1"
                ),
            ),
            validate_balance_sheet(
                total_assets=extracted.get(
                    "total_assets_period_2"
                ),
                total_capital_and_liabilities=extracted.get(
                    "total_capital_and_liabilities_period_2"
                ),
            ),
        ]

    if document_type == "profit and loss":
        return validate_profit_and_loss(
            interest_earned=extracted.get(
                "interest_earned_period_1"
            ),
            other_income=extracted.get(
                "other_income_period_1"
            ),
            total_income=extracted.get(
                "total_income_period_1"
            ),
            interest_expended=extracted.get(
                "interest_expended_period_1"
            ),
            operating_expenses=extracted.get(
                "operating_expenses_period_1"
            ),
            provisions=extracted.get(
                "provisions_period_1"
            ),
            total_expenditure=extracted.get(
                "total_expenditure_period_1"
            ),
            profit_before_minority=extracted.get(
                "profit_before_minority_period_1"
            ),
            minority_interest=extracted.get(
                "minority_interest_period_1"
            ),
            net_profit=extracted.get(
                "net_profit_period_1"
            ),
        )

    if document_type == "cash flow":
        return validate_cash_flow(
            operating_cash_flow=extracted.get(
                "operating_cash_flow_period_1"
            ),
            investing_cash_flow=extracted.get(
                "investing_cash_flow_period_1"
            ),
            financing_cash_flow=extracted.get(
                "financing_cash_flow_period_1"
            ),
            foreign_exchange_effect=extracted.get(
                "foreign_exchange_effect_period_1"
            ),
            net_cash_increase=extracted.get(
                "net_cash_increase_period_1"
            ),
            opening_cash_balance=extracted.get(
                "opening_cash_balance_period_1"
            ),
            closing_cash_balance=extracted.get(
                "closing_cash_balance_period_1"
            ),
        )

    if document_type == "invoice":
        items = extracted.get("invoice_items", [])

        return validate_invoice(
            invoice_items=items,
            subtotal=extracted.get("subtotal"),
            tax_amount=extracted.get("tax_amount"),
            total_amount=extracted.get("total_amount"),
            cash_paid=extracted.get("cash_paid"),
            change_amount=extracted.get("change_amount"),
        )

    return []


def process_document(
    file: BinaryIO,
    filename: str,
    content_type: str | None,
    document_type: str,
) -> dict:
    """
    Complete document processing pipeline:

    1. Validate file
    2. Save temporary upload
    3. Extract structured information with Gemini
    4. Run financial validation
    5. Return final result
    """

    normalized_type = normalize_document_type(document_type)

    # Read the uploaded file once.
    file.seek(0)
    file_bytes = file.read()

    # Validate the document.
    from io import BytesIO

    validation = validate_document(
        file=BytesIO(file_bytes),
        filename=filename,
        content_type=content_type,
    )

    # Save the uploaded file temporarily.
    saved_path = UPLOAD_DIR / filename
    saved_path.write_bytes(file_bytes)

    try:
        prompt = EXTRACTION_PROMPTS[normalized_type]

        extracted_text = extract_from_pdf(
            file_path=str(saved_path),
            prompt=prompt,
            document_type=normalized_type,
        )

        extracted = json.loads(extracted_text)

        validation_results = run_validation(
            document_type=normalized_type,
            extracted=extracted,
        )

        return {
            "document_name": filename,
            "document_type": extracted.get(
                "document_type",
                document_type,
            ),
            "processing_status": "PASS",
            "file_validation": validation,
            "extraction": extracted,
            "financial_validation": validation_results,
        }

    finally:
        # We don't need to keep uploaded files locally.
        if saved_path.exists():
            saved_path.unlink()