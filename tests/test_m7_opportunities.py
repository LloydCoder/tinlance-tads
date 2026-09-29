from tads_opportunities import ICPProfile, OpportunityEngine


def test_opportunity_score_is_explainable_and_bounded() -> None:
    result = OpportunityEngine().evaluate(
        "a1",
        industry="SaaS",
        geography="Germany",
        employees=100,
        capabilities={"cybersecurity", "ai"},
        signal_strength=0.9,
        momentum=0.8,
        negative_evidence=0.0,
        data_confidence=0.9,
        profile=ICPProfile(
            frozenset({"saas"}),
            frozenset({"germany"}),
            20,
            500,
            frozenset({"cybersecurity"}),
        ),
        evidence_ids=("ev-1", "ev-2"),
    )
    assert 0 <= result.score <= 1
    assert result.recommendation == "CREATE_OPPORTUNITY"
    assert result.hypothesis.startswith("Observed evidence")
    assert result.evidence_ids == ("ev-1", "ev-2")


def test_unknowns_are_preserved() -> None:
    result = OpportunityEngine().evaluate(
        "a1",
        industry=None,
        geography=None,
        employees=None,
        capabilities=set(),
        signal_strength=0.5,
        momentum=0.2,
        negative_evidence=0.0,
        data_confidence=0.5,
        profile=ICPProfile(frozenset({"saas"}), frozenset({"germany"})),
        evidence_ids=("ev-1",),
    )
    assert set(result.unknowns) == {"industry", "geography", "employee count"}


def test_opportunity_requires_evidence() -> None:
    import pytest

    with pytest.raises(ValueError, match="evidence"):
        OpportunityEngine().evaluate(
            "a1",
            industry="SaaS",
            geography="Germany",
            employees=100,
            capabilities=set(),
            signal_strength=0.5,
            momentum=0.2,
            negative_evidence=0.0,
            data_confidence=0.5,
            profile=ICPProfile(frozenset({"saas"}), frozenset({"germany"})),
            evidence_ids=(),
        )
