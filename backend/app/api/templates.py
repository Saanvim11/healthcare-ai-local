from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.template import Template
from backend.app.schemas.template import TemplateCreate, TemplateResponse
from typing import List

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.get("/", response_model=List[TemplateResponse])
def get_all_templates(db: Session = Depends(get_db)):
    templates = db.query(Template).all()
    return templates

@router.get("/defaults", response_model=List[TemplateResponse])
def get_default_templates(db: Session = Depends(get_db)):
    templates = db.query(Template).filter(Template.is_default == True).all()
    return templates

@router.post("/", response_model=TemplateResponse)
def create_custom_template(template: TemplateCreate, db: Session = Depends(get_db)):
    existing = db.query(Template).filter(Template.name == template.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Template name already exists")
    
    new_template = Template(**template.dict())
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@router.get("/test")
def test_templates():
    return {"message": "Templates API is working"}