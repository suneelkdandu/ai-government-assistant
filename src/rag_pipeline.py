"""
GovAssist AI — RAG Pipeline

Responsibilities:
1. Validate the user's question.
2. Build conversation context.
3. Retrieve relevant government document chunks.
4. Build a document-grounded prompt.
5. Generate an answer using Gemini.
6. Return the answer and retrieved sources.
7. Log important application events.
"""

from src.config import (
    GENERATION_MODEL,
    DEFAULT_TOP_K
)

from src.gemini_client import get_gemini_client

from src.retriever import retrieve_documents

from src.prompt_engine import SYSTEM_INSTRUCTION

from src.conversation import build_conversation_context

from src.logger import get_logger


# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------

logger = get_logger(
    "govassist.rag"
)


# ---------------------------------------------------------
# FALLBACK RESPONSE
# ---------------------------------------------------------

FALLBACK_RESPONSE = (
    "I could not find this information "
    "in the indexed government document."
)


# ---------------------------------------------------------
# BUILD DOCUMENT CONTEXT
# ---------------------------------------------------------

def build_context(documents):
    """
    Convert retrieved document chunks into
    structured context for the Gemini model.
    """

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        metadata = document.get(
            "metadata",
            {}
        )

        document_text = document.get(
            "text",
            ""
        )

        source = metadata.get(
            "source",
            "Unknown"
        )

        document_title = metadata.get(
            "document_title",
            "Unknown"
        )

        page_number = metadata.get(
            "page_number",
            "Unknown"
        )

        section = metadata.get(
            "section",
            "Unknown"
        )

        section_title = metadata.get(
            "section_title",
            "Unknown"
        )

        context_part = f"""
SOURCE {index}

Document:
{document_title}

File:
{source}

Page:
{page_number}

Section:
{section}

Section Title:
{section_title}

DOCUMENT TEXT:
{document_text}
"""

        context_parts.append(
            context_part
        )

    return "\n\n".join(
        context_parts
    )


# ---------------------------------------------------------
# GENERATE RAG ANSWER
# ---------------------------------------------------------

def generate_rag_answer(
    question,
    conversation_history=None,
    top_k=DEFAULT_TOP_K
):
    """
    Generate a document-grounded answer.

    Parameters
    ----------
    question:
        Current user question.

    conversation_history:
        Previous user and assistant messages.

    top_k:
        Maximum number of document chunks to retrieve.

    Returns
    -------
    Dictionary containing:
        success
        answer
        documents

    On failure:
        success
        error
    """

    try:

        # -------------------------------------------------
        # 1. LOG REQUEST
        # -------------------------------------------------

        logger.info(
            "RAG request started."
        )

        # -------------------------------------------------
        # 2. VALIDATE INPUT
        # -------------------------------------------------

        if not isinstance(question, str):

            raise ValueError(
                "Question must be a string."
            )

        if not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        if not isinstance(top_k, int) or top_k <= 0:

            raise ValueError(
                "top_k must be a positive integer."
            )

        logger.info(
            "Input validation completed."
        )

        # -------------------------------------------------
        # 3. BUILD CONVERSATION CONTEXT
        # -------------------------------------------------

        conversation_context = (
            build_conversation_context(
                conversation_history or []
            )
        )

        logger.info(
            "Conversation context prepared."
        )

        # -------------------------------------------------
        # 4. BUILD RETRIEVAL QUERY
        # -------------------------------------------------

        if conversation_context:

            retrieval_query = f"""
Previous conversation:

{conversation_context}

Current question:

{question}
"""

        else:

            retrieval_query = question

        # -------------------------------------------------
        # 5. RETRIEVE RELEVANT DOCUMENTS
        # -------------------------------------------------

        logger.info(
            "Document retrieval started."
        )

        retrieval_result = retrieve_documents(
            query=retrieval_query,
            top_k=top_k
        )

        if not retrieval_result["success"]:

            raise RuntimeError(
                "Document retrieval failed."
            )

        documents = retrieval_result.get(
            "documents",
            []
        )

        logger.info(
            "Document retrieval completed."
        )

        logger.info(
            "Retrieved document chunks: %s",
            len(documents)
        )

        # -------------------------------------------------
        # 6. HANDLE EMPTY RETRIEVAL
        # -------------------------------------------------

        if not documents:

            logger.warning(
                "No relevant document chunks were retrieved."
            )

            return {
                "success": True,
                "answer": FALLBACK_RESPONSE,
                "documents": []
            }

        # -------------------------------------------------
        # 7. BUILD DOCUMENT CONTEXT
        # -------------------------------------------------

        document_context = build_context(
            documents
        )

        logger.info(
            "Document context prepared."
        )

        # -------------------------------------------------
        # 8. BUILD GROUNDED PROMPT
        # -------------------------------------------------

        prompt = f"""
You are answering a question about an indexed
government document.

PREVIOUS CONVERSATION:

{conversation_context if conversation_context else "None"}

CURRENT USER QUESTION:

{question}

RETRIEVED GOVERNMENT DOCUMENT CONTEXT:

{document_context}

INSTRUCTIONS:

1. Answer the current question using ONLY the
   retrieved government document context.

2. Use previous conversation only to understand
   references and follow-up questions.

3. Do not treat previous assistant responses
   as independent factual evidence.

4. Do not use general knowledge to add
   government rules or legal information.

5. Do not invent sections, procedures, fees,
   deadlines, eligibility conditions or authorities.

6. If the retrieved context does not contain
   enough information to answer the question,
   respond exactly:

{FALLBACK_RESPONSE}

7. Preserve important legal terminology.

8. Explain the answer clearly.

9. Do not claim that information comes from a
   section or page unless the retrieved context
   supports that attribution.
"""

        logger.info(
            "RAG prompt prepared."
        )

        # -------------------------------------------------
        # 9. INITIALIZE GEMINI CLIENT
        # -------------------------------------------------

        client = get_gemini_client()

        # -------------------------------------------------
        # 10. GENERATE GROUNDED ANSWER
        # -------------------------------------------------

        logger.info(
            "Answer generation started."
        )

        interaction = client.interactions.create(
            model=GENERATION_MODEL,
            system_instruction=SYSTEM_INSTRUCTION,
            input=prompt
        )

        logger.info(
            "Answer generation completed."
        )

        # -------------------------------------------------
        # 11. EXTRACT ANSWER
        # -------------------------------------------------

        answer = interaction.output_text

        if not isinstance(answer, str):

            raise RuntimeError(
                "Gemini returned an invalid answer."
            )

        answer = answer.strip()

        if not answer:

            raise RuntimeError(
                "Gemini returned an empty answer."
            )

        # -------------------------------------------------
        # 12. RETURN RESULT
        # -------------------------------------------------

        logger.info(
            "RAG request completed successfully."
        )

        return {
            "success": True,
            "answer": answer,
            "documents": documents
        }

    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    except Exception as e:

        logger.error(
            "RAG pipeline failed: %s",
            type(e).__name__
        )

        return {
            "success": False,
            "error": e
        }