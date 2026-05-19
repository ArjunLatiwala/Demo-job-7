# Video Flow: Live Enterprise AI Operations & Reliability Platform

## Positioning

This demo is not a static dashboard walkthrough. It is a live operations showcase for a healthcare AI platform. The hero visuals are Docker orchestration, streaming logs, Grafana telemetry, traffic simulation, fallback routing, incident handling, governance enforcement, and CI/CD release gates.

## Scene 1 — Executive command center, 10 seconds

Open `dashboard.html` only as a branded opening layer.

Message: “A healthcare enterprise needs to operate AI agents safely with governance, reliability, and observability.”

Do not stay here long.

## Scene 2 — Start platform, 20 seconds

Run:

```bash
docker compose up --build
```

Show service startup, health checks, NGINX, Prometheus, Grafana, Agent API, and LLM Gateway.

Message: “The full local platform starts as containerized services with production-style boundaries.”

## Scene 3 — Container health, 10 seconds

Run:

```bash
docker compose ps
```

Show healthy containers.

## Scene 4 — Live control plane, 20 seconds

Run:

```bash
./scripts/live_ops_showcase.sh
```

This performs system status, safe workflow, risky workflow, fallback routing, and approval backlog checks.

## Scene 5 — Grafana as hero visual, 45 seconds

Open:

```text
http://localhost:3000
```

Dashboard:

```text
Live Enterprise AI Operations & Reliability Platform
```

Run:

```bash
python3 scripts/generate_traffic.py --requests 80 --risky-ratio 0.45 --delay 0.18
```

Show live movement in:

- AI Platform SLO
- Live AI throughput
- Gateway p95 latency
- Fallback routing timeline
- Approval queue growth
- Governance violation breakdown
- Token consumption and cost anomaly view
- Request latency heatmap

## Scene 6 — Incident spike, 35 seconds

Run:

```bash
python3 scripts/simulate_incident.py
```

Show colored terminal output:

- critical incident detected
- guardrail blocks unsafe output
- fallback provider activates
- approval workflow triggered
- Prometheus metrics updated
- Grafana incident spike visible
- runbook resolves incident

## Scene 7 — Metrics proof, 15 seconds

Open Prometheus:

```text
http://localhost:9090
```

Search:

```text
guardrail_blocks_total
llm_gateway_fallbacks_total
approval_queue_depth
estimated_cost_total
```

Message: “These are real metrics emitted by the services, not static UI numbers.”

## Scene 8 — DevSecOps release gate, 20 seconds

Open:

```text
.github/workflows/enterprise-devsecops.yml
```

Show:

- tests
- Bandit security scan
- Docker build validation
- Compose validation
- release gate summary

## Closing

Message: “This turns unsafe AI agents into a live, observable, governed, and reliable enterprise AI operations platform.”
