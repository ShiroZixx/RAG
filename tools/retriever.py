from models.llms import embedding_model
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.tools.retriever import create_retriever_tool


def create_retriever_tool_from_docs(docs: List[Document]):
    """
    Create retriever tool
    Combine FAISS (semantic) and BM25 (keyword)

    Returns:
        retriever_tool
    """


    # FAISS semantic retriever
    vectordb = FAISS.from_documents(docs, embedding_model)
    faiss_retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )


    # BM25 keyword retriever
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = 5


    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.4, 0.6],
    )


    # Create tool
    retriever_tool = create_retriever_tool(
        retriever=hybrid_retriever,
        name="retrieve_plant_disease",
        description="Tìm kiếm thông tin về các loại bệnh trên cây lúa theo truy vấn người dùng."
    )

    return retriever_tool

