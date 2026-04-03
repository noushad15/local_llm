from backend.rag.retriever import get_retriever
from backend.rag.generator import generate_answer


def run_pipeline(query):
    retriever = get_retriever()

    docs = retriever.get_relevant_documents(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    answer = generate_answer(context, query)

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs]
    }