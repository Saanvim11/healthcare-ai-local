from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.db.database import engine, Base, SessionLocal
from backend.app.api.patients import get_current_user
from backend.app.api.clinical import router as clinical_router
from backend.app.api.coding import router as coding_router
from backend.app.api.integrated import router as integrated_router
from backend.app.api.clinical_forms import router as clinical_forms_router
from backend.app.api.rag import router as rag_router
from backend.app.agents.orchestrator import MedicalOrchestrator
from backend.app.api.routes.verification import router as verification_router
from backend.app.api.encounters import router as encounters_router
from backend.app.api.timeline import router as timeline_router

import backend.app.models.user
import backend.app.models.patient
import backend.app.models.encounter
import backend.app.models.template

orchestrator = MedicalOrchestrator()   

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Local Privacy-First Healthcare AI Assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
from backend.app.api.auth import router as auth_router
from backend.app.api.patients import router as patients_router
from backend.app.api.templates import router as templates_router

app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(templates_router)
app.include_router(clinical_router)
app.include_router(coding_router)
app.include_router(integrated_router)
app.include_router(clinical_forms_router)
app.include_router(rag_router)
app.include_router(verification_router)
app.include_router(encounters_router)
app.include_router(timeline_router)

# Seed default templates
def seed_default_templates():
    db = SessionLocal()
    try:
        from backend.app.core.templates_data import DEFAULT_TEMPLATES
        from backend.app.models.template import Template
        
        for temp in DEFAULT_TEMPLATES:
            existing = db.query(Template).filter(Template.name == temp["name"]).first()
            if not existing:
                template = Template(**temp)
                db.add(template)
        db.commit()
        print("✅ Default templates seeded successfully!")
    finally:
        db.close()

seed_default_templates()

@app.get("/")
async def root():
    return {
        "message": "🏥 Healthcare AI System is Running",
        "status": "active",
        "version": "0.1.0"
    }

@app.get("/test-auth")
async def test_auth(current_user = Depends(get_current_user)):
    return {
        "message": "Authentication works!",
        "user": {
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)