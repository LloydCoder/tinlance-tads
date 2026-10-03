"""Material intelligence watches without notification or outreach execution."""

from dataclasses import dataclass
from enum import StrEnum


class WatchTarget(StrEnum):
    ACCOUNT = "account"
    SEGMENT = "segment"
    SIGNAL = "signal"
    OPPORTUNITY = "opportunity"
    BUYING_WINDOW = "buying_window"


@dataclass(frozen=True, slots=True)
class Watch:
    watch_id: str
    tenant_id: str
    target: WatchTarget
    target_id: str

    def validate(self) -> None:
        if not self.watch_id or not self.tenant_id or not self.target_id:
            raise ValueError("watch identifiers are required")


@dataclass(frozen=True, slots=True)
class Alert:
    alert_id: str
    watch_id: str
    materiality: float
    evidence_ids: tuple[str, ...]
    dedupe_key: str

    def validate(self) -> None:
        if not self.alert_id or not self.watch_id or not self.dedupe_key:
            raise ValueError("alert identifiers are required")
        if not 0.0 <= self.materiality <= 1.0:
            raise ValueError("materiality must be within [0, 1]")
        if not self.evidence_ids:
            raise ValueError("alert requires evidence")


class AlertRegistry:
    """Stores watches and material alerts; channel delivery remains external."""

    def __init__(self, minimum_materiality: float = 0.5) -> None:
        if not 0.0 <= minimum_materiality <= 1.0:
            raise ValueError("minimum_materiality must be within [0, 1]")
        self.minimum_materiality = minimum_materiality
        self._watches: dict[str, Watch] = {}
        self._alerts: dict[str, Alert] = {}

    def add_watch(self, watch: Watch) -> None:
        watch.validate()
        if watch.watch_id in self._watches:
            raise ValueError(f"watch already exists: {watch.watch_id}")
        self._watches[watch.watch_id] = watch

    def emit(self, alert: Alert) -> bool:
        alert.validate()
        if alert.watch_id not in self._watches:
            raise ValueError("alert watch does not exist")
        if alert.materiality < self.minimum_materiality:
            return False
        if alert.dedupe_key in {item.dedupe_key for item in self._alerts.values()}:
            return False
        self._alerts[alert.alert_id] = alert
        return True

    def alerts(self) -> tuple[Alert, ...]:
        return tuple(self._alerts.values())
