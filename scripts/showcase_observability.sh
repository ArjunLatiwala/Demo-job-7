#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DASHBOARD_URL="http://localhost:3000/d/healthcare-ai-governance/helixcare-ai-governance-and-reliability-operations?orgId=1&refresh=2s&from=now-10m&to=now"
PROM_TARGETS_URL="http://localhost:9090/targets"
PROM_GRAPH_REQUESTS="http://localhost:9090/graph?g0.expr=sum(rate(agent_requests_total%5B30s%5D))&g0.tab=0"
PROM_GRAPH_GUARDRAILS="http://localhost:9090/graph?g0.expr=sum(increase(guardrail_blocks_total%5B5m%5D))&g0.tab=0"
PROM_GRAPH_FALLBACKS="http://localhost:9090/graph?g0.expr=sum(increase(llm_gateway_fallbacks_total%5B5m%5D))&g0.tab=0"
PROM_GRAPH_APPROVALS="http://localhost:9090/graph?g0.expr=approval_queue_depth&g0.tab=0"

cd "$ROOT_DIR"

log() {
  printf "\033[1;36m[%s]\033[0m %s\n" "$(date +%H:%M:%S)" "$1"
}

warn() {
  printf "\033[1;33m[%s]\033[0m %s\n" "$(date +%H:%M:%S)" "$1"
}

fail() {
  printf "\033[1;31m[%s]\033[0m %s\n" "$(date +%H:%M:%S)" "$1" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

open_url() {
  local url="$1"
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 || warn "Could not auto-open: $url"
  else
    warn "Open manually: $url"
  fi
}

wait_for_http() {
  local name="$1"
  local url="$2"
  local max_attempts="${3:-30}"
  local attempt=1

  until curl -fsS "$url" >/dev/null 2>&1; do
    if (( attempt >= max_attempts )); then
      fail "$name not ready after $max_attempts attempts: $url"
    fi
    sleep 2
    attempt=$((attempt + 1))
  done
  log "$name ready"
}

cleanup() {
  if [[ -n "${TRAFFIC_PID:-}" ]] && kill -0 "$TRAFFIC_PID" >/dev/null 2>&1; then
    kill "$TRAFFIC_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

require_cmd docker
require_cmd curl
require_cmd python3

log "Building and starting Healthcare AI Governance platform"
docker compose up -d --build

log "Waiting for services"
wait_for_http "Agent API" "http://localhost:8010/health" 45
wait_for_http "LLM Gateway" "http://localhost:8001/health" 45
wait_for_http "Prometheus" "http://localhost:9090/-/ready" 45
wait_for_http "Grafana" "http://localhost:3000/api/health" 45
wait_for_http "Ingress" "http://127.0.0.1:8080/health" 20

log "Container status"
docker compose ps

log "Health evidence"
printf "Ingress: "
curl -4 -fsS http://127.0.0.1:8080/health
printf "\nAgent API: "
curl -fsS http://localhost:8010/health
printf "\nLLM Gateway: "
curl -fsS http://localhost:8001/health
printf "\nPrometheus: "
curl -fsS http://localhost:9090/-/ready
printf "\n"

log "Opening Prometheus evidence views"
open_url "$PROM_TARGETS_URL"
open_url "$PROM_GRAPH_REQUESTS"
open_url "$PROM_GRAPH_GUARDRAILS"
open_url "$PROM_GRAPH_FALLBACKS"
open_url "$PROM_GRAPH_APPROVALS"

log "Opening polished Grafana dashboard"
open_url "$DASHBOARD_URL"
log "Grafana login if prompted: admin / admin"

log "Running platform smoke test"
python3 scripts/demo_smoke_test.py

log "Starting live traffic simulation in background"
python3 scripts/generate_traffic.py &
TRAFFIC_PID=$!

log "Waiting for Prometheus/Grafana samples"
sleep 12

log "Running governance incident simulation"
python3 scripts/simulate_incident.py

log "Running live operations showcase"
bash scripts/live_ops_showcase.sh

log "Prometheus target summary"
python3 - <<'PY'
import json
import urllib.request

with urllib.request.urlopen("http://localhost:9090/api/v1/targets", timeout=5) as response:
    payload = json.load(response)

for target in payload.get("data", {}).get("activeTargets", []):
    labels = target.get("labels", {})
    print(f"{labels.get('job')}: {target.get('health')} · {target.get('scrapeUrl')} · {target.get('lastError') or 'no errors'}")
PY

log "Prometheus query evidence"
python3 - <<'PY'
import json
import urllib.parse
import urllib.request

queries = {
    "request_rate": "sum(rate(agent_requests_total[30s]))",
    "guardrail_blocks_5m": "sum(increase(guardrail_blocks_total[5m]))",
    "fallbacks_5m": "sum(increase(llm_gateway_fallbacks_total[5m]))",
    "approval_queue_depth": "approval_queue_depth",
}

for name, query in queries.items():
    url = "http://localhost:9090/api/v1/query?" + urllib.parse.urlencode({"query": query})
    with urllib.request.urlopen(url, timeout=5) as response:
        payload = json.load(response)
    results = payload.get("data", {}).get("result", [])
    value = results[0]["value"][1] if results else "0"
    print(f"{name}: {value}")
PY

log "Dashboard ready for recording"
printf "Grafana: %s\n" "$DASHBOARD_URL"
printf "Prometheus targets: %s\n" "$PROM_TARGETS_URL"
printf "Prometheus request rate: %s\n" "$PROM_GRAPH_REQUESTS"
printf "Prometheus guardrails: %s\n" "$PROM_GRAPH_GUARDRAILS"
printf "Prometheus fallbacks: %s\n" "$PROM_GRAPH_FALLBACKS"
printf "Prometheus approvals: %s\n" "$PROM_GRAPH_APPROVALS"
printf "\nKeep this terminal open during recording if you want traffic to continue.\n"
printf "Stop after recording:\n  cd %s && docker compose down\n" "$ROOT_DIR"
