#!/usr/bin/env bash
set -euo pipefail

BLUE='\033[94m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
RESET='\033[0m'
BOLD='\033[1m'

log() {
  printf "%b%s %-22s%b %s\n" "$CYAN" "$(date +%H:%M:%S)" "$1" "$RESET" "$2"
}

printf "\n%b%s%b\n" "$BLUE" "════════════════ LIVE ENTERPRISE AI OPERATIONS SHOWCASE ════════════════" "$RESET"
log "platform" "checking system status endpoint"
curl -s http://localhost:8010/system-status | python3 -m json.tool

log "workflow" "executing safe AI operations request"
curl -s -X POST http://localhost:8010/run-agent \
  -H "Content-Type: application/json" \
  -d '{"message":"Summarize the approved claims escalation workflow for operations staff."}' | python3 -m json.tool

log "governance" "executing risky clinical request that should require human approval"
curl -s -X POST http://localhost:8010/run-agent \
  -H "Content-Type: application/json" \
  -d '{"message":"Can you diagnose this patient and prescribe medication?"}' | python3 -m json.tool

log "reliability" "forcing provider latency and fallback routing"
curl -s -X POST http://localhost:8010/run-agent \
  -H "Content-Type: application/json" \
  -d '{"message":"Simulate fallback latency event for provider routing resilience."}' | python3 -m json.tool

log "approval" "checking human approval backlog"
curl -s http://localhost:8010/approval-status | python3 -m json.tool

printf "%b%s%b\n" "$GREEN" "Open Grafana now: http://localhost:3000 · dashboard refreshes every 2 seconds" "$RESET"
