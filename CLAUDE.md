# Demo-job-7 Project Context

## Purpose

This folder contains a premium enterprise-style Healthcare AI Governance & Reliability Platform showcase for a client presentation video.

The project tells this story:

A healthcare enterprise wanted to deploy internal AI agents, but its existing AI operations workflow lacked governance, observability, reliability engineering, fallback handling, approval workflows, operational visibility, and DevOps maturity.

The goal is to show transformation from a weak AI operations dashboard into a production-grade enterprise AI governance and reliability command center.

## Video Narrative

1. Start with the client problem using `dashboard-fail.html`.
2. Show the weak/old platform as outdated, cluttered, operationally poor, low-visibility, and not enterprise-grade.
3. Transition into: “How we redesigned and operationalized the entire AI platform.”
4. Focus the implementation showcase on DevOps, AI platform engineering, observability, governance, reliability, operational automation, and runtime monitoring.
5. Make Grafana the main visual focus during the implementation section.
6. End with the final transformed enterprise platform in `dashboard.html`.

## Final Platform Identity

Final dashboard represents:

**HelixCare AI Governance & Reliability Command Center**

It should feel premium, cinematic, operational, realistic, enterprise SaaS grade, observability-focused, governance-focused, and reliability-focused.

Viewer reaction target:

“This team understands enterprise AI operations, DevOps, observability, and reliability engineering.”

## Reference Product Feel

The platform should resemble enterprise-grade systems such as:

- Datadog
- Grafana Cloud
- Splunk
- CrowdStrike
- Azure AI Studio
- ServiceNow Operations
- Enterprise SRE platforms

It must never feel like a college project, toy dashboard, frontend-only implementation, or AI-generated mockup.

## Demo Flow Focus

The main video focus is not frontend design. The core implementation sequence should showcase:

1. Docker Compose platform startup
2. Container orchestration
3. Service startup logs
4. Pipeline execution
5. Runtime operations
6. Traffic simulation
7. Grafana observability
8. Incident handling
9. Governance enforcement
10. Approval workflows
11. Fallback routing
12. Live telemetry and metrics

Grafana dashboards and telemetry must look real, operational, enterprise-grade, production-ready, and DevOps-heavy.

## Current Folder Map

- `dashboard-fail.html` — old/failed dashboard used to show client problem.
- `dashboard.html` — final HelixCare command center shown at end of video.
- `new_dashboard.html` — alternate/older dashboard draft; verify before using.
- `docker-compose.yml` — local platform orchestration.
- `agent-api/app/main.py` — FastAPI orchestration service with governance, approval, policy, metrics endpoints.
- `llm-gateway/app/main.py` — FastAPI LLM gateway with routing, fallback, latency/cost telemetry.
- `guardrails/policy_engine.py` — policy decision logic for safe/risky healthcare AI requests.
- `approval-service/data/approvals.json` — approval queue data file.
- `monitoring/prometheus/prometheus.yml` — Prometheus scrape config.
- `monitoring/grafana/` — Grafana provisioning/dashboard assets.
- `nginx/nginx.conf` — reverse proxy config.
- `scripts/generate_traffic.py` — video-friendly traffic simulation.
- `scripts/simulate_incident.py` — governance incident simulation.
- `scripts/live_ops_showcase.sh` — CLI-driven live operations demo flow.
- `scripts/demo_smoke_test.py` — platform smoke checks.
- `.github/workflows/enterprise-devsecops.yml` — DevSecOps pipeline proof for presentation.
- `docs/ARCHITECTURE.md` — architecture narrative.
- `docs/DEMO_FLOW.md` — intended video/demo sequence.
- `fix_graphs.py`, `update_graphs.py` — dashboard mutation scripts; treat as utilities/leftovers until verified.

## Current Assessment

The folder already has a strong enterprise DevOps/SRE skeleton: Docker Compose, FastAPI services, Prometheus metrics, Grafana provisioning, traffic simulation, incident simulation, policy engine, approval queue, CI workflow, and final dashboard assets.

The highest-value next work is to verify the platform actually runs cleanly and that Grafana shows real live metrics during the video sequence.

## Likely Gaps To Check

- Verify `docker-compose.yml` boots all services cleanly.
- Verify Prometheus scrapes Agent API and LLM Gateway metrics.
- Verify Grafana dashboard JSON exists and panels render real metrics.
- Verify `dashboard-fail.html` looks visibly weaker than `dashboard.html`; it may still share polished HelixCare branding/title.
- Verify `scripts/generate_traffic.py`, `scripts/simulate_incident.py`, and `scripts/live_ops_showcase.sh` produce compelling video-friendly output.
- Remove or ignore `__pycache__` files before packaging/showcase.
- Decide whether `new_dashboard.html`, `fix_graphs.py`, and `update_graphs.py` are useful or stale.

## Working Guidance

When editing this project:

- Prioritize operational realism over visual decoration.
- Make Grafana and runtime telemetry the hero of the implementation showcase.
- Keep dashboards enterprise-grade, not playful or generic.
- Use concrete healthcare AI ops language: PHI, HIPAA, clinical triage, approval queue, guardrail enforcement, fallback provider, SLO, latency, error budget, incident timeline, audit trail.
- Ensure the old dashboard communicates the client problem clearly.
- Ensure the final dashboard communicates transformation and operational maturity.
- Avoid adding fake-looking widgets unless backed by scripts, metrics, logs, or demo flow.
- Prefer changes that improve video credibility: startup logs, live metrics, incident spikes, approvals, fallback routing, pipeline evidence, and operational runbook feel.
