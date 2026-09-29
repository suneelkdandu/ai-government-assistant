from src.document_loader import load_pdf
from src.chunker import chunk_pages


def test_chunker():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — CHUNKING AND METADATA TEST")
    print("=" * 70)


    # -----------------------------------------------------
    # STEP 1 — LOAD PDF
    # -----------------------------------------------------

    print("\nSTEP 1 — Loading PDF")
    print("-" * 70)

    document = load_pdf(
        "data/APPR_ACT_1994.pdf"
    )


    if not document["success"]:

        print("❌ PDF loading failed.")

        print(
            document["error"]
        )

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


    result = chunk_pages(

        pages=document["pages"],

        source=document["file_name"],

        chunk_size=1000,

        overlap=200
    )


    if not result["success"]:

        print("❌ Chunking failed.")

        print(
            result["error"]
        )

        return


    print("✅ Chunking successful.")

    print(
        "Total chunks:",
        result["count"]
    )


    # -----------------------------------------------------
    # STEP 3 — DISPLAY SAMPLE CHUNKS
    # -----------------------------------------------------

    print("\nSTEP 3 — Sample chunks")
    print("-" * 70)


    for chunk in result["chunks"][:5]:

        metadata = chunk["metadata"]

        print("\n")
        print("=" * 70)

        print(
            "Chunk ID:",
            metadata["chunk_id"]
        )

        print(
            "Source:",
            metadata["source"]
        )

        print(
            "Document:",
            metadata["document_title"]
        )

        print(
            "Page:",
            metadata["page_number"]
        )

        print(
            "Section:",
            metadata["section"]
        )

        print(
            "Section Title:",
            metadata["section_title"]
        )

        print("\nText Preview:")
        print("-" * 70)

        print(
            chunk["text"][:500]
        )


    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    test_chunker()