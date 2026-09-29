from evaluation.evaluation_dataset import (
    EVALUATION_DATASET
)

from src.rag_pipeline import (
    generate_rag_answer
)


FALLBACK_RESPONSE = (
    "I could not find this information "
    "in the indexed government document."
)


def check_expected_keywords(
    answer,
    expected_keywords
):
    """
    Check which expected keywords appear
    in the generated answer.
    """

    answer_lower = answer.lower()

    found = []
    missing = []

    for keyword in expected_keywords:

        if keyword.lower() in answer_lower:
            found.append(keyword)

        else:
            missing.append(keyword)

    return found, missing


def evaluate_rag():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — RAG ANSWER EVALUATION")
    print("=" * 70)


    total_questions = len(
        EVALUATION_DATASET
    )

    supported_questions = 0

    keyword_scores = []

    fallback_tests = 0
    fallback_successes = 0


    # -----------------------------------------------------
    # EVALUATE EACH QUESTION
    # -----------------------------------------------------

    for item in EVALUATION_DATASET:

        question_id = item["id"]

        question = item["question"]

        print("Current evaluation item:", item)
        supported = item["supported"]

        expected_keywords = item[
            "expected_keywords"
        ]


        print("\n")
        print("=" * 70)

        print(
            "Question ID:",
            question_id
        )

        print(
            "Question:",
            question
        )

        print(
            "Expected to be supported:",
            supported
        )


        # -------------------------------------------------
        # RUN COMPLETE RAG PIPELINE
        # -------------------------------------------------

        result = generate_rag_answer(
            question=question,
            conversation_history=[],
            top_k=5
        )


        if not result["success"]:

            print(
                "\n❌ RAG pipeline failed."
            )

            print(
                result["error"]
            )

            continue


        answer = result["answer"]


        print("\nGenerated answer:")
        print("-" * 70)

        print(answer)


        # -------------------------------------------------
        # SUPPORTED QUESTION
        # -------------------------------------------------

        if supported:

            supported_questions += 1


            found, missing = (
                check_expected_keywords(
                    answer,
                    expected_keywords
                )
            )


            if expected_keywords:

                keyword_score = (
                    len(found)
                    / len(expected_keywords)
                )

            else:

                keyword_score = 0


            keyword_scores.append(
                keyword_score
            )


            print("\nGround-truth keyword check:")

            print(
                "Expected:",
                expected_keywords
            )

            print(
                "Found:",
                found
            )

            print(
                "Missing:",
                missing
            )

            print(
                "Keyword coverage:",
                f"{keyword_score:.2%}"
            )


            # ---------------------------------------------
            # RETRIEVED SECTION CHECK
            # ---------------------------------------------

            expected_section = item[
                "expected_section"
            ]


            retrieved_sections = [

                str(
                    document[
                        "metadata"
                    ].get(
                        "section"
                    )
                )

                for document in result[
                    "documents"
                ]
            ]


            print(
                "Expected section:",
                expected_section
            )

            print(
                "Retrieved sections:",
                retrieved_sections
            )


        # -------------------------------------------------
        # UNSUPPORTED QUESTION
        # -------------------------------------------------

        else:

            fallback_tests += 1


            fallback_correct = (
                answer.strip()
                == FALLBACK_RESPONSE
            )


            if fallback_correct:

                fallback_successes += 1


            print(
                "\nFallback response correct:",
                fallback_correct
            )


    # -----------------------------------------------------
    # FINAL METRICS
    # -----------------------------------------------------

    if keyword_scores:

        average_keyword_coverage = (
            sum(keyword_scores)
            / len(keyword_scores)
        )

    else:

        average_keyword_coverage = 0


    if fallback_tests:

        fallback_accuracy = (
            fallback_successes
            / fallback_tests
        )

    else:

        fallback_accuracy = 0


    # -----------------------------------------------------
    # DISPLAY REPORT
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RAG EVALUATION RESULTS")
    print("=" * 70)


    print(
        "Questions evaluated:",
        total_questions
    )

    print(
        "Supported questions:",
        supported_questions
    )

    print(
        "Average keyword coverage:",
        f"{average_keyword_coverage:.2%}"
    )

    print(
        "Unsupported questions tested:",
        fallback_tests
    )

    print(
        "Fallback accuracy:",
        f"{fallback_accuracy:.2%}"
    )


    print("=" * 70)


if __name__ == "__main__":
    evaluate_rag()