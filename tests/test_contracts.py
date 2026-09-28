from datetime import UTC, datetime

import pytest

from tads_contracts import (
    EvidenceRef,
    FadeReachHandoff,
    ProvenanceRef,
    RecommendationAction,
    ReconOSRequest,
    ResolutionState,
    ScoreComponent,
    ScoreContract,
    SourceClass,
    SourceContract,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(
        "ev-1",
        ProvenanceRef("src-1", "snap-1", "sha256:abc", datetime.now(UTC), "test", "1"),
        0.9,
    )


def test_provenance_and_evidence() -> None:
    evidence().validate()


def test_evidence_confidence() -> None:
    item = EvidenceRef("ev-1", evidence().provenance, 1.1)
    with pytest.raises(ValueError, match="confidence"):
        item.validate()


def test_enabled_source_requires_review() -> None:
    source = SourceContract(
        "greenhouse",
        "Greenhouse",
        "Job Board",
        SourceClass.PUBLIC_STRUCTURED,
        "documented_api",
        "provider-policy:greenhouse",
        ("job_id",),
        (),
        30,
        30,
        authentication_required=False,
        legal_reviewed=False,
        tenant_id="t-1",
        enabled=True,
    )
    with pytest.raises(ValueError, match="review"):
        source.validate()


def test_scores_are_evidence_backed() -> None:
    component = ScoreComponent("signal_strength", 0.8, 1.0, ("ev-1",))
    ScoreContract("m0.1", (component,), 0.8, 0.9).validate()


def test_score_without_evidence_fails() -> None:
    with pytest.raises(ValueError, match="evidence"):
        ScoreComponent("fit", 0.8, 1.0, ()).validate()


def test_fadereach_handoff_is_evidence_backed() -> None:
    handoff = FadeReachHandoff(
        "h-1",
        "t-1",
        "a-1",
        "o-1",
        "documented change",
        ("ev-1",),
        None,
        None,
    )
    assert handoff.evidence_ids == ("ev-1",)


def test_reconos_request_is_tenant_scoped() -> None:
    request = ReconOSRequest("r-1", "t-1", "a-1", ("technology",), "account_research")
    assert request.tenant_id == "t-1"


def test_score_recomputation_is_deterministic() -> None:
    contract = ScoreContract(
        "m0.1",
        (
            ScoreComponent("fit", 0.8, 2.0, ("ev-1",)),
            ScoreComponent("freshness", 0.4, 1.0, ("ev-2",)),
        ),
        0.6666666667,
        0.9,
    )
    assert contract.recompute() == pytest.approx(2 / 3)


def test_taxonomy_values_are_stable() -> None:
    assert RecommendationAction.QUEUE_FOR_FADEREACH.value == "queue_for_fadereach"
    assert ResolutionState.AMBIGUOUS.value == "ambiguous"
