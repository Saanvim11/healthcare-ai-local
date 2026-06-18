import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.retrieval import MedicalRetriever
from src.nlp import MedicalNLP
from src.config import Config
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Initialize components
retriever = MedicalRetriever()
nlp = MedicalNLP()

TEMPERATURE = 0.3
NUM_CTX = 8192
LOCAL_OLLAMA_URL = "http://192.168.1.199:11434"

# Smart LLM initialization with fallback
def get_llm():
    for url in [LOCAL_OLLAMA_URL, Config.OLLAMA_BASE_URL]:
        try:
            llm = ChatOllama(
                base_url=url,
                model=Config.OLLAMA_MODEL,
                temperature=TEMPERATURE,
                num_ctx=NUM_CTX,
            )
            # Quick health check
            print(f" Connected to Ollama at {url}")
            return llm
        except Exception as e:
            print(f"  Failed to connect to {url}: {e}")
            continue
    raise ConnectionError("Could not connect to any Ollama server!")

llm = get_llm()

prompt = ChatPromptTemplate.from_template("""
You are an experienced, accurate medical assistant.
Use only the provided context to answer. Be concise, clear, and professional.
If the context doesn't have enough information, say so.

Context:
{context}

Question: {question}

Answer:
""")

def ask(question: str):
    print(f"\n Question: {question}")
    
    try:
        # NLP Enhancement
        enhanced, entities = nlp.enhance_query(question)
        print(f"   Entities: {entities}")
        
        # Retrieval
        docs, scores = retriever.retrieve(enhanced, k=4)
        context = "\n\n".join(docs)
        
        if not context.strip():
            print("    No relevant documents found.")
            context = "No relevant medical context available."
        
        # LLM Call with error handling
        response = llm.invoke(
            prompt.format(context=context, question=question)
        )
        
        print("\n Answer:")
        print(response.content)
        
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f" Trying to connect to Ollama...")
    ask("What is covid?")