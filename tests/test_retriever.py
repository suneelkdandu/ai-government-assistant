from src.retriever import retrieve_documents


def test_retriever():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — SEMANTIC RETRIEVAL TEST")
    print("=" * 70)


    # -------------------------------------------------
    # TEST QUESTION
    # -------------------------------------------------

    question = (
        "What is gram sabha and what need to be discussed "
        "in this meetinng under Section 6?"
    )


    print("\nQuestion:")
    print(question)


    # -------------------------------------------------
    # RETRIEVE DOCUMENTS
    # -------------------------------------------------

    print("\nSearching government document...")


    result = retrieve_documents(
        query=question,
        top_k=5
    )


    # -------------------------------------------------
    # CHECK RESULT
    # -------------------------------------------------

    if not result["success"]:

        print("\n❌ Retrieval failed.")

        print(
            result["error"]
        )

        return


    print("\n✅ Retrieval successful.")


    # -------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------

    for index, document in enumerate(
        result["documents"],
        start=1
    ):

        metadata = document["metadata"]

        print("\n")
        print("=" * 70)

        print(
            f"RESULT {index}"
        )

        print("-" * 70)

        print(
            "Distance:",
            document["distance"]
        )

        print(
            "Source:",
            metadata.get(
                "source"
            )
        )

        print(
            "Page:",
            metadata.get(
                "page_number"
            )
        )

        print(
            "Chunk ID:",
            metadata.get(
                "chunk_id"
            )
        )

        print(
            "Section:",
            metadata.get(
                "section"
            )
        )

        print(
            "Section Title:",
            metadata.get(
                "section_title"
            )
        )

        print("\nRetrieved Text:")
        print("-" * 70)

        print(
            document["text"]
        )


    print("\n")
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    test_retriever()