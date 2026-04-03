import json
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from langchain_core.documents import Document
from langchain_community.vectorstores import Qdrant

from backend.config import QDRANT_URL, COLLECTION_NAME
from backend.rag.embeddings import get_embeddings


# -----------------------
# Load Data
# -----------------------

def load_quran(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for item in data:
        content = f"{item['text']} ({item['translation']})"

        metadata = {
            "type": "quran",
            "surah": item["surah"],
            "ayah": item["ayah"]
        }

        docs.append(Document(page_content=content, metadata=metadata))

    return docs


def load_hadith(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for item in data:
        content = item["text"]

        metadata = {
            "type": "hadith",
            "source": item["source"],
            "hadith_no": item["hadith_no"],
            "grade": item.get("grade", "unknown")
        }

        docs.append(Document(page_content=content, metadata=metadata))

    return docs


# -----------------------
# Create Collection
# -----------------------

def create_collection(client, embedding_dim):
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
            )
        )


# -----------------------
# Main Ingest
# -----------------------

def ingest():
    print("Loading data...")

    quran_docs = load_quran("data/quran/quran.json")
    hadith_docs = load_hadith("data/hadith/hadith.json")

    all_docs = quran_docs + hadith_docs

    print(f"Total documents: {len(all_docs)}")

    embeddings = get_embeddings()

    client = QdrantClient(url=QDRANT_URL)

    # Get embedding size dynamically
    sample_vector = embeddings.embed_query("test")
    embedding_dim = len(sample_vector)

    create_collection(client, embedding_dim)

    print("Uploading to Qdrant...")

    Qdrant.from_documents(
        documents=tqdm(all_docs),
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingest()