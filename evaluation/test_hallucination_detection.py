from src.retriever import (
    retrieve_documents
)

from evaluation.grounding_evaluator import (
    evaluate_grounding
)


def test_hallucination_detection():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — HALLUCINATION DETECTION TEST")
    print("=" * 70)


    question = (
        "What is Gram Sabha and what needs to be "
        "discussed in its meeting under Section 6?"
    )


    # -----------------------------------------------------
    # RETRIEVE REAL DOCUMENT EVIDENCE
    # -----------------------------------------------------

    retrieval = retrieve_documents(
        query=question,
        top_k=5
    )


    if not retrieval["success"]:

        print(
            "❌ Retrieval failed."
        )

        print(
            retrieval["error"]
        )

        return


    documents = retrieval[
        "documents"
    ]


    # -----------------------------------------------------
    # DELIBERATELY INSERT A FALSE / UNSUPPORTED CLAIM
    # -----------------------------------------------------

    fake_answer = """
The Gram Sabha discusses matters concerning village
development and beneficiaries of development programmes.

Every Gram Sabha member must also pay an annual
membership fee of Rs. 500.
"""


    print("\nTEST ANSWER:")
    print(fake_answer)


    # -----------------------------------------------------
    # EVALUATE
    # -----------------------------------------------------

    evaluation = evaluate_grounding(
        question=question,
        answer=fake_answer,
        documents=documents
    )


    if not evaluation["success"]:

        print(
            "❌ Evaluation failed."
        )

        print(
            evaluation["error"]
        )

        return


    print("\n")
    print("=" * 70)
    print("CLAIM RESULTS")
    print("=" * 70)


    for claim in evaluation["claims"]:

        print(
            "\nClaim:",
            claim.get("claim")
        )

        print(
            "Status:",
            claim.get("status")
        )

        print(
            "Evidence:",
            claim.get("evidence")
        )


    print("\nGrounding score:")

    print(
        f"{evaluation['grounding_score']:.2%}"
    )


if __name__ == "__main__":
    test_hallucination_detection()