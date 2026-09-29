import importlib
import sys

from src.config import (
    PDF_PATH,
    CHROMA_PATH,
    COLLECTION_NAME,
    GENERATION_MODEL,
    EMBEDDING_MODEL,
    validate_config
)

from src.logger import get_logger


logger = get_logger(
    "govassist.readiness"
)


def run_check(name, check_function):
    """
    Execute one readiness check.

    Return True when the check passes.
    """

    try:

        check_function()

        logger.info(
            "PASS | %s",
            name
        )

        return True

    except Exception as e:

        logger.error(
            "FAIL | %s | %s",
            name,
            type(e).__name__
        )

        return False


# ---------------------------------------------------------
# CHECK 1 — DEPENDENCIES
# ---------------------------------------------------------

def check_dependencies():

    required_modules = [
        "dotenv",
        "google.genai",
        "streamlit",
        "pypdf",
        "chromadb"
    ]

    for module_name in required_modules:

        importlib.import_module(
            module_name
        )


# ---------------------------------------------------------
# CHECK 2 — CONFIGURATION
# ---------------------------------------------------------

def check_configuration():

    validate_config()

    if not GENERATION_MODEL:

        raise ValueError(
            "Generation model is missing."
        )

    if not EMBEDDING_MODEL:

        raise ValueError(
            "Embedding model is missing."
        )


# ---------------------------------------------------------
# CHECK 3 — PDF
# ---------------------------------------------------------

def check_pdf():

    if not PDF_PATH.is_file():

        raise FileNotFoundError(
            "Government PDF is missing."
        )

    if PDF_PATH.stat().st_size == 0:

        raise ValueError(
            "Government PDF is empty."
        )


# ---------------------------------------------------------
# CHECK 4 — VECTOR DATABASE
# ---------------------------------------------------------

def check_vector_database():

    if not CHROMA_PATH.is_dir():

        raise FileNotFoundError(
            "ChromaDB directory is missing."
        )

    import chromadb

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # get_collection does not silently create
    # a missing collection.

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    record_count = collection.count()

    if record_count == 0:

        raise ValueError(
            "The vector collection is empty."
        )

    logger.info(
        "Indexed records: %s",
        record_count
    )


# ---------------------------------------------------------
# CHECK 5 — APPLICATION IMPORTS
# ---------------------------------------------------------

def check_application_imports():

    modules = [
        "src.gemini_client",
        "src.document_loader",
        "src.chunker",
        "src.metadata",
        "src.embeddings",
        "src.vector_store",
        "src.retriever",
        "src.prompt_engine",
        "src.rag_pipeline",
        "src.conversation"
    ]

    for module_name in modules:

        importlib.import_module(
            module_name
        )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    logger.info(
        "Starting GovAssist readiness checks."
    )

    checks = [
        (
            "Dependencies",
            check_dependencies
        ),
        (
            "Configuration",
            check_configuration
        ),
        (
            "APPR_ACT_1994",
            check_pdf
        ),
        (
            "Vector database",
            check_vector_database
        ),
        (
            "Application imports",
            check_application_imports
        )
    ]

    passed = 0

    for name, check_function in checks:

        if run_check(
            name,
            check_function
        ):

            passed += 1

    total = len(checks)

    logger.info(
        "Readiness result: %s/%s passed.",
        passed,
        total
    )

    if passed != total:

        logger.error(
            "GovAssist is not ready."
        )

        return 1

    logger.info(
        "GovAssist readiness checks passed."
    )

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )