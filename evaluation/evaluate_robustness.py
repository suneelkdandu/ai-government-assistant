from evaluation.robustness_dataset import (
    ROBUSTNESS_DATASET
)

from src.rag_pipeline import (
    generate_rag_answer
)


FALLBACK_RESPONSE = (
    "I could not find this information "
    "in the indexed government document."
)


def section_found(
    documents,
    expected_section
):
    """
    Check whether the expected section appears
    anywhere in the retrieved documents.
    """

    if expected_section is None:
        return False

    for document in documents:

        metadata = document.get(
            "metadata",
            {}
        )

        section = metadata.get(
            "section"
        )

        if str(section) == str(
            expected_section
        ):
            return True

    return False


def evaluate_robustness():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — ROBUSTNESS EVALUATION")
    print("=" * 70)


    total_tests = len(
        ROBUSTNESS_DATASET
    )

    passed_tests = 0


    # -----------------------------------------------------
    # RUN EACH TEST
    # -----------------------------------------------------

    for item in ROBUSTNESS_DATASET:

        test_id = item["id"]

        test_type = item["type"]

        question = item["question"]

        expected_section = item[
            "expected_section"
        ]

        should_be_supported = item[
            "should_be_supported"
        ]


        print("\n")
        print("=" * 70)

        print(
            "Test:",
            test_id
        )

        print(
            "Type:",
            test_type
        )

        print(
            "Question:",
            repr(question)
        )


        # -------------------------------------------------
        # EMPTY INPUT TEST
        # -------------------------------------------------

        if test_type == "empty":

            result = generate_rag_answer(
                question=question,
                conversation_history=[],
                top_k=5
            )


            # Our RAG pipeline should reject empty input.
            passed = (
                result["success"] is False
            )


            print(
                "Empty input rejected:",
                passed
            )


            if not passed:

                print(
                    "❌ Empty question was not "
                    "handled correctly."
                )


        # -------------------------------------------------
        # NORMAL RAG TEST
        # -------------------------------------------------

        else:

            result = generate_rag_answer(
                question=question,
                conversation_history=[],
                top_k=5
            )


            if not result["success"]:

                print(
                    "❌ RAG pipeline failed:"
                )

                print(
                    result["error"]
                )

                passed = False


            else:

                answer = result["answer"]

                documents = result.get(
                    "documents",
                    []
                )


                print("\nAnswer:")
                print(answer)


                # -----------------------------------------
                # SUPPORTED QUESTION
                # -----------------------------------------

                if should_be_supported:

                    expected_found = (
                        section_found(
                            documents,
                            expected_section
                        )
                    )


                    fallback_used = (
                        answer.strip()
                        == FALLBACK_RESPONSE
                    )


                    passed = (
                        expected_found
                        and not fallback_used
                    )


                    print(
                        "\nExpected section:",
                        expected_section
                    )

                    print(
                        "Expected section retrieved:",
                        expected_found
                    )

                    print(
                        "Fallback incorrectly used:",
                        fallback_used
                    )


                # -----------------------------------------
                # UNSUPPORTED QUESTION
                # -----------------------------------------

                else:

                    fallback_used = (
                        answer.strip()
                        == FALLBACK_RESPONSE
                    )


                    passed = fallback_used


                    print(
                        "\nCorrect fallback used:",
                        fallback_used
                    )


        # -------------------------------------------------
        # TEST RESULT
        # -------------------------------------------------

        if passed:

            passed_tests += 1

            print(
                "\n✅ TEST PASSED"
            )

        else:

            print(
                "\n❌ TEST FAILED"
            )


    # -----------------------------------------------------
    # FINAL RESULTS
    # -----------------------------------------------------

    robustness_score = (
        passed_tests
        / total_tests
        if total_tests
        else 0
    )


    print("\n")
    print("=" * 70)
    print("ROBUSTNESS EVALUATION RESULTS")
    print("=" * 70)


    print(
        "Total tests:",
        total_tests
    )

    print(
        "Passed:",
        passed_tests
    )

    print(
        "Failed:",
        total_tests - passed_tests
    )

    print(
        "Robustness pass rate:",
        f"{robustness_score:.2%}"
    )


    print("=" * 70)


if __name__ == "__main__":
    evaluate_robustness()