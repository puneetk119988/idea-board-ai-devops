import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import Base, engine, get_db
from .models import Idea
from .schemas import IdeaCreate, IdeaOut

# Create tables (simple approach for case study; production would use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Idea Board API")

cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/ideas", response_model=list[IdeaOut])
def list_ideas(db: Session = Depends(get_db)):
    ideas = db.execute(select(Idea).order_by(Idea.created_at.desc())).scalars().all()
    return ideas

@app.post("/api/ideas", response_model=IdeaOut)
def create_idea(payload: IdeaCreate, db: Session = Depends(get_db)):
    idea = Idea(content=payload.content)
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return idea
