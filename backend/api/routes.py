from fastapi import APIRouter
from backend.rag.pipeline import run_pipeline
from backend.translators.translator import translate

router = APIRouter()


@router.post("/ask")
def ask_question(payload: dict):
    user_query = payload.get("question")

    # Step 1: translate to English
    translated_query = translate(user_query, "English")

    # Step 2: run RAG
    result = run_pipeline(translated_query)

    # Step 3: translate back
    final_answer = translate(result["answer"], "original language")

    return {
        "answer": final_answer,
        "sources": result["sources"]
    }


@router.post("/v1/chat/completions")
def chat_completions(payload: dict):
    user_message = payload["messages"][-1]["content"]

    result = run_pipeline(user_message)

    return {
        "id": "chatcmpl-local",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result["answer"]
                },
                "finish_reason": "stop"
            }
        ]
    }

@router.get("/v1/models")
def get_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "local-rag",
                "object": "model",
                "owned_by": "local"
            }
        ]
    }