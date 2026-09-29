from src.document_loader import load_pdf
from src.chunker import chunk_pages
from src.embeddings import create_embedding
from src.vector_store import add_document


from src.config import (
    PDF_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


def index_document():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — GOVERNMENT DOCUMENT INDEXING")
    print("=" * 70)


    # -----------------------------------------------------
    # STEP 1 — LOAD PDF
    # -----------------------------------------------------

    print("\nSTEP 1 — Loading government PDF")
    print("-" * 70)

    document = load_pdf(
        PDF_PATH
    )

    if not document["success"]:

        print("❌ PDF loading failed.")
        print(document["error"])

        return


    print("✅ PDF loaded successfully.")

    print(
        "File:",
        document["file_name"]
    )

    print(
        "Total PDF pages:",
        document["total_pdf_pages"]
    )

    print(
        "Pages containing text:",
        len(document["pages"])
    )


    # -----------------------------------------------------
    # STEP 2 — CREATE CHUNKS
    # -----------------------------------------------------

    print("\nSTEP 2 — Creating chunks")
    print("-" * 70)

    chunk_result = chunk_pages(
        pages=document["pages"],
        source=document["file_name"],
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    if not chunk_result["success"]:

        print("❌ Chunking failed.")
        print(chunk_result["error"])

        return


    chunks = chunk_result["chunks"]


    print("✅ Chunking successful.")

    print(
        "Total chunks:",
        len(chunks)
    )


    # -----------------------------------------------------
    # STEP 3 — EMBED AND STORE CHUNKS
    # -----------------------------------------------------

    print("\nSTEP 3 — Creating embeddings and indexing")
    print("-" * 70)


    successful_chunks = 0
    failed_chunks = 0


    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        text = chunk["text"]

        metadata = chunk["metadata"]


        print(
            f"Processing chunk "
            f"{index}/{len(chunks)}..."
        )


        # -------------------------------------------------
        # CREATE EMBEDDING
        # -------------------------------------------------

        embedding_result = create_embedding(
            text
        )


        if not embedding_result["success"]:

            failed_chunks += 1

            print(
                f"❌ Embedding failed "
                f"for chunk {index}"
            )

            print(
                embedding_result["error"]
            )

            continue


        embedding = (
            embedding_result["embedding"]
        )


        # -------------------------------------------------
        # CREATE UNIQUE CHROMADB ID
        # -------------------------------------------------

        document_id = (
            f"government_chunk_"
            f"{metadata['chunk_id']:04d}"
        )


        # -------------------------------------------------
        # STORE IN CHROMADB
        # -------------------------------------------------

        store_result = add_document(
            document_id=document_id,
            text=text,
            embedding=embedding,
            metadata=metadata
        )


        if store_result["success"]:

            successful_chunks += 1

            print(
                f"✅ Chunk {index} indexed"
            )


        else:

            failed_chunks += 1

            print(
                f"❌ Storage failed "
                f"for chunk {index}"
            )

            print(
                store_result["error"]
            )


    # -----------------------------------------------------
    # FINAL SUMMARY
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("INDEXING SUMMARY")
    print("=" * 70)

    print(
        "Total chunks:",
        len(chunks)
    )

    print(
        "Successfully indexed:",
        successful_chunks
    )

    print(
        "Failed:",
        failed_chunks
    )

    print("=" * 70)


if __name__ == "__main__":
    index_document()