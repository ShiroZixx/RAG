import PyPDF2


def read_pdf(pdf_path: str, method: str = "pypdf2") -> str:
    """
    Read PDF file and extract text content

    Args:
        pdf_path: Path to the PDF file
        method: Method to use ('pypdf2' or 'pymupdf')

    Returns:
        Extracted text content
    """
    text = ""

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF with PyPDF2: {str(e)}")

    return text.strip()