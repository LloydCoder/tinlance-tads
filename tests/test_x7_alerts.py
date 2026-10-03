import pytest

from tads_alerts import Alert, AlertRegistry, Watch, WatchTarget


def watch() -> Watch:
    return Watch("watch-1", "tenant-1", WatchTarget.ACCOUNT, "acct-1")


def alert(*, materiality: float = 0.8, dedupe_key: str = "change-1") -> Alert:
    return Alert("alert-1", "watch-1", materiality, ("ev-1",), dedupe_key)


def test_only_material_alerts_are_emitted() -> None:
    registry = AlertRegistry(minimum_materiality=0.5)
    registry.add_watch(watch())
    assert registry.emit(alert(materiality=0.49)) is False
    assert registry.emit(alert(materiality=0.8)) is True
    assert len(registry.alerts()) == 1


def test_alerts_are_deduplicated() -> None:
    registry = AlertRegistry()
    registry.add_watch(watch())
    assert registry.emit(alert()) is True
    assert registry.emit(Alert("alert-2", "watch-1", 0.9, ("ev-2",), "change-1")) is False


def test_alert_requires_known_watch() -> None:
    registry = AlertRegistry()
    with pytest.raises(ValueError, match="watch"):
        registry.emit(alert())


def test_watch_and_alert_require_evidence() -> None:
    registry = AlertRegistry()
    registry.add_watch(watch())
    with pytest.raises(ValueError, match="evidence"):
        registry.emit(Alert("alert-1", "watch-1", 0.8, (), "change-1"))
