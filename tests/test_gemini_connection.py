from src.gemini_client import get_gemini_client


def test_gemini_connection():
    try:
        client = get_gemini_client()

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=(
                "Explain artificial intelligence "
                "in one simple sentence."
            )
        )

        print("\nGemini connection successful.")

        print("\nGemini response:")
        print(interaction.output_text)

    except Exception as e:
        print("\nGemini connection failed.")
        print(e)


if __name__ == "__main__":
    test_gemini_connection()