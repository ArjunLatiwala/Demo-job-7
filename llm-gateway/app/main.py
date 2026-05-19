import json
import logging
import random
import time
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("llm-gateway")

app = FastAPI(
    title="Enterprise LLM Gateway",
    description="Provider routing, fallback, token accounting, and reliability controls for healthcare AI agents.",
    version="1.0.0",
)

REQUESTS = Counter("llm_gateway_requests_total", "Total LLM gateway requests", ["provider", "status"])
FAILURES = Counter("llm_gateway_failures_total", "Total simulated provider failures", ["provider"])
FALLBACKS = Counter("llm_gateway_fallbacks_total", "Total fallback routing events", ["from_provider", "to_provider"])
TOKENS = Counter("estimated_token_usage_total", "Estimated token usage", ["provider"])
COST = Counter("estimated_cost_total", "Estimated model cost in demo units", ["provider"])
LATENCY = Histogram("llm_gateway_latency_seconds", "Gateway latency", ["provider"])

PROVIDER_COSTS = {
    "provider_a": 0.0008,
    "provider_b": 0.0006,
    "fallback_provider": 0.0004,
}


class GatewayRequest(BaseModel):
    request_id: str | None = None
    prompt: str
    policy_status: str = "approved"
    risk_level: str = "low"
    preferred_provider: str = "provider_a"


def log_event(**payload):
    event = {"timestamp": datetime.now(timezone.utc).isoformat(), "service": "llm-gateway", **payload}
    logger.info(json.dumps(event))


def estimate_tokens(text: str) -> int:
    return max(32, int(len(text.split()) * 1.35) + random.randint(25, 90))


def simulate_provider(provider: str, prompt: str) -> tuple[str, int, int]:
    latency_ms = random.randint(180, 900)
    if provider == "provider_a" and any(term in prompt.lower() for term in ["latency", "fallback", "outage"]):
        latency_ms = random.randint(1350, 1900)
    time.sleep(latency_ms / 1000)
    tokens = estimate_tokens(prompt)
    response = (
        "Enterprise clinical operations guidance generated from approved policy context. "
        "This response avoids diagnosis, medication advice, and patient-specific disclosure."
    )
    return response, latency_ms, tokens


@app.post("/generate")
def generate(payload: GatewayRequest, request: Request):
    request_id = payload.request_id or str(uuid4())
    primary_provider = payload.preferred_provider
    provider = primary_provider
    fallback_used = False

    response_text, latency_ms, tokens = simulate_provider(provider, payload.prompt)

    if latency_ms > 1200:
        FAILURES.labels(provider=provider).inc()
        fallback_provider = "fallback_provider"
        FALLBACKS.labels(from_provider=provider, to_provider=fallback_provider).inc()
        log_event(
            event="provider_latency_threshold_exceeded",
            request_id=request_id,
            provider=provider,
            latency_ms=latency_ms,
            routing_decision="fallback_provider_selected",
        )
        provider = fallback_provider
        fallback_used = True
        response_text, latency_ms, tokens = simulate_provider(provider, payload.prompt)

    estimated_cost = round(tokens * PROVIDER_COSTS[provider], 5)
    REQUESTS.labels(provider=provider, status="success").inc()
    TOKENS.labels(provider=provider).inc(tokens)
    COST.labels(provider=provider).inc(estimated_cost)
    LATENCY.labels(provider=provider).observe(latency_ms / 1000)

    log_event(
        event="llm_completion_routed",
        request_id=request_id,
        provider=provider,
        primary_provider=primary_provider,
        latency_ms=latency_ms,
        estimated_tokens=tokens,
        estimated_cost=estimated_cost,
        fallback_used=fallback_used,
        policy_status=payload.policy_status,
        risk_level=payload.risk_level,
    )

    return {
        "request_id": request_id,
        "provider": provider,
        "primary_provider": primary_provider,
        "fallback_used": fallback_used,
        "latency_ms": latency_ms,
        "estimated_tokens": tokens,
        "estimated_cost": estimated_cost,
        "response": response_text,
    }


@app.get("/health")
def health():
    return {"service": "llm-gateway", "status": "healthy", "providers": ["provider_a", "provider_b", "fallback_provider"]}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
