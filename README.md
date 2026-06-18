# 🏥 MedAI - Local Healthcare AI Assistant

A **privacy-first, locally hosted** AI-powered clinical decision support system designed for doctors and general users.

---

## 🚀 Features

### **Public Mode** (No Login Required)
- Ask general medical questions
- Get clear, easy-to-understand answers
- Practical precautions and advice

### **Doctor Mode** (Authenticated)
- Full clinical reasoning with SOAP notes
- Patient history awareness (Longitudinal Intelligence)
- Timeline of previous visits
- ICD code suggestions
- Red flag detection
- Verification & Safety Layer

### **Core Capabilities**
- **RAG-based** medical knowledge retrieval
- **Advanced Verification System** (Cross-Encoder + LLM Judge)
- **Hallucination Detection**
- **ICD Validation**
- **Safety Alerts** for emergency conditions
- **Patient Timeline & Encounter Management**

---

## 🛠 Tech Stack

- **Backend**: FastAPI + Python
- **AI Models**: Ollama (Local / Remote GPU)
- **Vector Database**: ChromaDB
- **Frontend**: Streamlit
- **Database**: SQLite
- **Authentication**: JWT

---

## 📁 Project Structure

```bash
healthcare-ai-local/
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── api/                 # API endpoints
│   │   ├── agents/              # Agent orchestration
│   │   ├── core/                # Configuration & security
│   │   ├── db/                  # Database connection
│   │   ├── models/              # Database models
│   │   ├── rag/                 # Retrieval pipeline
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── ...
│   ├── ingest.py
│   └── main.py
│
├── data/
│   └── knowledge_base/          # Medical PDFs
│
├── frontend/
│   └── app.py
│
├── streamlit_app.py             # Streamlit frontend
├── clinical.db                  # SQLite database
├── requirements.txt
├── .env                         # Environment variables
└── README.md
```


---

## 🧪 How to Run

### 1. Backend
```bash
cd healthcare-ai-local
python -m backend.main

2. Frontend
Bashstreamlit run streamlit_app.py

🔐 Login Credentials (Doctor Mode)

Username: user@example.com
Password: string

⚠️ Important Notes

This is a local, privacy-first system. No data leaves your machine.
AI-generated content is for assistance only. Final clinical decisions must be made by licensed physicians.
Best performance achieved with strong models like phi4:14b or BioMistral.


📈 Future Enhancements

Docker deployment
Better medical models (Meditron, BioMistral)
Mobile-friendly UI
PDF report generation
Multi-user support

Built with care for local healthcare AI experimentation
