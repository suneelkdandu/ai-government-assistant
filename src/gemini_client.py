from google import genai

from src.config import GEMINI_API_KEY


def get_gemini_client():
    """
    Create and return a Gemini API client.
    """

    if not GEMINI_API_KEY:

        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Check your .env file."
        )

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        return client

    except Exception as e:

        raise RuntimeError(
            f"Failed to initialize Gemini client: {e}"
        ) from e