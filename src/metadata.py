import re


from src.config import DOCUMENT_TITLE


def detect_section(text):
    """
    Detect a section number and title from text.

    Example:
    86. Licensing of places for disposal of the dead
    """

    try:

        if not text or not text.strip():
            return {
                "section": None,
                "section_title": None
            }

        pattern = r"(?m)^\s*(\d+[A-Za-z]?)\.\s+([^\n]+)"

        match = re.search(
            pattern,
            text
        )

        if not match:
            return {
                "section": None,
                "section_title": None
            }

        section_number = match.group(1)

        section_title = match.group(2).strip()

        section_title = " ".join(
            section_title.split()
        )

        return {
            "section": section_number,
            "section_title": section_title
        }

    except Exception:

        return {
            "section": None,
            "section_title": None
        }