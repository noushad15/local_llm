import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "islamic_docs")

# Embedding model configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# LLM configuration
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
MODEL_NAME = os.getenv("MODEL_NAME",  "llama3")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama_l:11434")