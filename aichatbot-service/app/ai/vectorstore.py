from langchain_chroma import Chroma
from .embedding import get_embeddings
import os

_vectorstore = None


def get_vectorstore():
    global _vectorstore

    if _vectorstore is None:

        chroma_path = os.path.join(os.getcwd(), "chroma_db")

        print(f"⚡ Loading Chroma DB from: {chroma_path}")

        _vectorstore = Chroma(
            collection_name="products",
            persist_directory=chroma_path,
            embedding_function=get_embeddings(),
            collection_metadata={"hnsw:space": "cosine"}
        )

    return _vectorstore