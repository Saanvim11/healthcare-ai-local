import os
from backend.app.rag.retriever import MedicalRetriever

def ingest_medical_documents():
    print(" Starting Medical Document Ingestion for RAG...\n")
    
    retriever = MedicalRetriever()
    
    success = retriever.ingest_documents()
    
    if success:
        print("\n RAG Ingestion Completed Successfully!")
        print("You can now use semantic search in Phase 3.")
    else:
        print("\n  No documents found in knowledge_base folder.")
        print("Please add some medical PDFs into: ./data/knowledge_base/")

if __name__ == "__main__":
    ingest_medical_documents()