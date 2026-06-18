import chromadb
from sentence_transformers import SentenceTransformer
from src.config import Config
import os
from tqdm import tqdm

class MedicalRetriever:
    def __init__(self):
        print("Loading embedding model...")
        self.embedder = SentenceTransformer(Config.EMBEDDING_MODEL)
        os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection("medical_knowledge")
        print(" Medical Retriever initialized")
    
    def ingest_documents(self, documents: list, metadatas: list = None):
        if not documents:
            print("No documents to ingest")
            return
        
        print(f"Generating embeddings for {len(documents)} chunks...")
        embeddings = self.embedder.encode(documents, show_progress_bar=True)
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas or [{} for _ in documents],
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        print(f" Successfully ingested {len(documents)} document chunks")
    
    def retrieve(self, query: str, k: int = 4):
        query_emb = self.embedder.encode([query])[0]
        results = self.collection.query(
            query_embeddings=[query_emb.tolist()],
            n_results=k
        )
        docs = results['documents'][0]
        metas = results.get('metadatas', [[]])[0]
        return docs, metas