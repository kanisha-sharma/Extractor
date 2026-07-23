import fitz


def extract_pdf_metadata(pdf_path: str):

    document = fitz.open(pdf_path)

    metadata = document.metadata

    result = {

        "title": metadata.get("title"),

        "author": metadata.get("author"),

        "subject": metadata.get("subject"),

        "creator": metadata.get("creator"),

        "producer": metadata.get("producer"),

        "total_pages": document.page_count

    }

    document.close()

    return result