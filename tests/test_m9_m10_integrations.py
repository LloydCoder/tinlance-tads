import pytest

from tads_integrations import EnrichmentRequest, EnrichmentResult, OpportunityHandoff


def test_recon_request_and_result_are_evidence_bounded() -> None:
    request = EnrichmentRequest("a1", "validate technology need", ("technology",))
    result = EnrichmentResult(
        "reconos", "contract-v1", "a1", ("ev-1",), (("technology", "postgres"),), ()
    )
    assert request.evidence_required is True
    assert result.evidence_ids == ("ev-1",)


def test_fadereach_handoff_validates_bounds_and_evidence() -> None:
    handoff = OpportunityHandoff(
        "o1", "a1", 0.8, 0.7, "evidence-backed hypothesis", ("ev-1",), None, None, "now"
    )
    assert handoff.score == 0.8


def test_invalid_contracts_fail_closed() -> None:
    with pytest.raises(ValueError):
        EnrichmentRequest("a1", "", ("technology",))
    with pytest.raises(ValueError):
        EnrichmentResult("reconos", "v1", "a1", (), (), ())
    with pytest.raises(ValueError):
        OpportunityHandoff("o1", "a1", 1.2, 0.7, "x", ("ev-1",), None, None, None)
