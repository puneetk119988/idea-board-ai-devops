#!/usr/bin/env python3
import os, sys, json, textwrap
import urllib.request

env_name = sys.argv[1] if len(sys.argv) > 1 else "prod"
api_key = os.getenv("OPENAI_API_KEY", "")

# Fallback plan if no API key configured (keeps repo runnable)
# IMPORTANT: must match your actual repo filenames and service names.
fallback = textwrap.dedent(f"""#!/usr/bin/env bash
set -euo pipefail
echo "Deploying to environment: {env_name}"

kubectl get ns idea-board >/dev/null 2>&1 || kubectl apply -f k8s/namespace.yaml

kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/backend-deployment.yaml

kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

echo "Done. Check service:"
kubectl -n idea-board get svc frontend-svc
""")

if not api_key:
    print(fallback)
    sys.exit(0)

prompt = f"""You are a DevOps assistant. Generate a SAFE bash script that deploys Kubernetes manifests for the Idea Board app.
Constraints:
- Only use kubectl commands and apply local yaml files under k8s/
- Use namespace idea-board
- Must be idempotent
- Must NOT delete resources
Environment: {env_name}
Return only bash script content.
"""
payload = {
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "Return ONLY bash script. No markdown."},
    {"role": "user", "content": prompt}
  ],
  "temperature": 0.2
}

req = urllib.request.Request(
    "https://api.openai.com/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
        script = data["choices"][0]["message"]["content"]

        # Minimal hardening: ensure it looks like a bash script and uses kubectl
        if "kubectl" not in script:
            print(fallback)
        else:
            print(script)
except Exception:
    print(fallback)
