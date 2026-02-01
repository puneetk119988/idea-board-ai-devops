import os
import time
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

# -----------------------------
# Config
# -----------------------------
def build_database_url() -> str:
    """
    Prefer DATABASE_URL (recommended).
    Fallback to DB_* env vars (matches your Kubernetes Secret style).
    """
    url = os.getenv("DATABASE_URL")
    if url and url.strip():
        return url.strip()

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASSWORD")

    missing = [k for k, v in {
        "DB_HOST": host,
        "DB_NAME": name,
        "DB_USER": user,
        "DB_PASSWORD": pwd,
    }.items() if not v]

    if missing:
        raise RuntimeError(
            f"Missing database environment variables: {', '.join(missing)}. "
            "Set DATABASE_URL or DB_HOST/DB_NAME/DB_USER/DB_PASSWORD."
        )

    # psycopg (v3) driver URL form:
    # postgresql+psycopg://user:pass@host:port/db
    return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{name}"


DATABASE_URL = build_database_url()

# SQLAlchemy 2.x engine/session
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


# -----------------------------
# Models
# -----------------------------
class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# -----------------------------
# Pydantic Schemas
# -----------------------------
class IdeaCreate(BaseModel):
    content: str


class IdeaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy -> Pydantic
    id: int
    content: str
    created_at: datetime


# -----------------------------
# DB Wait + Init
# -----------------------------
def wait_for_db(retries: int = 30, delay_seconds: int = 2) -> None:
    last_err = None
    for i in range(1, retries + 1):
        try:
            print(f"⏳ Waiting for DB... attempt {i}/{retries}", flush=True)
            with engine.connect() as conn:
                # ✅ SQLAlchemy 2.x requires text()
                conn.execute(text("SELECT 1"))
            print("✅ DB reachable", flush=True)
            return
        except Exception as e:
            last_err = e
            print(f"❌ DB connect failed (attempt {i}): {repr(e)}", flush=True)
            time.sleep(delay_seconds)

    raise RuntimeError(
        f"❌ Database not reachable after {retries} attempts. Last error: {repr(last_err)}"
    )


def init_db() -> None:
    # Create tables if not present
    Base.metadata.create_all(bind=engine)


# -----------------------------
# App
# -----------------------------
app = FastAPI()

# Allow frontend (nginx/react) to call backend
# In production, restrict origins to your ALB domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Wait DB then init schema
    wait_for_db(retries=30, delay_seconds=2)
    init_db()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/ideas", response_model=List[IdeaOut])
def list_ideas():
    with SessionLocal() as db:
        ideas = db.query(Idea).order_by(Idea.id.desc()).all()
        return ideas


@app.post("/api/ideas", response_model=IdeaOut)
def create_idea(payload: IdeaCreate):
    content = (payload.content or "").strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")

    with SessionLocal() as db:
        idea = Idea(content=content)
        db.add(idea)
        db.commit()
        db.refresh(idea)
        return idea