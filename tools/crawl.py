from typing import List

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document


def crawl_data(urls: List[str]) -> List[Document] :
    docs = []

    for url in urls:
        try:
            loader = WebBaseLoader(
                web_paths=(url,),
            )
            doc = loader.load()
            docs.extend(doc)
            print(f"Successfully loaded: {url}")
        except Exception as e:
            print(f"Error loading {url}: {str(e)}")

    return docs