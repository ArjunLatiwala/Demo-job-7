import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

sys.path.append(str(Path(__file__).resolve().parents[2]))
from guardrails.policy_engine import evaluate_policy, retrieve_policy_context

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("agent-api")

LLM_GATEWAY_URL = os.getenv("LLM_GATEWAY_URL", "http://llm-gateway:8001")
APPROVAL_QUEUE = Path(os.getenv("APPROVAL_QUEUE", "/app/data/approvals.json"))
APPROVAL_QUEUE.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Enterprise Healthcare AI Agent Governance Platform",
    description="Agent orchestration, guardrails, approval workflow, and observability for regulated healthcare AI.",
    version="1.0.0",
)

AGENT_REQUESTS = Counter("agent_requests_total", "Total agent orchestration requests", ["status", "risk_level"])
GUARDRAIL_BLOCKS = Counter("guardrail_blocks_total", "Requests requiring guardrail escalation", ["risk_level", "reason"])
APPROVAL_REQUESTS = Counter("approval_requests_total", "Human approval workflow requests", ["status"])
AGENT_LATENCY = Histogram("agent_latency_seconds", "Agent orchestration latency", ["policy_status"])
SYSTEM_HEALTH = Gauge("system_health", "Synthetic platform health score", ["component"])
APPROVAL_QUEUE_DEPTH = Gauge("approval_queue_depth", "Current approval queue depth")

SYSTEM_HEALTH.labels(component="agent-api").set(1)
SYSTEM_HEALTH.labels(component="llm-gateway").set(1)
SYSTEM_HEALTH.labels(component="guardrails").set(1)


class AgentRequest(BaseModel):
    user_id: str = "clinical-ops-user"
    department: str = "care-operations"
    message: str
    preferred_provider: str = "provider_a"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(**payload):
    event = {"timestamp": utc_now(), "service": "agent-api", **payload}
    logger.info(json.dumps(event))


def load_queue() -> list[dict]:
    if not APPROVAL_QUEUE.exists():
        return []
    try:
        return json.loads(APPROVAL_QUEUE.read_text())
    except json.JSONDecodeError:
        return []


def save_queue(queue: list[dict]) -> None:
    APPROVAL_QUEUE.write_text(json.dumps(queue, indent=2))
    APPROVAL_QUEUE_DEPTH.set(len([item for item in queue if item["status"] == "pending"]))


def enqueue_approval(request_id: str, payload: AgentRequest, decision, context: dict) -> dict:
    queue = load_queue()
    approval = {
        "approval_id": f"APR-{request_id[:8].upper()}",
        "request_id": request_id,
        "status": "pending",
        "risk_level": decision.risk_level,
        "risk_reasons": decision.reasons,
        "department": payload.department,
        "user_id": payload.user_id,
        "message_preview": payload.message[:140],
        "policy_document": context["document"],
        "created_at": utc_now(),
        "escalation_path": "Clinical AI Governance Board > On-call Safety Reviewer",
    }
    queue.append(approval)
    save_queue(queue)
    APPROVAL_REQUESTS.labels(status="pending").inc()
    return approval


@app.post("/run-agent")
def run_agent(payload: AgentRequest, request: Request):
    request_id = str(uuid4())
    started = time.time()

    log_event(
        event="agent_request_received",
        request_id=request_id,
        user_id=payload.user_id,
        department=payload.department,
        preferred_provider=payload.preferred_provider,
    )

    decision = evaluate_policy(payload.message)
    context = retrieve_policy_context(payload.message)

    for reason in decision.reasons:
        GUARDRAIL_BLOCKS.labels(risk_level=decision.risk_level, reason=reason).inc()

    log_event(
        event="policy_evaluation_completed",
        request_id=request_id,
        policy_status=decision.status,
        risk_level=decision.risk_level,
        risk_reasons=decision.reasons,
        requires_approval=decision.requires_approval,
        retrieved_document=context["document"],
    )

    approval = None
    if decision.requires_approval:
        approval = enqueue_approval(request_id, payload, decision, context)
        log_event(
            event="human_approval_requested",
            request_id=request_id,
            approval_id=approval["approval_id"],
            risk_level=decision.risk_level,
            escalation_path=approval["escalation_path"],
        )

    gateway_payload = {
        "request_id": request_id,
        "prompt": f"Context: {context['summary']}\nUser request: {payload.message}",
        "policy_status": decision.status,
        "risk_level": decision.risk_level,
        "preferred_provider": payload.preferred_provider,
    }

    gateway_response = requests.post(f"{LLM_GATEWAY_URL}/generate", json=gateway_payload, timeout=8).json()
    elapsed = round(time.time() - started, 4)

    AGENT_REQUESTS.labels(status=decision.status, risk_level=decision.risk_level).inc()
    AGENT_LATENCY.labels(policy_status=decision.status).observe(elapsed)

    log_event(
        event="agent_workflow_completed",
        request_id=request_id,
        latency_ms=int(elapsed * 1000),
        model_provider=gateway_response["provider"],
        fallback_used=gateway_response["fallback_used"],
        estimated_tokens=gateway_response["estimated_tokens"],
        estimated_cost=gateway_response["estimated_cost"],
        approval_required=decision.requires_approval,
    )

    return {
        "request_id": request_id,
        "workflow": "healthcare-agent-governance-orchestration",
        "policy_status": decision.status,
        "risk_level": decision.risk_level,
        "risk_reasons": decision.reasons,
        "approval_required": decision.requires_approval,
        "approval": approval,
        "retrieval": context,
        "llm_gateway": gateway_response,
        "final_response": gateway_response["response"] if not decision.requires_approval else "Response staged for human review before delivery.",
        "latency_ms": int(elapsed * 1000),
    }


@app.get("/approval-status")
def approval_status():
    queue = load_queue()
    pending = [item for item in queue if item["status"] == "pending"]
    APPROVAL_QUEUE_DEPTH.set(len(pending))
    return {
        "service": "clinical-ai-governance-workflow",
        "pending_count": len(pending),
        "total_requests": len(queue),
        "approvals": queue[-15:],
    }


@app.get("/system-status")
def system_status():
    queue = load_queue()
    pending = len([item for item in queue if item["status"] == "pending"])
    return {
        "platform": "Enterprise Healthcare AI Agent Governance Platform",
        "environment": os.getenv("ENVIRONMENT", "local-enterprise-demo"),
        "status": "operational",
        "components": {
            "agent_api": "healthy",
            "guardrails": "enforcing",
            "llm_gateway": "healthy",
            "approval_workflow": "active",
            "observability": "enabled",
        },
        "active_model_routing": ["provider_a", "provider_b", "fallback_provider"],
        "approval_queue_depth": pending,
    }


@app.get("/health")
def health():
    return {"service": "agent-api", "status": "healthy", "guardrails": "enabled", "observability": "enabled"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
