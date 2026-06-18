from src.retrieval import MedicalRetriever
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from src.config import Config

def ingest_knowledge_base():
    retriever = MedicalRetriever()
    
    kb_path = Config.KB_PATH
    if not os.path.exists(kb_path) or len(os.listdir(kb_path)) == 0:
        print("  No files found in data/knowledge_base/")
        print("Please put some medical PDF files in that folder and run again.")
        return
    
    print(f"Found {len(os.listdir(kb_path))} file(s) in knowledge base...")
    loader = PyPDFDirectoryLoader(kb_path)
    docs = loader.load()
    
    print(f"Loaded {len(docs)} documents. Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)
    
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [{"source": chunk.metadata.get("source", "unknown")} for chunk in chunks]
    
    retriever.ingest_documents(texts, metadatas)
    print("\n Knowledge Base Ingestion Completed Successfully!")

if __name__ == "__main__":
    ingest_knowledge_base()