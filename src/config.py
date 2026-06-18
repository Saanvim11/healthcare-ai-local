import os
from dotenv import load_dotenv

load_dotenv()   # Load .env file

class Config:
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
    OLLAMA_MODEL = "phi4:14b"
    VECTOR_DB_PATH = "./data/vector_db"
    KB_PATH = "./data/knowledge_base"
    OLLAMA_BASE_URL = "http://192.168.1.199:11434"