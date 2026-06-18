from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from backend.app.rag.config import RAGConfig
import os

class MedicalRetriever:
    def __init__(self):
        self.config = RAGConfig()
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None
        self.index_path = os.path.join(self.config.vector_db_path, "faiss_index")

    def ingest_documents(self):
        if not os.path.exists(self.config.knowledge_base_path):
            os.makedirs(self.config.knowledge_base_path)
            print(f"📁 Created folder: {self.config.knowledge_base_path}")
            print("Please add medical PDFs inside this folder.")
            return False

        print("📄 Loading documents...")
        loader = PyPDFDirectoryLoader(self.config.knowledge_base_path)
        documents = loader.load()

        print("📝 Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents)

        print(f"🔄 Creating FAISS index with {len(chunks)} chunks...")
        self.vector_db = FAISS.from_documents(chunks, self.embeddings)
        
        # Save index
        os.makedirs(self.config.vector_db_path, exist_ok=True)
        self.vector_db.save_local(self.index_path)
        
        print(f"✅ Successfully ingested {len(chunks)} chunks using FAISS!")
        return True

    def retrieve(self, query: str, k: int = 5):
        """Retrieve relevant chunks using FAISS"""
        if not self.vector_db:
            self.vector_db = FAISS.load_local(
                self.index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        
        results = self.vector_db.similarity_search(query, k=k)
        
        # Simple deduplication
        seen = set()
        unique = []
        for doc in results:
            sig = doc.page_content[:150].strip().lower()
            if sig not in seen:
                seen.add(sig)
                unique.append(doc.page_content)
                if len(unique) >= k:
                    break
        return unique