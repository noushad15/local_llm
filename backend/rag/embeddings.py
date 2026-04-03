from langchain_community.embeddings import OllamaEmbeddings
import os

def get_embeddings():
    return OllamaEmbeddings(
        model="llama3",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://ollama_l:11434")
    )