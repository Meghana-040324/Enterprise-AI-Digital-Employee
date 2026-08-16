# rag_service.py
import re

from services.document_service import (
    document_service
)

from utils.helpers import chunk_text


class RAGService:

    def search(
        self,
        query: str,
        limit: int = 5
    ):

        documents = (
            document_service
            .get_all_documents()
        )

        if not documents:
            return []

        query_words = set(
            re.findall(
                r"\w+",
                query.lower()
            )
        )

        results = []

        for document in documents:

            chunks = chunk_text(
                document["text"]
            )

            for chunk in chunks:

                words = set(
                    re.findall(
                        r"\w+",
                        chunk.lower()
                    )
                )

                score = len(
                    query_words &
                    words
                )

                if score:

                    results.append(
                        {
                            "score":
                                score,

                            "filename":
                                document[
                                    "filename"
                                ],

                            "content":
                                chunk
                        }
                    )

        results.sort(
            key=lambda item:
                item["score"],
            reverse=True
        )

        return results[:limit]


rag_service = RAGService()