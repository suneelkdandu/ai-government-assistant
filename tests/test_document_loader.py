from src.document_loader import load_pdf


def test_document_loader():

    result = load_pdf(
        "data/APPR_ACT_1994.pdf"
    )

    if not result["success"]:
        print("\nPDF loading failed.")
        print(result["error"])
        return

    print("\nPDF loaded successfully.")

    print(
        "File:",
        result["file_name"]
    )

    print(
        "Total PDF pages:",
        result["total_pdf_pages"]
    )

    print(
        "Pages containing text:",
        len(result["pages"])
    )

    if result["pages"]:

        first_page = result["pages"][0]

        print("\nFirst extracted page:")
        print(
            "Page number:",
            first_page["page_number"]
        )

        print("\nText preview:")
        print(
            first_page["text"][:1000]
        )


if __name__ == "__main__":
    test_document_loader()