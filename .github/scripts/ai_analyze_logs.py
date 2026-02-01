#!/usr/bin/env python3
import os, sys, json
import urllib.request

env = sys.argv[1] if len(sys.argv) > 1 else "prod"
goal = sys.argv[2] if len(sys.argv) > 2 else "balanced"
api_key = os.getenv("OPENAI_API_KEY", "")

# Deterministic fallback
def fallback(env: str, goal: str) -> dict:
    if env == "prod" or goal == "ha":
        return {"BACKEND_REPLICAS": 2, "FRONTEND_REPLICAS": 2}
    if goal == "cost":
        return {"BACKEND_REPLICAS": 1, "FRONTEND_REPLICAS": 1}
    return {"BACKEND_REPLICAS": 2, "FRONTEND_REPLICAS": 2}

if not api_key:
    cfg = fallback(env, goal)
    print(f"BACKEND_REPLICAS={cfg['BACKEND_REPLICAS']}")
    print(f"FRONTEND_REPLICAS={cfg['FRONTEND_REPLICAS']}")
    sys.exit(0)

prompt = f"""
You are a DevOps assistant. Suggest replica counts for a small demo app on Kubernetes.

Inputs:
- environment: {env}
- goal: {goal} (cost|balanced|ha)

Rules:
- Return ONLY strict JSON: {{"backend_replicas": <int>, "frontend_replicas": <int>}}
- Use integers between 1 and 4
- Keep it simple and conservative.
"""

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Return only strict JSON. No markdown."},
        {"role": "user", "content": prompt},
    ],
    "temperature": 0.2,
}

req = urllib.request.Request(
    "https://api.openai.com/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"].strip()
        cfg = json.loads(content)
        b = int(cfg["backend_replicas"])
        f = int(cfg["frontend_replicas"])
        b = min(max(b, 1), 4)
        f = min(max(f, 1), 4)
        print(f"BACKEND_REPLICAS={b}")
        print(f"FRONTEND_REPLICAS={f}")
except Exception:
    cfg = fallback(env, goal)
    print(f"BACKEND_REPLICAS={cfg['BACKEND_REPLICAS']}")
    print(f"FRONTEND_REPLICAS={cfg['FRONTEND_REPLICAS']}")