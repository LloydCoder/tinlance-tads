import pytest

from tads_console import AccountIntelligenceView
from tads_runtime import ComponentHealth, RuntimeReadiness


def test_console_projection_is_evidence_first() -> None:
    view = AccountIntelligenceView(
        "a1",
        "Acme",
        ("security hiring increased",),
        ("recent security hiring",),
        0.8,
        0.7,
        "RESEARCH",
        ("ev-1",),
        ("ownership",),
        (("icp_fit", 0.9), ("timing", 0.8)),
        ("audit-1",),
    )
    assert view.evidence_ids == ("ev-1",)
    assert view.to_dict()["score_components"] == {"icp_fit": 0.9, "timing": 0.8}


def test_runtime_readiness_fails_closed() -> None:
    blocked = RuntimeReadiness(
        ComponentHealth.HEALTHY,
        ComponentHealth.UNHEALTHY,
        ComponentHealth.HEALTHY,
        ComponentHealth.HEALTHY,
    )
    ready = RuntimeReadiness(
        ComponentHealth.HEALTHY,
        ComponentHealth.HEALTHY,
        ComponentHealth.HEALTHY,
        ComponentHealth.HEALTHY,
    )
    assert blocked.ready is False
    assert ready.ready is True


def test_console_view_rejects_missing_evidence() -> None:
    with pytest.raises(ValueError):
        AccountIntelligenceView(
            "a1",
            "Acme",
            (),
            (),
            0.5,
            0.5,
            "MONITOR",
            ("ev-1",),
            (),
        )


def test_console_view_rejects_missing_score_decomposition() -> None:
    with pytest.raises(ValueError, match="score decomposition"):
        AccountIntelligenceView(
            "a1",
            "Acme",
            (),
            (),
            0.5,
            0.5,
            "MONITOR",
            ("ev-1",),
            (),
        )
