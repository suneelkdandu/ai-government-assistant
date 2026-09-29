from pathlib import Path

import chromadb

from src.config import (
    CHROMA_PATH,
    COLLECTION_NAME
)


class VectorStore:
    """
    Manage one ChromaDB database and collection.

    Production and tests can use separate instances.
    """

    def __init__(
        self,
        db_path,
        collection_name
    ):

        self.db_path = Path(
            db_path
        )

        self.client = chromadb.PersistentClient(
            path=str(self.db_path)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )


    def add_document(
        self,
        document_id,
        text,
        embedding,
        metadata
    ):
        """
        Store one document chunk with its embedding
        and metadata.
        """

        try:

            if not document_id:

                raise ValueError(
                    "Document ID cannot be empty."
                )

            if not isinstance(text, str) or not text.strip():

                raise ValueError(
                    "Document text cannot be empty."
                )

            if embedding is None or len(embedding) == 0:

                raise ValueError(
                    "Embedding cannot be empty."
                )

            # ChromaDB metadata values cannot be None.
            # Remove unavailable optional metadata fields.

            clean_metadata = {

                key: value

                for key, value in (metadata or {}).items()

                if value is not None
            }

            self.collection.upsert(
                ids=[document_id],
                documents=[text],
                embeddings=[embedding],
                metadatas=[clean_metadata]
            )

            return {
                "success": True
            }

        except Exception as e:

            return {
                "success": False,
                "error": e
            }


    def search_documents(
        self,
        query_embedding,
        top_k=3
    ):
        """
        Search for the most similar document chunks.
        """

        try:

            if (
                query_embedding is None
                or len(query_embedding) == 0
            ):

                raise ValueError(
                    "Query embedding cannot be empty."
                )

            if top_k <= 0:

                raise ValueError(
                    "top_k must be greater than zero."
                )

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            return {
                "success": True,
                "results": results
            }

        except Exception as e:

            return {
                "success": False,
                "error": e
            }


    def count_documents(self):
        """
        Return the number of stored records.
        """

        return self.collection.count()


# ---------------------------------------------------------
# PRODUCTION VECTOR STORE
# ---------------------------------------------------------

_production_store = None


def get_production_store():
    """
    Create the production store only when needed.
    """

    global _production_store

    if _production_store is None:

        _production_store = VectorStore(
            db_path=CHROMA_PATH,
            collection_name=COLLECTION_NAME
        )

    return _production_store


# ---------------------------------------------------------
# BACKWARD-COMPATIBLE FUNCTIONS
# ---------------------------------------------------------

def add_document(
    document_id,
    text,
    embedding,
    metadata
):

    return get_production_store().add_document(
        document_id=document_id,
        text=text,
        embedding=embedding,
        metadata=metadata
    )


def search_documents(
    query_embedding,
    top_k=3
):

    return get_production_store().search_documents(
        query_embedding=query_embedding,
        top_k=top_k
    )