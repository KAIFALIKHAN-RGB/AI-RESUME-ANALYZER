"""
Extracts text content from PDF resume files.
"""

import PyPDF2


def extract_pdf_text(uploaded_file):
    """
    Extract all text from a PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        str: Extracted text, or empty string if extraction fails.
    """
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    except Exception as e:
        raise ValueError(f"Could not read PDF file: {e}") from e

    return text