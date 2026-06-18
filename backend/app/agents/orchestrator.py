from typing import Dict, Any
from src.nlp import MedicalNLP
from backend.app.rag.retriever import MedicalRetriever

class MedicalOrchestrator:
    def __init__(self):
        self.nlp = MedicalNLP()
        self.retriever = MedicalRetriever()

    def process(self, query: str) -> Dict[str, Any]:
        """Phase 5 - Agentic Orchestrator"""
        
        # NLP Enhancement
        enhanced_query, entities = self.nlp.enhance_query(query)
        
        # Routing Decision
        lower_query = query.lower()
        use_rag = (
            len(entities.get('Disease_disorder', [])) > 0 or
            any(word in lower_query for word in ["symptoms", "signs", "causes", "what is", "definition", "treatment", "hypertension"])
        )
        
        # Retrieve context safely
        context = ""
        if use_rag:
            result = self.retriever.retrieve(enhanced_query, k=5)
            # Handle different possible return formats
            if isinstance(result, tuple) and len(result) >= 2:
                docs = result[0] if isinstance(result[0], list) else result[0]
            else:
                docs = result if isinstance(result, list) else []
            
            context = "\n\n".join(docs[:4]) if docs else ""

        print(f"🔀 Orchestrator Decision:")
        print(f"   Query       : {query}")
        print(f"   Entities    : {entities}")
        print(f"   Use RAG     : {use_rag}")
        print(f"   Context Len : {len(context)} chars")
        
        return {
            "original_query": query,
            "enhanced_query": enhanced_query,
            "entities": entities,
            "use_rag": use_rag,
            "context": context
        }