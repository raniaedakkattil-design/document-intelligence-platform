# Document Intelligence Platform

AI-powered financial document extraction, validation, and REST API platform built for the AI Engineer Internship Case Study.

## Overview
Processes Invoice, Balance Sheet, Profit & Loss, and Cash Flow Statement documents. Users select the document type and upload PDF/JPG/JPEG/PNG files. The platform validates the file, uses Gemini multimodal AI for structured extraction, applies financial reconciliation rules, stores results in PostgreSQL, and displays them through a web dashboard.

## Architecture
```text
Browser → Frontend → FastAPI REST API
                         ├→ Document Validation
                         ├→ Gemini Multimodal Extraction
                         ├→ Pydantic Structured Output
                         └→ Financial Validation
                                   ↓
                              PostgreSQL
                                   ↓
                         History / Result Retrieval
```

## Technology Stack
- Backend: Python, FastAPI
- AI: Google Gemini `gemini-3.6-flash`
- Structured output: Pydantic
- Database: PostgreSQL via Supabase
- ORM: SQLAlchemy
- PDF validation: PyMuPDF
- Image validation: Pillow
- Frontend: HTML, CSS, JavaScript
- API documentation: Swagger / OpenAPI
- Deployment: Render
- Testing: Pytest
- Source control: Git / GitHub

## Processing Flow
1. Select document type and upload a file.
2. Validate file type, readability, and PDF page count.
3. Temporarily store the upload.
4. Extract structured information with Gemini.
5. Enforce predictable JSON using Pydantic schemas.
6. Apply financial reconciliation rules.
7. Store the result in PostgreSQL.
8. Display extraction and validation results.
9. Remove the temporary upload.

## Financial Validation
### Invoice
- Quantity × Unit Price = Line Total
- Sum of Line Totals = Subtotal / displayed total where applicable
- Explicit tax-inclusive handling
- Cash Paid − Total = Change

### Balance Sheet
- Total Assets = Total Capital and Liabilities

### Profit & Loss
- Interest Earned + Other Income = Total Income
- Interest Expended + Operating Expenses + Provisions = Total Expenditure
- Total Income − Total Expenditure = Profit Before Minority
- Profit Before Minority − Minority Interest = Net Profit

### Cash Flow
- Operating + Investing + Financing + Foreign Exchange Effect = Net Cash Increase
- Opening Cash Balance + Net Cash Increase = Closing Cash Balance

Statement validations are performed for both reporting periods when required operands are available. Missing operands produce `NOT_APPLICABLE`.

## Validation Output
Each rule reports the formula, inputs, calculated value, reported value, variance, and status:
- `PASS`
- `FAIL`
- `NOT_APPLICABLE`

Current numeric tolerance: `0.01`.

## REST API
- `POST /api/v1/documents/process` — upload and process a document
- `GET /api/v1/documents/{document_name}` — retrieve latest result
- `GET /api/v1/documents` — processing history
- `GET /api/v1/health` — health check
- `/docs` — Swagger/OpenAPI documentation

## AI / Model Usage
Gemini multimodal AI is used for document understanding and structured extraction. Pydantic schemas are used for the four document types. Prompts instruct the model to extract visible information, avoid invention, return `null` for missing/unclear values, preserve negative values, and capture page/source evidence where possible. Invoice extraction also identifies explicitly tax-inclusive totals.

Temporary Gemini `429` and `503` errors are handled using retry with backoff.

## File Validation
Supported: PDF, JPG, JPEG, PNG.

PDF validation checks readability and a maximum of 3 pages. Images are checked for integrity/readability. Invalid processing results can be stored with `processing_status = FAILED`.

## Testing
Current automated suite: **9 passing tests**.

Run from the project root:
```powershell
$env:PYTHONPATH="backend"
pytest -q
```

Tests cover file validation and financial reconciliation for the four document categories, including PASS/FAIL/NOT_APPLICABLE behavior and tax-inclusive invoice validation.

## Deployment
Live application: https://document-intelligence-platform-3t87.onrender.com

Swagger: https://document-intelligence-platform-3t87.onrender.com/docs

Health: https://document-intelligence-platform-3t87.onrender.com/api/v1/health

GitHub: https://github.com/raniaedakkattil-design/document-intelligence-platform

Secrets are supplied through environment variables and are not committed to the repository.

## Repository Structure
```text
document_intelligence/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   └── tests/
├── frontend/
├── docs/
├── sample_outputs/
├── .env.example
├── .gitignore
├── Dockerfile
├── render.yaml
└── requirements.txt
```

## Limitations
- Extraction quality depends on document quality and layout complexity.
- Gemini API rate limits and availability can affect processing latency.
- Current scope is the four specified financial document categories.
- Authentication and multi-tenant access control are not implemented.
- More extensive integration testing can be added.

## Future Improvements
- More robust page-level evidence/source mapping
- Expanded document and accounting-rule coverage
- More API/integration tests
- Authentication and role-based access
- Batch/background processing
- Improved confidence scoring and human review
- Production monitoring and observability
- Additional AI fallback strategies

## Current Verification Status
Verified:
- 9/9 automated tests passing
- Render deployment
- Live frontend
- Health endpoint
- Swagger/OpenAPI
- PostgreSQL persistence/history
- Live Balance Sheet processing
- Live Profit & Loss processing

Live Cash Flow and Invoice re-testing is pending because Gemini API rate limiting was encountered during repeated live tests.

## AI Assistance
AI tools were used for implementation guidance, debugging, code review, validation logic, documentation, and presentation preparation. The resulting implementation was tested and reviewed during development.
