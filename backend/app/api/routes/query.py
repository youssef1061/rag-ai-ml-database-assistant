from fastapi import APIRouter, HTTPException, Request
from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import RetrievalService

router = APIRouter(tags=["RAG"])

@router.get("/health")
def health(request: Request):
    return {"status": "ok", "vector_store_loaded": hasattr(request.app.state, "retrieval")}

@router.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest, request: Request):
    try:
        chunks = request.app.state.retrieval.retrieve(payload.question)
        answer = request.app.state.generation.answer(payload.question, chunks)
        sources = list(dict.fromkeys(RetrievalService.source_label(chunk["metadata"]) for chunk in chunks))
        return QueryResponse(answer=answer, sources=sources)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"RAG service unavailable: {exc}") from exc
