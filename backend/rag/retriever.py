from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from backend.config import QDRANT_URL, COLLECTION_NAME
from backend.rag.embeddings import get_embeddings


def get_retriever():
    client = QdrantClient(url=QDRANT_URL)

    vectorstore = Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=get_embeddings()
    )

    return vectorstore.as_retriever(search_kwargs={"k": 5})