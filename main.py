from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse

from utils import build_keywords_text, extract_text_from_docx, extract_text_from_pdf

app = FastAPI()

PDF_CONTENT_TYPES = {"application/pdf", "application/octet-stream"}
DOCX_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/octet-stream",
}
UPLOAD_ERROR = "Please upload a PDF or DOCX file"


@app.post(
    "/parse-resume",
    responses={400: {"description": UPLOAD_ERROR}},
)
async def parse_resume(file: Annotated[UploadFile, File(...)]):
    extension = Path(file.filename or "").suffix.lower()
    file_bytes = await file.read()

    if extension == ".pdf" and file.content_type in PDF_CONTENT_TYPES:
        resume_text = extract_text_from_pdf(file_bytes)
    elif extension == ".docx" and file.content_type in DOCX_CONTENT_TYPES:
        resume_text = extract_text_from_docx(file_bytes)
    else:
        raise HTTPException(status_code=400, detail=UPLOAD_ERROR)

    return PlainTextResponse(build_keywords_text(resume_text))
