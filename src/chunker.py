from src.metadata import (
    DOCUMENT_TITLE,
    detect_section
)


def chunk_pages(
    pages,
    source,
    chunk_size=1000,
    overlap=200
):
    """
    Split page-wise PDF text into smaller overlapping chunks.

    Each chunk contains:
    - text
    - source document
    - document title
    - page number
    - chunk ID
    - section number
    - section title

    Section information is inherited by following chunks
    until another section heading is detected.
    """

    try:

        # -------------------------------------------------
        # INPUT VALIDATION
        # -------------------------------------------------

        if not pages:
            raise ValueError(
                "No pages were provided for chunking."
            )

        if not source:
            raise ValueError(
                "Source document name was not provided."
            )

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative."
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )


        # -------------------------------------------------
        # INITIAL VARIABLES
        # -------------------------------------------------

        chunks = []

        chunk_id = 1

        current_section = None
        current_section_title = None


        # -------------------------------------------------
        # PROCESS EACH PDF PAGE
        # -------------------------------------------------

        for page in pages:

            page_number = page["page_number"]

            text = page["text"]


            # Skip pages with no usable text
            if not text or not text.strip():
                continue


            text = text.strip()

            text_length = len(text)

            start = 0


            # ---------------------------------------------
            # CREATE CHUNKS FROM CURRENT PAGE
            # ---------------------------------------------

            while start < text_length:

                end = start + chunk_size

                chunk_text = text[
                    start:end
                ].strip()


                if chunk_text:

                    # -------------------------------------
                    # DETECT SECTION
                    # -------------------------------------

                    section_info = detect_section(
                        chunk_text
                    )


                    # If a new section is detected,
                    # remember it.
                    if (
                        section_info["section"]
                        is not None
                    ):

                        current_section = (
                            section_info["section"]
                        )

                        current_section_title = (
                            section_info[
                                "section_title"
                            ]
                        )


                    # -------------------------------------
                    # CREATE METADATA
                    # -------------------------------------

                    metadata = {

                        "source": source,

                        "document_title":
                            DOCUMENT_TITLE,

                        "page_number":
                            page_number,

                        "chunk_id":
                            chunk_id,

                        "section":
                            current_section,

                        "section_title":
                            current_section_title
                    }


                    # -------------------------------------
                    # STORE CHUNK
                    # -------------------------------------

                    chunks.append(
                        {
                            "text": chunk_text,
                            "metadata": metadata
                        }
                    )


                    chunk_id += 1


                # -----------------------------------------
                # MOVE TO NEXT CHUNK
                # -----------------------------------------

                start = end - overlap


        # -------------------------------------------------
        # RETURN RESULT
        # -------------------------------------------------

        return {
            "success": True,
            "chunks": chunks,
            "count": len(chunks)
        }


    except Exception as e:

        return {
            "success": False,
            "error": e
        }