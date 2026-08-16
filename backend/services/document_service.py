# document_service.py
from pathlib import Path

from fastapi import UploadFile
from pypdf import PdfReader
from docx import Document

from config import (
    UPLOAD_DIR,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB
)

from utils.helpers import (
    generate_id,
    clean_text,
    get_extension
)


class DocumentService:

    def __init__(self):

        self.documents = {}

    async def save_and_extract(
        self,
        file: UploadFile
    ):

        filename = (
            file.filename or
            "document"
        )

        extension = get_extension(
            filename
        )

        if extension not in ALLOWED_EXTENSIONS:

            raise ValueError(
                "Only PDF, DOCX and TXT files are supported."
            )

        content = await file.read()

        max_bytes = (
            MAX_FILE_SIZE_MB *
            1024 *
            1024
        )

        if len(content) > max_bytes:

            raise ValueError(
                f"Maximum file size is "
                f"{MAX_FILE_SIZE_MB} MB."
            )

        document_id = generate_id()

        path = (
            UPLOAD_DIR /
            f"{document_id}{extension}"
        )

        path.write_bytes(content)

        if extension == ".pdf":

            text = self._extract_pdf(
                path
            )

        elif extension == ".docx":

            text = self._extract_docx(
                path
            )

        else:

            text = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        text = clean_text(text)

        self.documents[document_id] = {

            "id":
                document_id,

            "filename":
                filename,

            "path":
                str(path),

            "text":
                text
        }

        return self.documents[
            document_id
        ]

    def _extract_pdf(
        self,
        path: Path
    ):

        reader = PdfReader(
            str(path)
        )

        pages = []

        for page in reader.pages:

            pages.append(
                page.extract_text()
                or ""
            )

        return "\n".join(
            pages
        )

    def _extract_docx(
        self,
        path: Path
    ):

        document = Document(
            str(path)
        )

        return "\n".join(

            paragraph.text

            for paragraph
            in document.paragraphs
        )

    def get_all_documents(
        self
    ):

        return list(
            self.documents.values()
        )


document_service = DocumentService()