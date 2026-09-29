import pytest

from tads_integrations import EnrichmentRequest, OpportunityHandoff


def test_recon_request_is_purpose_limited() -> None:
    request = EnrichmentRequest("a1", "validate technology need", ("technology",))
    assert request.evidence_required is True
    assert request.fields == ("technology",)


def test_fadereach_handoff_requires_evidence_and_score_bounds() -> None:
    handoff = OpportunityHandoff(
        "o1", "a1", 0.8, 0.7, "evidence-backed hypothesis", ("ev-1",), None, None, "now"
    )
    assert 0 <= handoff.score <= 1
    assert handoff.evidence_ids


def test_invalid_handoff_is_rejected_by_consumer_validation() -> None:
    handoff = OpportunityHandoff("o1", "a1", 1.2, 0.7, "x", (), None, None, None)
    with pytest.raises(ValueError):
        if not 0 <= handoff.score <= 1 or not handoff.evidence_ids:
            raise ValueError("handoff requires bounded score and evidence")
