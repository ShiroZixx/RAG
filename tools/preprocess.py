from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import unicodedata
from langchain.schema import Document
from typing import List

def clean_text(texts: List[Document]) -> List[Document]:
    """
    Args:
        text: Raw text to clean

    Returns:
        Cleaned text
    """
    cleaned_documents =[]

    for doc in texts:
        text = doc.page_content

        # Normalize Unicode characters
        text = unicodedata.normalize('NFC', text)

        # Remove all newline characters
        text = text.replace('\n', ' ').replace('\r', ' ')

        # Replace tab characters
        text = text.replace('\t', ' ')

        # Remove excessive punctuation repetitions
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)


        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        # Remove common web artifacts
        text = re.sub(r'Cookie.*?Accept', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Skip to.*?content', '', text, flags=re.IGNORECASE)

        # Strip leading and trailing spaces
        text = text.strip()

        doc.page_content = text

        cleaned_documents.append(doc)

    return cleaned_documents


def splitter(docs: List[Document], chunk_size: int = 700, chunk_overlap: int = 150) -> List[Document]:
    """
        List of split document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",  # Paragraph breaks
            "\n",  # Line breaks
            ".",  # Sentence endings
            "!",  # Exclamation endings
            "?",  # Question endings
            ";",  # Semicolon breaks
            ",",  # Comma breaks (last resort)
            " ",  # Space breaks (very last resort)
        ]
    )

    docs_splits = text_splitter.split_documents(docs)
    return docs_splits