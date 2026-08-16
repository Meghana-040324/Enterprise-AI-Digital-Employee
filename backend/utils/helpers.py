# helpers.py
import re
import uuid
from pathlib import Path


def generate_id() -> str:
    return str(uuid.uuid4())


def clean_text(text: str) -> str:

    text = text.replace("\x00", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_extension(filename: str) -> str:

    return Path(filename).suffix.lower()


def chunk_text(
    text: str,
    chunk_size: int = 1500,
    overlap: int = 200
):

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size - overlap

    return chunks