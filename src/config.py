import os
from pathlib import Path

from dotenv import load_dotenv


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

DATA_DIR = BASE_DIR / "data"

PDF_PATH = DATA_DIR / "APPR_ACT_1994.pdf"

CHROMA_PATH = BASE_DIR / "chroma_db"


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv(ENV_PATH)


# ---------------------------------------------------------
# GEMINI CONFIGURATION
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GENERATION_MODEL = os.getenv(
    "GENERATION_MODEL",
    "gemini-3.6-flash"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "gemini-embedding-001"
)


# ---------------------------------------------------------
# CHROMADB CONFIGURATION
# ---------------------------------------------------------

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "government_documents"
)


# ---------------------------------------------------------
# DOCUMENT CONFIGURATION
# ---------------------------------------------------------

DOCUMENT_TITLE = (
    "Andhra Pradesh Panchayat Raj Act, 1994"
)


# ---------------------------------------------------------
# CHUNKING CONFIGURATION
# ---------------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200


# ---------------------------------------------------------
# RETRIEVAL CONFIGURATION
# ---------------------------------------------------------

DEFAULT_TOP_K = 5


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

def validate_config():
    """
    Validate the essential application settings.
    """

    if not GEMINI_API_KEY:

        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Check your .env file."
        )

    if CHUNK_SIZE <= 0:

        raise ValueError(
            "CHUNK_SIZE must be greater than zero."
        )

    if not 0 <= CHUNK_OVERLAP < CHUNK_SIZE:

        raise ValueError(
            "CHUNK_OVERLAP must be between "
            "zero and CHUNK_SIZE."
        )

    if DEFAULT_TOP_K <= 0:

        raise ValueError(
            "DEFAULT_TOP_K must be greater than zero."
        )

    return True