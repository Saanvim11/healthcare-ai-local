from sentence_transformers import SentenceTransformer

# Load once when app starts
embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)