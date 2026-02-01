from pydantic import BaseModel
from datetime import datetime

class IdeaCreate(BaseModel):
    content: str

class IdeaOut(BaseModel):
    id: int
    content: str
    created_at: datetime

    # Pydantic v2 replacement for orm_mode = True
    model_config = {"from_attributes": True}