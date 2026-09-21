import re
from pathlib import Path

from pypdf import PdfReader


UPLOAD_DIR = Path("data/documents")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}


def ensure_upload_directory() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def extract_text(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension in {".txt", ".md"}:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    raise ValueError(f"Unsupported file type: {extension}")


def extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(file_path)

    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    # Remove null/control characters while preserving
    # useful whitespace such as newlines and tabs.
    text = text.replace("\x00", "")
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Normalize common PDF bullet characters.
    text = text.replace("•", "- ")
    text = text.replace("▪", "- ")
    text = text.replace("●", "- ")

    # Normalize spaces without destroying paragraphs.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        start = end - chunk_overlap

    return chunks