from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.app.api.patients import get_current_user
from backend.app.rag.retriever import MedicalRetriever
from src.nlp import MedicalNLP

router = APIRouter(prefix="/rag", tags=["RAG Retrieval"])

class RetrieveRequest(BaseModel):
    query: str
    k: int = 5

class RetrieveResponse(BaseModel):
    query: str
    enhanced_query: Optional[str] = None
    retrieved_chunks: List[str]
    total_chunks: int
    message: str

# Initialize components (singleton style)
retriever = MedicalRetriever()
nlp = MedicalNLP()

@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_medical_context(
    request: RetrieveRequest,
    current_user = Depends(get_current_user)
):
    try:
        # 1. Enhance query using Medical NLP
        enhanced_query, entities = nlp.enhance_query(request.query)
        
        # 2. Retrieve relevant medical context
        chunks = retriever.retrieve(enhanced_query, k=request.k)
        
        if not chunks:
            return RetrieveResponse(
                query=request.query,
                enhanced_query=enhanced_query,
                retrieved_chunks=[],
                total_chunks=0,
                message="No relevant medical documents found in the knowledge base."
            )
        
        return RetrieveResponse(
            query=request.query,
            enhanced_query=enhanced_query,
            retrieved_chunks=chunks,
            total_chunks=len(chunks),
            message="Successfully retrieved relevant medical context from knowledge base."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG retrieval failed: {str(e)}"
        )