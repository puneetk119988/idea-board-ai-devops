#!/usr/bin/env python3
import subprocess, sys

def sh(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True).strip()

try:
    # Simple rollout checks
    sh("kubectl -n idea-board rollout status deploy/backend --timeout=120s")
    sh("kubectl -n idea-board rollout status deploy/frontend --timeout=120s")
    print("✅ Rollout healthy")
except subprocess.CalledProcessError as e:
    print("❌ Health check failed")
    print(e.output)
    sys.exit(1)
