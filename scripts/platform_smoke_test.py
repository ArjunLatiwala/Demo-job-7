import json
import sys

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8010"

checks = [
    ("health", "GET", f"{BASE}/health", None),
    ("system-status", "GET", f"{BASE}/system-status", None),
    (
        "safe-agent-request",
        "POST",
        f"{BASE}/run-agent",
        {"message": "Summarize the claims escalation workflow for operations staff."},
    ),
    (
        "governed-agent-request",
        "POST",
        f"{BASE}/run-agent",
        {"message": "Can you diagnose this patient and prescribe medication?"},
    ),
]

for name, method, url, payload in checks:
    response = requests.request(method, url, json=payload, timeout=12)
    print(json.dumps({"check": name, "status_code": response.status_code, "passed": response.ok}))
    response.raise_for_status()
