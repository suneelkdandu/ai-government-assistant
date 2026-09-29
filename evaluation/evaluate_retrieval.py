from evaluation.evaluation_dataset import EVALUATION_DATASET

from src.retriever import retrieve_documents


def section_found(
    documents,
    expected_section,
    top_k
):
    """
    Check whether the expected section occurs
    within the first top_k retrieved documents.
    """

    for document in documents[:top_k]:

        metadata = document["metadata"]

        retrieved_section = metadata.get(
            "section"
        )

        if str(retrieved_section) == str(
            expected_section
        ):
            return True

    return False


def evaluate_retrieval():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — RETRIEVAL EVALUATION")
    print("=" * 70)


    total_questions = len(
        EVALUATION_DATASET
    )

    recall_at_1_hits = 0
    recall_at_3_hits = 0
    recall_at_5_hits = 0


    # -----------------------------------------------------
    # EVALUATE EACH QUESTION
    # -----------------------------------------------------

    for item in EVALUATION_DATASET:

        question_id = item["id"]

        question = item["question"]

        expected_section = item[
            "expected_section"
        ]


        print("\n")
        print("-" * 70)

        print(
            "Question ID:",
            question_id
        )

        print(
            "Question:",
            question
        )

        print(
            "Expected section:",
            expected_section
        )


        # -------------------------------------------------
        # RETRIEVE TOP 5
        # -------------------------------------------------

        result = retrieve_documents(
            query=question,
            top_k=5
        )


        if not result["success"]:

            print(
                "❌ Retrieval failed:"
            )

            print(
                result["error"]
            )

            continue


        documents = result["documents"]


        # -------------------------------------------------
        # SHOW RETRIEVED SECTIONS
        # -------------------------------------------------

        retrieved_sections = [

            str(
                document["metadata"].get(
                    "section"
                )
            )

            for document in documents
        ]


        print(
            "Retrieved sections:",
            retrieved_sections
        )


        # -------------------------------------------------
        # RECALL @ 1
        # -------------------------------------------------

        hit_at_1 = section_found(
            documents,
            expected_section,
            1
        )


        # -------------------------------------------------
        # RECALL @ 3
        # -------------------------------------------------

        hit_at_3 = section_found(
            documents,
            expected_section,
            3
        )


        # -------------------------------------------------
        # RECALL @ 5
        # -------------------------------------------------

        hit_at_5 = section_found(
            documents,
            expected_section,
            5
        )


        if hit_at_1:
            recall_at_1_hits += 1

        if hit_at_3:
            recall_at_3_hits += 1

        if hit_at_5:
            recall_at_5_hits += 1


        print(
            "Hit@1:",
            hit_at_1
        )

        print(
            "Hit@3:",
            hit_at_3
        )

        print(
            "Hit@5:",
            hit_at_5
        )


    # -----------------------------------------------------
    # CALCULATE FINAL METRICS
    # -----------------------------------------------------

    recall_at_1 = (
        recall_at_1_hits
        / total_questions
    )

    recall_at_3 = (
        recall_at_3_hits
        / total_questions
    )

    recall_at_5 = (
        recall_at_5_hits
        / total_questions
    )


    # -----------------------------------------------------
    # DISPLAY REPORT
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RETRIEVAL EVALUATION RESULTS")
    print("=" * 70)


    print(
        f"Questions evaluated: "
        f"{total_questions}"
    )

    print(
        f"Recall@1: "
        f"{recall_at_1:.2%}"
    )

    print(
        f"Recall@3: "
        f"{recall_at_3:.2%}"
    )

    print(
        f"Recall@5: "
        f"{recall_at_5:.2%}"
    )


    print("=" * 70)


if __name__ == "__main__":
    evaluate_retrieval()