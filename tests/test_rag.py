from src.rag_pipeline import generate_rag_answer


def test_rag():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — RAG PIPELINE TEST")
    print("=" * 70)


    question = (
       "What is the procedure for obtaining "
    "an Indian passport?"
    )


    print("\nQUESTION:")
    print(question)


    print("\nGenerating grounded answer...")


    result = generate_rag_answer(
        question=question,
        top_k=5
    )


    if not result["success"]:

        print("\n❌ RAG pipeline failed.")

        print(
            result["error"]
        )

        return


    # -------------------------------------------------
    # DISPLAY ANSWER
    # -------------------------------------------------

    print("\n")
    print("=" * 70)
    print("GOVASSIST ANSWER")
    print("=" * 70)

    print(
        result["answer"]
    )


    # -------------------------------------------------
    # DISPLAY SOURCES
    # -------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)


    for index, document in enumerate(
        result["documents"],
        start=1
    ):

        metadata = document["metadata"]

        print(
            f"\nSource {index}:"
        )

        print(
            "Document:",
            metadata.get("document_title")
        )

        print(
            "Page:",
            metadata.get("page_number")
        )

        print(
            "Section:",
            metadata.get("section")
        )

        print(
            "Section Title:",
            metadata.get("section_title")
        )

        print(
            "Distance:",
            document["distance"]
        )


    print("\n")
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    test_rag()