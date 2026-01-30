from pydantic import BaseModel, Field
from datetime import datetime

class IdeaCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

class IdeaOut(BaseModel):
    id: int
    content: str
    created_at: datetime
