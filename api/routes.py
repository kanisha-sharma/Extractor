from __future__ import annotations

import os
import shutil
import traceback
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from config import UPLOAD_FOLDER

from database.db import get_db

from database.crud import (
    create_document,
    get_all_documents,
    get_document,
)

from coastalExtractor.pdf_metadata import extract_pdf_metadata

from coastalExtractor.analyzer.document_analyzer import (
    DocumentAnalyzer,
)

from coastalExtractor.intelligence.document_analyzer import (
    DocumentIntelligenceAnalyzer,
)

from coastalExtractor.extraction.extraction_service import (
    ExtractionService
)

from coastalExtractor.extraction.section_formatter import (
    SectionFormatter
)

from schemas.extraction_schema import (
    SectionCatalogResponse,
    SectionExtractionResponse
)

router = APIRouter()


# =====================================================
# Health Check
# =====================================================

@router.get("/health")
def health():

    return {

        "status": "healthy",

        "message": "Backend is running successfully."

    }


# =====================================================
# Upload PDF
# =====================================================

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename received."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    unique_filename = f"{uuid.uuid4()}.pdf"

    save_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    try:

        with open(save_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        metadata = extract_pdf_metadata(
            save_path
        )

        document = create_document(

            db=db,

            filename=file.filename,

            filepath=save_path,

            total_pages=metadata.get(
                "total_pages",
                0
            )

        )

    except Exception as e:

        if os.path.exists(save_path):

            os.remove(save_path)

        raise HTTPException(

            status_code=500,

            detail=f"Upload failed: {str(e)}"

        )

    return {

        "message": "PDF uploaded successfully.",

        "document_id": document.id,

        "original_filename": document.filename,

        "stored_filename": unique_filename,

        "filepath": document.filepath,

        "pages": document.total_pages

    }

# =====================================================
# Get All Documents
# =====================================================

@router.get("/documents")
def list_documents(
    db: Session = Depends(get_db)
):

    documents = get_all_documents(db)

    return {

        "count": len(documents),

        "documents": documents

    }


# =====================================================
# Get Single Document
# =====================================================

@router.get("/documents/{document_id}")
def document_details(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = get_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return document


# =====================================================
# Run Stage 2 Analysis
# =====================================================

@router.post("/documents/{document_id}/stage2")
def analyze_stage2(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = get_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    if not os.path.exists(document.filepath):

        raise HTTPException(
            status_code=404,
            detail="PDF file not found."
        )

    analyzer = None

    try:

        analyzer = DocumentAnalyzer(
            document.filepath
        )

        result = analyzer.analyze()

        return {
            "status": "success",
            "document_id": document.id,
            "filename": document.filename,
            "pages": result["total_pages"],
            "headings": len(result["headings"]),
            "sections": len(result["sections"]),
            "paragraphs": len(result["paragraphs"]),
            "tables": len(result["tables"]),
            "figures": len(result["figures"]),
            "images": len(result["images"]),
            "lists": len(result["lists"])
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if analyzer is not None:

            analyzer.close()


# =====================================================
# Run Stage 3 Intelligence
# =====================================================

@router.post("/documents/{document_id}/stage3")
def analyze_stage3(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = get_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    if not os.path.exists(document.filepath):

        raise HTTPException(
            status_code=404,
            detail="PDF file not found."
        )

    analyzer = None

    try:

        analyzer = DocumentIntelligenceAnalyzer(
            document.filepath
        )

        result = analyzer.analyze()

        return {
            "status": "success",
            "document_id": document.id,
            "filename": document.filename,
            "stage": 3,
            "pages": result.metadata.page_count,
            "document_type": result.classification.document_type,
            "headings": len(result.headings),
            "sections": len(result.sections),
            "tables": len(result.tables),
            "captions": len(result.captions),
            "lists": len(result.lists),
            "entities": len(result.entities),
            "key_values": len(result.key_values),
            "processing_time": round(result.processing_time, 2),
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if analyzer is not None:

            analyzer.close()


# =====================================================
# Run Complete Pipeline
# =====================================================

@router.post("/documents/{document_id}/analyze")
def analyze_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = get_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    if not os.path.exists(document.filepath):

        raise HTTPException(
            status_code=404,
            detail="PDF file not found."
        )

    stage2 = None
    stage3 = None

    stage2_analyzer = None
    stage3_analyzer = None

    try:

        stage2_analyzer = DocumentAnalyzer(
            document.filepath
        )

        stage2 = stage2_analyzer.analyze()

        stage3_analyzer = DocumentIntelligenceAnalyzer(
            document.filepath
        )

        stage3 = stage3_analyzer.analyze()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if stage2_analyzer is not None:
            stage2_analyzer.close()

        if stage3_analyzer is not None:
            stage3_analyzer.close()

    return {

        "document_id": document.id,

        "filename": document.filename,

        "pages": document.total_pages,

    }

# ============================================================
# Stage 4
# Section Catalog
# ============================================================


@router.get(
    "/documents/{document_id}/sections"
)
def get_document_sections(
    document_id: int,
    db: Session = Depends(get_db)
):

    """
    Returns detected sections
    for user selection.
    """


    document = get_document(
        db,
        document_id
    )


    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    service = ExtractionService(
        document.filepath
    )


    try:

        sections = service.get_sections()


        return {

            "document_id":

                document_id,


            "sections":

                sections

        }


    finally:

        service.close()


# ============================================================
# Stage 4
# Section Catalog
# ============================================================


@router.get(
    "/documents/{document_id}/sections"
)
def get_document_sections(
    document_id: int,
    db: Session = Depends(get_db)
):

    """
    Returns detected sections
    for frontend dropdown.
    """


    document = get_document(
        db,
        document_id
    )


    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )



    service = ExtractionService(
        document.filepath
    )


    try:

        sections = service.get_sections()


        return {

            "status": "success",

            "document_id": document_id,

            "sections": sections

        }


    finally:

        service.close()



# ============================================================
# Stage 4
# Extract Selected Section
# ============================================================


@router.post(
    "/documents/{document_id}/extract/{section_number}"
)
def extract_section(
    document_id: int,
    section_number: int,
    db: Session = Depends(get_db)
):

    """
    Extract section selected
    from dropdown/list.
    """



    document = get_document(
        db,
        document_id
    )


    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )



    service = ExtractionService(
        document.filepath
    )


    formatter = SectionFormatter()



    try:

        result = service.extract_by_number(
            section_number
        )



        if result is None:

            raise HTTPException(
                status_code=404,
                detail="Section not found"
            )



        return formatter.format_json(
            result
        )


    finally:

        service.close()