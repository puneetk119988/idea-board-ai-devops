#!/usr/bin/env python3
import os, json, subprocess, urllib.request, textwrap, sys

api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key:
    print("No OPENAI_API_KEY set; skipping AI log analysis.")
    sys.exit(0)

def sh(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True)

# Grab recent logs
backend_pods = sh("kubectl -n idea-board get pods -l app=backend -o name").strip().splitlines()
if not backend_pods:
    print("No backend pods found.")
    sys.exit(0)

logs = ""
for p in backend_pods[:2]:
    logs += f"\n=== {p} ===\n"
    logs += sh(f"kubectl -n idea-board logs {p} --tail=200")

prompt = textwrap.dedent(f"""Analyze these Kubernetes application logs and decide if deployment is healthy.
Return JSON with keys:
- status: HEALTHY or ROLLBACK
- summary: short human summary
- evidence: list of 2-5 bullet strings referencing log patterns

LOGS:
{logs}
""")

payload = {
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "Return ONLY JSON. No markdown."},
    {"role": "user", "content": prompt}
  ],
  "temperature": 0.2
}

req = urllib.request.Request(
    "https://api.openai.com/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode("utf-8"))
    txt = data["choices"][0]["message"]["content"]

result = json.loads(txt)
print("AI_STATUS:", result.get("status"))
print("AI_SUMMARY:", result.get("summary"))

if result.get("status") == "ROLLBACK":
    print("Triggering rollback for backend…")
    subprocess.check_call("kubectl -n idea-board rollout undo deploy/backend", shell=True)
