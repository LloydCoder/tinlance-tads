from datetime import UTC, datetime

import pytest

from tads_contracts.source import SourceContract
from tads_contracts.taxonomy import SourceClass
from tads_sources import SourceHealth, SourceLifecycle, SourceRecord, SourceRegistry


def contract(*, enabled: bool = False, legal_reviewed: bool = False) -> SourceContract:
    return SourceContract(
        source_id="greenhouse:example",
        provider="greenhouse",
        name="Example Greenhouse board",
        source_class=SourceClass.JOBS,
        access_mechanism="documented_public_api",
        terms_reference="https://example.test/terms",
        permitted_fields=("title", "location"),
        geographic_constraints=(),
        retention_days=30,
        rate_limit_per_minute=30,
        authentication_required=False,
        legal_reviewed=legal_reviewed,
        enabled=enabled,
    )


def test_registry_is_fail_closed_until_activation() -> None:
    registry = SourceRegistry()
    registry.register(SourceRecord(contract()))
    assert registry.ingestion_allowed("greenhouse:example") is False


def test_activation_requires_review_and_enabled_contract() -> None:
    registry = SourceRegistry()
    registry.register(SourceRecord(contract(enabled=False, legal_reviewed=True)))
    with pytest.raises(ValueError, match="enabled"):
        registry.activate("greenhouse:example")


def test_activation_then_suspend_blocks_ingestion() -> None:
    registry = SourceRegistry()
    registry.register(SourceRecord(contract(enabled=True, legal_reviewed=True)))
    active = registry.activate("greenhouse:example")
    assert active.lifecycle is SourceLifecycle.ACTIVE
    assert registry.ingestion_allowed("greenhouse:example") is True
    suspended = registry.suspend("greenhouse:example")
    assert suspended.lifecycle is SourceLifecycle.SUSPENDED
    assert registry.ingestion_allowed("greenhouse:example") is False


def test_retirement_disables_contract_and_is_terminal() -> None:
    registry = SourceRegistry()
    registry.register(SourceRecord(contract(enabled=True, legal_reviewed=True)))
    retired = registry.retire("greenhouse:example")
    assert retired.lifecycle is SourceLifecycle.RETIRED
    assert retired.contract.enabled is False
    with pytest.raises(ValueError, match="retired"):
        registry.activate("greenhouse:example")


def test_health_events_require_aware_timestamps() -> None:
    registry = SourceRegistry()
    registry.register(SourceRecord(contract()))
    healthy = registry.record_success("greenhouse:example", datetime(2026, 10, 3, tzinfo=UTC))
    assert healthy.health is SourceHealth.HEALTHY
    assert healthy.last_success_at is not None
    with pytest.raises(ValueError, match="timezone-aware"):
        registry.record_failure("greenhouse:example", datetime(2026, 10, 3))


def test_duplicate_registration_is_rejected() -> None:
    registry = SourceRegistry()
    record = SourceRecord(contract())
    registry.register(record)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(record)
