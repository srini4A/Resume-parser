from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse

from utils import build_compact_resume_text, extract_text_from_pdf

app = FastAPI()

ALLOWED_PDF_CONTENT_TYPES = {"application/pdf", "application/octet-stream"}
PDF_UPLOAD_ERROR = "Please upload a PDF file"


@app.post(
    "/parse-resume",
    responses={400: {"description": "Please upload a PDF file"}},
)
async def parse_resume(file: Annotated[UploadFile, File(...)]):
    if file.content_type not in ALLOWED_PDF_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail=PDF_UPLOAD_ERROR)

    pdf_bytes = await file.read()
    resume_text = extract_text_from_pdf(pdf_bytes)

    compact_text = build_compact_resume_text(
        filename=file.filename or "resume.pdf",
        resume_text=resume_text,
    )
    return PlainTextResponse(compact_text)
