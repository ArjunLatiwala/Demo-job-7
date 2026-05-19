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

## Work Completed In This Session

### Platform Runtime Fixes

- Fixed Docker Compose approval queue storage so `agent-api` can write approval records while running as non-root user.
- Fixed NGINX upstream names so reverse proxy resolves Docker network services correctly.
- Fixed incident simulation script argument conflict that caused `TypeError: emit() got multiple values for argument 'severity'`.
- Verified platform runtime direction: Docker Compose starts Agent API, LLM Gateway, Prometheus, Grafana, and NGINX for local showcase.

### Legacy Dashboard Repositioning

`dashboard-fail.html` was repositioned as the client’s old/pre-remediation AI operations console, not just the new platform in an outage state.

Changes made:

- Renamed visual identity toward legacy/pre-remediation operations.
- Added weak-maturity signals: stale sync, missing trace IDs, manual spreadsheet reviews, no fallback routing, fragmented logs, partial observability coverage.
- Kept it realistic and enterprise-internal, not cartoonishly broken.
- Strengthened contrast against final transformed platform.

### Grafana Dashboard Upgrade

`monitoring/grafana/dashboards/healthcare-ai-governance.json` was upgraded into a stronger enterprise operations dashboard.

It now focuses on:

- AI request throughput.
- Guardrail escalations.
- Human review queue depth.
- Fallback routing events.
- Provider latency.
- Token/cost burn.
- Governance control actions.
- Incident containment proof.
- Executive reliability summary.

Design intent:

- Grafana should be the main visual proof of runtime observability.
- Dashboard should feel like a real enterprise AI operations command center.
- Colors should communicate controlled operations, not constant failure.

### Local Showcase Script

Created/strengthened `scripts/showcase_observability.sh`.

Purpose:

- One-command local platform showcase for video recording.
- Starts Docker Compose runtime.
- Waits for services to be healthy.
- Opens Grafana and Prometheus views.
- Runs smoke workflow.
- Starts traffic generation.
- Runs incident simulation.
- Prints Prometheus evidence.
- Keeps environment ready for screen recording.

Important distinction:

- `scripts/showcase_observability.sh` is for local video recording.
- GitHub Actions pipeline starts its own internal runtime in the runner, but it does not open browser windows for recording.

### CI Runtime Gate

Created `scripts/ci_observability_gate.sh` for GitHub Actions.

Purpose:

- Start full Docker Compose platform in CI.
- Validate service health.
- Run smoke workflow.
- Run incident simulation.
- Validate Prometheus targets.
- Validate metrics moved.
- Validate Grafana dashboard provisioning.
- Tear down runtime after validation.

This proves the platform is not just static HTML; it runs as a multi-service system with real telemetry and runtime checks.

### Pipeline Evolution

The GitHub Actions workflow went through multiple iterations:

1. Fixed broken file paths caused by workflow assuming wrong repository root.
2. Expanded from basic CI into enterprise-style release orchestration.
3. Reduced over-complex 19-job graph because it was too dense for client video.
4. Refactored job names from generic DevOps gates toward architecture-facing platform components.
5. Reshaped graph so GitHub Actions UI is more readable without zoom.

Current workflow file:

- `.github/workflows/enterprise-devsecops.yml`

Current workflow name:

- `HelixCare AI Platform Release`

Current graph shape is intentionally shallow:

```text
Platform Blueprint
        │
        ├─ AI Control Plane
        ├─ LLM Gateway
        ├─ Governance Engine
        ├─ Observability Stack
        └─ Operations Workflow
        │
        ▼
Release Evidence
        │
        ▼
Production Summary
```

Reason:

- GitHub Actions graph cannot be manually forced vertical.
- GitHub renders DAGs left-to-right.
- Best video-readable layout is fewer columns with stacked parallel architecture jobs.
- This layout maps to actual solution architecture and remains readable in screen recording.

Current pipeline jobs:

- `Platform Blueprint` — validates architecture files and platform structure.
- `AI Control Plane` — validates Agent API service contract.
- `LLM Gateway` — validates gateway/fallback service layer.
- `Governance Engine` — validates healthcare policy controls and tests.
- `Observability Stack` — validates Prometheus/Grafana configuration and dashboard JSON.
- `Operations Workflow` — deploys full runtime, runs smoke test, incident simulation, synthetic traffic, Prometheus target checks, Grafana dashboard check, and runtime metric checks.
- `Release Evidence` — generates release attestation.
- `Production Summary` — publishes executive release summary.

Required evidence artifacts now exist in workflow:

- `governance-report.json`
- `runtime-readiness-report.json`
- `observability-evidence.json`
- `release-attestation.json`

Additional evidence artifacts:

- `platform-blueprint.json`
- `ai-control-plane.json`
- `llm-gateway.json`
- `security-evidence.json`
- `sbom.json`

Pipeline language requirement:

- Avoid `demo`, `Demo`, or `DEMO` in pipeline-visible names because video should feel like real enterprise release flow.

## Actual Solution Architecture

This project provides an enterprise Healthcare AI Operations platform made of these layers:

```text
Healthcare AI Agent Platform
        +
Governance Control Plane
        +
LLM Gateway
        +
Human Approval Workflow
        +
Observability Stack
        +
DevSecOps Release Pipeline
```

### AI Control Plane

Implemented by Agent API.

Responsibilities:

- Receive AI workflow requests.
- Run policy checks before model delivery.
- Route approved requests to LLM Gateway.
- Queue high-risk requests for human review.
- Expose operational metrics.

Files:

- `agent-api/app/main.py`
- `agent-api/Dockerfile`

### LLM Gateway

Responsibilities:

- Centralize model/provider access.
- Simulate primary/fallback provider routing.
- Track provider latency.
- Track token and cost metrics.
- Expose gateway metrics.

Files:

- `llm-gateway/app/main.py`
- `llm-gateway/Dockerfile`

### Governance Engine

Responsibilities:

- Detect clinical-risk prompts.
- Detect prescription/medication risk.
- Detect PHI/patient data risk.
- Detect prompt-injection style requests.
- Decide whether request is approved, blocked, or sent to human review.

File:

- `guardrails/policy_engine.py`

### Human Approval Workflow

Responsibilities:

- Store high-risk requests needing review.
- Track approval queue depth.
- Provide governance evidence for risky AI operations.

Files:

- `approval-service/data/approvals.json`
- `agent-api/app/main.py`

### Observability Stack

Responsibilities:

- Prometheus scrapes runtime metrics from Agent API and LLM Gateway.
- Grafana renders enterprise operations dashboard.
- Runtime scripts generate traffic and incidents so metrics visibly move.

Files:

- `monitoring/prometheus/prometheus.yml`
- `monitoring/grafana/dashboards/healthcare-ai-governance.json`

Important metrics:

- `agent_requests_total`
- `guardrail_blocks_total`
- `approval_queue_depth`
- `llm_gateway_fallbacks_total`
- `llm_gateway_latency_seconds_bucket`
- `estimated_token_usage_total`
- `estimated_cost_total`

### Container Platform

Responsibilities:

- Run the platform locally as a multi-service environment.
- Provide repeatable startup for showcase and CI validation.

Files:

- `docker-compose.yml`
- `nginx/nginx.conf`

Services:

- Agent API
- LLM Gateway
- Prometheus
- Grafana
- NGINX ingress

### DevSecOps Pipeline

Responsibilities:

- Validate platform architecture.
- Validate architecture layers.
- Deploy local runtime stack in GitHub runner.
- Validate observability, governance, fallback, and approval workflows.
- Generate release evidence and production summary.

File:

- `.github/workflows/enterprise-devsecops.yml`

## Further Approach

### Immediate Next Steps

1. Push current workflow changes and run GitHub Actions.
2. Confirm GitHub Actions graph is readable in video without zoom.
3. Fix any failing job based on logs, especially dependency/security/runtime checks.
4. Ensure full pipeline ends green before final recording.
5. Re-run local `scripts/showcase_observability.sh` to confirm Grafana/Prometheus runtime view still works.

### Video Showcase Approach

Recommended sequence:

1. Show `dashboard-fail.html` as old client platform.
2. Explain missing governance, weak observability, manual approvals, no fallback, stale operations.
3. Show GitHub Actions pipeline as architecture release flow.
4. Show Docker Compose / terminal startup.
5. Run or show `scripts/showcase_observability.sh`.
6. Show Prometheus targets and metric queries.
7. Show Grafana command center with live metrics.
8. Trigger/observe incident simulation.
9. Show fallback routing and human approval queue evidence.
10. End with final `dashboard.html` transformed command center.

### Pipeline Presentation Guidance

When showing GitHub Actions:

- Do not zoom too far into logs unless needed.
- Focus on the graph labels because they now map to architecture.
- Explain each job as a platform layer, not as generic CI/CD.
- If a job fails, do not record final video; fix and rerun until green.
- Green readable graph matters more than high job count.

### Remaining Quality Checks

Before final packaging/showcase:

- Verify no `__pycache__` or `.pyc` files are included.
- Verify local Docker Compose startup from clean state.
- Verify Grafana dashboard loads with expected title.
- Verify Prometheus targets show `agent-api` and `llm-gateway` healthy.
- Verify incident simulation moves fallback and guardrail metrics.
- Verify approval queue file remains writable in container.
- Verify pipeline has no visible `demo` wording in job names or video-visible output.
- Decide whether `new_dashboard.html`, `fix_graphs.py`, and `update_graphs.py` should be kept, ignored, or removed before final delivery.

### Current Design Principle

The project should present as a real enterprise AI platform modernization:

```text
Before: fragmented AI operations, weak governance, no telemetry, manual review.
After: governed AI control plane, LLM gateway, approval workflow, Prometheus/Grafana telemetry, fallback routing, and release evidence.
```

Primary credibility signals:

- Running containers.
- Real metrics.
- Grafana dashboard.
- Prometheus targets.
- Incident simulation.
- Human approval queue.
- Fallback routing.
- GitHub Actions evidence artifacts.
- Final polished command center.
