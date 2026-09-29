from src.rag_pipeline import (
    generate_rag_answer
)

from evaluation.grounding_evaluator import (
    evaluate_grounding
)


def test_grounding():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — CLAIM-LEVEL GROUNDING TEST")
    print("=" * 70)


    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    question = (
        "What is Gram Sabha and what needs to be "
        "discussed in its meeting under Section 6?"
    )


    print("\nQUESTION:")
    print(question)


    # -----------------------------------------------------
    # GENERATE RAG ANSWER
    # -----------------------------------------------------

    print(
        "\nGenerating GovAssist answer..."
    )


    rag_result = generate_rag_answer(
        question=question,
        conversation_history=[],
        top_k=5
    )


    if not rag_result["success"]:

        print(
            "\n❌ RAG generation failed."
        )

        print(
            rag_result["error"]
        )

        return


    answer = rag_result["answer"]

    documents = rag_result[
        "documents"
    ]


    print("\nGENERATED ANSWER:")
    print("-" * 70)

    print(answer)


    # -----------------------------------------------------
    # RUN GROUNDING EVALUATION
    # -----------------------------------------------------

    print(
        "\nEvaluating factual claims..."
    )


    evaluation = evaluate_grounding(
        question=question,
        answer=answer,
        documents=documents
    )


    if not evaluation["success"]:

        print(
            "\n❌ Grounding evaluation failed."
        )

        print(
            evaluation["error"]
        )

        return


    # -----------------------------------------------------
    # DISPLAY CLAIM RESULTS
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("CLAIM-LEVEL RESULTS")
    print("=" * 70)


    for index, claim in enumerate(
        evaluation["claims"],
        start=1
    ):

        print(
            f"\nClaim {index}:"
        )

        print(
            claim.get(
                "claim"
            )
        )

        print(
            "Status:",
            claim.get(
                "status"
            )
        )

        print(
            "Evidence:",
            claim.get(
                "evidence"
            )
        )


    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("GROUNDING SUMMARY")
    print("=" * 70)


    print(
        "Total factual claims:",
        evaluation["total_claims"]
    )

    print(
        "Supported claims:",
        evaluation["supported_claims"]
    )

    print(
        "Unsupported claims:",
        evaluation["unsupported_claims"]
    )

    print(
        "Grounding score:",
        f"{evaluation['grounding_score']:.2%}"
    )


    print("=" * 70)


if __name__ == "__main__":
    test_grounding()