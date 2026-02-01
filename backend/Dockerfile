FROM python:3.11-slim

WORKDIR /app

# System deps (safe defaults; psycopg3 wheels usually work without pg-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app ./app

EXPOSE 8000

# FastAPI entrypoint (your app lives at backend/app/main.py -> app.main:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
