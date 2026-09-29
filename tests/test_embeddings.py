from src.embeddings import create_embedding


def test_embedding():

    print("\n")
    print("=" * 70)
    print("GOVASSIST AI — EMBEDDING TEST")
    print("=" * 70)


    # -------------------------------------------------
    # SAMPLE GOVERNMENT TEXT
    # -------------------------------------------------

    sample_text = (
        "An application for a licence shall be "
        "accompanied by the required particulars."
    )


    print("\nText:")
    print(sample_text)


    # -------------------------------------------------
    # CREATE EMBEDDING
    # -------------------------------------------------

    print("\nCreating embedding...")

    result = create_embedding(
        sample_text
    )


    # -------------------------------------------------
    # CHECK RESULT
    # -------------------------------------------------

    if not result["success"]:

        print("\n❌ Embedding creation failed.")

        print(
            result["error"]
        )

        return


    # -------------------------------------------------
    # DISPLAY RESULT
    # -------------------------------------------------

    embedding = result["embedding"]

    print("\n✅ Embedding created successfully.")

    print(
        "Embedding dimensions:",
        result["dimension"]
    )

    print("\nFirst 10 vector values:")

    print(
        embedding[:10]
    )


    print("\n")
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    test_embedding()