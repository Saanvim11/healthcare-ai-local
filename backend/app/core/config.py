from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Healthcare AI Assistant"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./clinical.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "meditron"
    OLLAMA_TEMPERATURE: float = 0.3
    OLLAMA_NUM_CTX: int = 8192
    
    # Embedding & RAG
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    VECTOR_DB_PATH: str = "./data/vector_db"
    KB_PATH: str = "./data/knowledge_base"
    
    # Local fallback
    LOCAL_OLLAMA_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()