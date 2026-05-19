#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

log() {
  printf "[observability-gate] %s\n" "$1"
}

cleanup() {
  docker compose down -v >/dev/null 2>&1 || true
}
trap cleanup EXIT

wait_for_http() {
  local name="$1"
  local url="$2"
  local max_attempts="${3:-45}"
  local attempt=1

  until curl -fsS "$url" >/dev/null 2>&1; do
    if (( attempt >= max_attempts )); then
      echo "$name not ready: $url" >&2
      docker compose ps >&2 || true
      docker compose logs --tail=120 >&2 || true
      exit 1
    fi
    sleep 2
    attempt=$((attempt + 1))
  done
  log "$name ready"
}

log "starting docker compose platform"
mkdir -p approval-service/data
test -f approval-service/data/approvals.json || printf '[]\n' > approval-service/data/approvals.json
chmod -R 777 approval-service/data
docker compose up -d --build

wait_for_http "agent-api" "http://localhost:8010/health"
wait_for_http "llm-gateway" "http://localhost:8001/health"
wait_for_http "prometheus" "http://localhost:9090/-/ready"
wait_for_http "grafana" "http://localhost:3000/api/health"
wait_for_http "ingress" "http://127.0.0.1:8080/health"

log "running smoke workflow"
python3 scripts/platform_smoke_test.py

log "running incident simulation"
python3 scripts/simulate_incident.py

log "validating Prometheus targets and metric signals"
python3 - <<'PY'
import json
import urllib.parse
import urllib.request


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.load(response)


targets = fetch_json("http://localhost:9090/api/v1/targets")
active = targets.get("data", {}).get("activeTargets", [])
required_jobs = {"agent-api", "llm-gateway"}
healthy_jobs = {target.get("labels", {}).get("job") for target in active if target.get("health") == "up"}
missing = sorted(required_jobs - healthy_jobs)
if missing:
    raise SystemExit(f"missing healthy Prometheus targets: {missing}")

queries = {
    "agent_requests_total": "sum(increase(agent_requests_total[10m]))",
    "guardrail_blocks_total": "sum(increase(guardrail_blocks_total[10m]))",
    "llm_gateway_fallbacks_total": "sum(increase(llm_gateway_fallbacks_total[10m]))",
    "approval_queue_depth": "approval_queue_depth",
}

for name, query in queries.items():
    url = "http://localhost:9090/api/v1/query?" + urllib.parse.urlencode({"query": query})
    payload = fetch_json(url)
    results = payload.get("data", {}).get("result", [])
    value = float(results[0]["value"][1]) if results else 0.0
    print(f"{name}={value}")
    if name != "approval_queue_depth" and value <= 0:
        raise SystemExit(f"metric did not move: {name}")

print("observability gate passed")
PY

log "validating Grafana provisioned dashboard"
python3 - <<'PY'
import json
import urllib.request

request = urllib.request.Request("http://localhost:3000/api/search")
credentials = "admin:admin".encode()
import base64
request.add_header("Authorization", "Basic " + base64.b64encode(credentials).decode())
with urllib.request.urlopen(request, timeout=10) as response:
    dashboards = json.load(response)

titles = {item.get("title") for item in dashboards}
expected = "HelixCare AI Governance & Reliability Operations"
if expected not in titles:
    raise SystemExit(f"Grafana dashboard missing: {expected}")
print("grafana_dashboard=provisioned")
PY

log "observability gate complete"
