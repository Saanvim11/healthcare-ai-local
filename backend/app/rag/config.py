from pydantic import BaseModel

class RAGConfig(BaseModel):
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    vector_db_path: str = "./data/vector_db"
    knowledge_base_path: str = "./data/knowledge_base"
    chunk_size: int = 800
    chunk_overlap: int = 100