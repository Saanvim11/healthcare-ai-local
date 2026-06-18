from backend.app.rag.retriever import MedicalRetriever
from src.nlp import MedicalNLP
from backend.app.agents.orchestrator import MedicalOrchestrator

# Initialize components
retriever = MedicalRetriever()
nlp = MedicalNLP()
orchestrator = MedicalOrchestrator()

def test_retrieval():
    print("🔍 TESTING BASIC RETRIEVAL + NLP\n")
    test_queries = [
        "What are symptoms of diabetic neuropathy?",
        "What is the definition of hypertension?",
        "What are global health statistics about diabetes?",
        "Signs of pneumonia on examination"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        print('='*60)
        
        enhanced, entities = nlp.enhance_query(query)
        print(f"Entities: {entities}")
        
        results = retriever.retrieve(enhanced, k=4)
        print(f"Retrieved {len(results)} chunks")
        for i, chunk in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(chunk[:400] + "..." if len(chunk) > 400 else chunk)

def test_phase5_orchestrator():
    print("\n🚀 PHASE 5 - AGENTIC ORCHESTRATION TEST\n")
    
    test_queries = [
        "What are symptoms of diabetic neuropathy?",
        "What is the definition of hypertension?",
        "Patient has high blood pressure and severe headache",
        "Signs of pneumonia on examination"
    ]
    
    for query in test_queries:
        print("=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        
        result = orchestrator.process(query)
        
        print(f"Enhanced Query : {result.get('enhanced_query')}")
        print(f"Entities       : {result.get('entities')}")
        print(f"Used RAG       : {result.get('use_rag')}")
        print(f"Context Length : {len(result.get('context', ''))} characters")
        print("\n")

if __name__ == "__main__":
    test_retrieval()
    test_phase5_orchestrator()