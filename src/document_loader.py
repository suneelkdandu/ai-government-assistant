from pathlib import Path

from pypdf import PdfReader


def load_pdf(file_path):
    """
    Load a PDF and extract text page by page.
    """

    try:
        pdf_path = Path(file_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        reader = PdfReader(pdf_path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):
            text = page.extract_text()

            if text and text.strip():
                pages.append(
                    {
                        "page_number": page_number,
                        "text": text.strip()
                    }
                )

        return {
            "success": True,
            "file_name": pdf_path.name,
            "total_pdf_pages": len(reader.pages),
            "pages": pages
        }

    except Exception as e:

        return {
            "success": False,
            "error": e
        }