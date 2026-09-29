import tempfile

from pathlib import Path

from src.vector_store import VectorStore


def test_vector_store():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — ISOLATED VECTOR STORE TEST")
    print("=" * 70)


    # -----------------------------------------------------
    # CREATE TEMPORARY DATABASE
    # -----------------------------------------------------

    with tempfile.TemporaryDirectory() as temp_dir:

        test_db_path = (
            Path(temp_dir) / "test_chroma_db"
        )

        store = VectorStore(
            db_path=test_db_path,
            collection_name="test_documents"
        )


        # -------------------------------------------------
        # TEST DATA
        # -------------------------------------------------

        document_text = (
            "A Gram Panchayat is a local "
            "government institution."
        )

        # Small fixed vectors are sufficient to test
        # ChromaDB storage and retrieval.

        document_embedding = [
            0.1,
            0.2,
            0.3
        ]

        query_embedding = [
            0.1,
            0.2,
            0.3
        ]

        metadata = {
            "source": "test_document",
            "page_number": 1,
            "chunk_id": 1
        }


        # -------------------------------------------------
        # STORE DOCUMENT
        # -------------------------------------------------

        result = store.add_document(
            document_id="test_chunk_001",
            text=document_text,
            embedding=document_embedding,
            metadata=metadata
        )

        assert result["success"], (
            f"Storage failed: {result.get('error')}"
        )

        assert store.count_documents() == 1

        print(
            "\nDocument stored successfully."
        )


        # -------------------------------------------------
        # SEARCH DOCUMENT
        # -------------------------------------------------

        result = store.search_documents(
            query_embedding=query_embedding,
            top_k=1
        )

        assert result["success"], (
            f"Search failed: {result.get('error')}"
        )

        documents = result["results"]["documents"][0]

        assert documents, (
            "No documents were retrieved."
        )

        assert documents[0] == document_text

        print(
            "Document retrieved successfully."
        )


        # -------------------------------------------------
        # VERIFY UPSERT
        # -------------------------------------------------

        result = store.add_document(
            document_id="test_chunk_001",
            text=document_text,
            embedding=document_embedding,
            metadata=metadata
        )

        assert result["success"]

        assert store.count_documents() == 1

        print(
            "Upsert verified successfully."
        )


    # TemporaryDirectory removes the test database
    # when the with block finishes.

    print(
        "Temporary database cleaned up."
    )

    print("\n")
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    test_vector_store()