from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest
from app.ai.rag_engine import ask

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(request: ChatRequest):

    try:
        result = ask(request.message)

        return {
            "answer": result["answer"],
            "matched_products": result["matched_products"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )