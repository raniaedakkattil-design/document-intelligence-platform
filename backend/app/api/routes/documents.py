import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import Document
from app.services.document_service import process_document
from app.services.document_validation_service import DocumentValidationError


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


@router.post("/process")
async def process_uploaded_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    db: Session = Depends(get_db),
):
    filename = file.filename or "uploaded_document"

    try:
        result = process_document(
            file=file.file,
            filename=filename,
            content_type=file.content_type,
            document_type=document_type,
        )

        document = Document(
            document_name=filename,
            document_type=result["document_type"],
            processing_status=result["processing_status"],
            result_json=json.dumps(result),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return result

    except DocumentValidationError as exc:
        failed_result = {
            "document_name": filename,
            "document_type": document_type,
            "processing_status": "FAILED",
            "error": str(exc),
        }

        document = Document(
            document_name=filename,
            document_type=document_type,
            processing_status="FAILED",
            result_json=json.dumps(failed_result),
        )

        db.add(document)
        db.commit()

        raise HTTPException(
            status_code=400,
            detail=failed_result,
        )

    except ValueError as exc:
        failed_result = {
            "document_name": filename,
            "document_type": document_type,
            "processing_status": "FAILED",
            "error": str(exc),
        }

        document = Document(
            document_name=filename,
            document_type=document_type,
            processing_status="FAILED",
            result_json=json.dumps(failed_result),
        )

        db.add(document)
        db.commit()

        raise HTTPException(
            status_code=400,
            detail=failed_result,
        )

    except Exception as exc:
        failed_result = {
            "document_name": filename,
            "document_type": document_type,
            "processing_status": "FAILED",
            "error": f"PROCESSING_ERROR: {str(exc)}",
        }

        document = Document(
            document_name=filename,
            document_type=document_type,
            processing_status="FAILED",
            result_json=json.dumps(failed_result),
        )

        db.add(document)
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=failed_result,
        )


@router.get("")
def list_documents(
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .order_by(Document.processed_at.desc())
        .all()
    )

    return [
        {
            "id": document.id,
            "document_name": document.document_name,
            "document_type": document.document_type,
            "processing_status": document.processing_status,
            "processed_at": document.processed_at,
        }
        for document in documents
    ]


@router.get("/{document_name}")
def get_document(
    document_name: str,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.document_name == document_name)
        .order_by(Document.processed_at.desc())
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="DOCUMENT_NOT_FOUND",
        )

    return json.loads(document.result_json)