import re
from io import BytesIO

import pdfplumber
from docx import Document


def extract_text_from_pdf(pdf_file):
    text_parts = []

    if isinstance(pdf_file, (bytes, bytearray)):
        pdf_file = BytesIO(pdf_file)

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def extract_text_from_docx(docx_file):
    if isinstance(docx_file, (bytes, bytearray)):
        docx_file = BytesIO(docx_file)

    document = Document(docx_file)
    text_parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]

    for table in document.tables:
        for row in table.rows:
            row_text = " ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                text_parts.append(row_text)

    return "\n".join(text_parts)


def extract_words(text: str):
    # Keep only lowercase words and numbers to make downstream prompts compact.
    return re.findall(r"[a-z0-9]+", text.lower())


def build_keywords_text(resume_text: str) -> str:
    return ",".join(extract_words(resume_text))
