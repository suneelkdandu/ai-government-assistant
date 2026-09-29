from src.config import EMBEDDING_MODEL

from src.gemini_client import get_gemini_client


def create_embedding(text):
    """
    Convert text into a numerical embedding vector
    using the configured Gemini embedding model.
    """

    try:

        if not isinstance(text, str):

            raise ValueError(
                "Text must be a string."
            )

        if not text.strip():

            raise ValueError(
                "Text cannot be empty."
            )

        client = get_gemini_client()

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )

        if not response.embeddings:

            raise RuntimeError(
                "The embedding API returned no embeddings."
            )

        embedding = response.embeddings[0].values

        if not embedding:

            raise RuntimeError(
                "The embedding API returned an empty vector."
            )

        return {
            "success": True,
            "embedding": embedding,
            "dimension": len(embedding)
        }

    except Exception as e:

        return {
            "success": False,
            "error": e
        }