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
    )
    assert view.evidence_ids == ("ev-1",)


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
        AccountIntelligenceView("a1", "Acme", (), (), 0.5, 0.5, "MONITOR", (), ())
