
import fitz


def extract_pdf_text(file_path):

    document = fitz.open(file_path)

    pages = []

    try:
        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()

            pages.append({
                "page_number": page_number,
                "content": text
            })

    finally:
        document.close()

    return pages
