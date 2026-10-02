import pytest

from tads_assurance import (
    CalibrationRecord,
    E2EStage,
    E2EValidation,
    EnterpriseGate,
    GovernanceRecord,
    IdempotencyPolicy,
    OutcomeRecord,
    PrecisionRecall,
    PrivacyPolicy,
    Readiness,
    ReliabilityPolicy,
    RetentionPolicy,
    RetryPolicy,
    SecurityPolicy,
)


def test_feedback_metrics_and_outcome_are_deterministic() -> None:
    outcome = OutcomeRecord("opp-1", "2026-09-29T08:00:00Z", "won", "crm")
    metrics = PrecisionRecall(8, 2, 1, 9)
    calibration = CalibrationRecord("m11-v1", 20, 0.8, 0.75)
    assert outcome.opportunity_id == "opp-1"
    assert metrics.precision == 0.8
    assert metrics.recall == 8 / 9
    assert calibration.absolute_error == pytest.approx(0.05)


def test_reliability_security_and_governance_contracts() -> None:
    retry = RetryPolicy(4, 2.0, 10.0)
    assert retry.delay(1) == 2.0
    reliability = ReliabilityPolicy()
    reliability.validate()
    idempotency = IdempotencyPolicy()
    idempotency.validate("handoff-1")
    assert retry.delay(4) == 10.0
    assert retry.should_retry(3) is True
    policy = SecurityPolicy()
    policy.validate()
    privacy = PrivacyPolicy()
    privacy.validate()
    retention = RetentionPolicy(365, 90, 730)
    record = GovernanceRecord("M16-ACCESS", "security", "approved", "2026-09-29", "audit-1", 90)
    assert retention.personal_data_days < retention.evidence_days
    assert record.status == "approved"


def test_e2e_and_enterprise_gate() -> None:
    e2e = E2EValidation(frozenset(E2EStage))
    e2e.validate()
    gate = EnterpriseGate(True, True, True, True, True, True, True)
    assert gate.readiness is Readiness.READY
