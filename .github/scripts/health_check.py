#!/usr/bin/env python3
import os, json, subprocess, urllib.request, textwrap, sys

api_key = os.getenv("OPENAI_API_KEY", "")

def sh(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)

# Collect rollout + logs
try:
    backend_logs = sh("kubectl -n idea-board logs deploy/backend --tail=200")
except Exception as e:
    backend_logs = f"(failed to read backend logs) {e}"

try:
    frontend_logs = sh("kubectl -n idea-board logs deploy/frontend --tail=120")
except Exception as e:
    frontend_logs = f"(failed to read frontend logs) {e}"

try:
    pods = sh("kubectl -n idea-board get pods -o wide")
except Exception as e:
    pods = f"(failed to get pods) {e}"

# Deterministic “hard” checks first
hard_bad_signals = []
for s in ["Traceback", "ERROR", "Exception", "CrashLoopBackOff", "Back-off restarting failed container"]:
    if s in backend_logs or s in pods:
        hard_bad_signals.append(s)

if hard_bad_signals:
    print("Hard failure signals detected:", ", ".join(hard_bad_signals))
    print("Rolling back backend deployment...")
    try:
        print(sh("kubectl -n idea-board rollout undo deploy/backend"))
    except Exception as e:
        print("Rollback failed:", e)
    sys.exit(1)

# If no API key, just print a summary and exit
if not api_key:
    print("No OPENAI_API_KEY set. Skipping AI analysis.")
    print("Pods:\n", pods)
    sys.exit(0)

prompt = f"""
You are an SRE assistant. Analyze the Kubernetes deployment health based on the following.

Return ONLY strict JSON with:
{{
  "healthy": true/false,
  "summary": "<short human summary>",
  "suspected_root_cause": "<short>",
  "recommended_action": "<short>"
}}

Data:
--- PODS ---
{pods}

--- BACKEND LOGS ---
{backend_logs}

--- FRONTEND LOGS ---
{frontend_logs}
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
    with urllib.request.urlopen(req, timeout=45) as r:
        data = json.loads(r.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"].strip()
        result = json.loads(content)
except Exception as e:
    print("AI analysis failed, printing deterministic info only:", e)
    print("Pods:\n", pods)
    sys.exit(0)

print("AI Health Summary:", result.get("summary"))
print("Suspected Root Cause:", result.get("suspected_root_cause"))
print("Recommended Action:", result.get("recommended_action"))

if result.get("healthy") is False:
    print("AI thinks deployment is unhealthy. Rolling back backend...")
    try:
        print(sh("kubectl -n idea-board rollout undo deploy/backend"))
    except Exception as e:
        print("Rollback failed:", e)
        sys.exit(1)
    sys.exit(1)

sys.exit(0)