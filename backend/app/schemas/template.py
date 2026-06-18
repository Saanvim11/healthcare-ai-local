from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TemplateBase(BaseModel):
    name: str
    template_type: str
    content: str
    is_default: bool = False

class TemplateCreate(TemplateBase):
    created_by: Optional[int] = None

class TemplateResponse(TemplateBase):
    id: int
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True   # This is critical
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }