import re
from dataclasses import dataclass
from typing import List


@dataclass
class PolicyDecision:
    status: str
    risk_level: str
    reasons: List[str]
    requires_approval: bool


POLICY_PATTERNS = {
    "clinical_diagnosis": [r"\bdiagnose\b", r"\bdiagnosis\b", r"what disease", r"do i have"],
    "prescription_advice": [r"\bprescribe\b", r"\bmedication dosage\b", r"stop taking", r"increase my dose"],
    "patient_records": [r"patient record", r"medical record", r"mrn", r"ssn", r"date of birth"],
    "prompt_injection": [r"ignore previous", r"system prompt", r"developer message", r"bypass policy"],
    "unsafe_guidance": [r"emergency but", r"avoid the doctor", r"skip treatment"],
}


def evaluate_policy(message: str) -> PolicyDecision:
    normalized = message.lower()
    reasons: List[str] = []

    for category, patterns in POLICY_PATTERNS.items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            reasons.append(category)

    if not reasons:
        return PolicyDecision(
            status="approved",
            risk_level="low",
            reasons=[],
            requires_approval=False,
        )

    high_risk = {"clinical_diagnosis", "prescription_advice", "patient_records"}
    risk_level = "high" if any(reason in high_risk for reason in reasons) else "medium"

    return PolicyDecision(
        status="human_review_required",
        risk_level=risk_level,
        reasons=reasons,
        requires_approval=True,
    )


def retrieve_policy_context(message: str) -> dict:
    normalized = message.lower()
    if "claim" in normalized or "insurance" in normalized:
        return {
            "document": "clinical-operations-claims-routing-v4",
            "summary": "Claims and coverage questions must be answered using approved benefit policy language.",
        }
    if "medication" in normalized or "dose" in normalized or "prescription" in normalized:
        return {
            "document": "medication-safety-escalation-policy-v2",
            "summary": "Medication decisions require licensed clinician review before guidance is provided.",
        }
    if "patient" in normalized or "record" in normalized:
        return {
            "document": "hipaa-minimum-necessary-access-standard",
            "summary": "Patient record access must be audited and limited to approved care operations.",
        }
    return {
        "document": "enterprise-ai-assistant-safe-response-standard",
        "summary": "General operational questions may be answered with safe, non-clinical guidance.",
    }
