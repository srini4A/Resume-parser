import re
from io import BytesIO

import pdfplumber


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


def extract_words(text: str):
    # Keep only lowercase words and numbers to make downstream prompts compact.
    return re.findall(r"[a-z0-9]+", text.lower())


def build_compact_resume_text(filename: str, resume_text: str) -> str:
    words = extract_words(resume_text)

    # Return full parsed content with no count fields.
    return "\n".join(
        [
            f"FILE|{filename}",
            "TEXT|" + " ".join(resume_text.split()),
            "WORDS|" + ",".join(words),
        ]
    )
