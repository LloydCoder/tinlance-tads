"""Bounded buying-window lifecycle without purchase-intent claims."""

from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum


class BuyingWindowState(StrEnum):
    EMERGING = "emerging"
    ACTIVE = "active"
    COOLING = "cooling"
    DORMANT = "dormant"
    INVALIDATED = "invalidated"


@dataclass(frozen=True, slots=True)
class BuyingWindow:
    window_id: str
    account_id: str
    state: BuyingWindowState
    opened_at: datetime
    expires_at: datetime
    evidence_ids: tuple[str, ...]
    trigger_ids: tuple[str, ...]
    is_purchase_intent_claim: bool = False

    def validate(self) -> None:
        if not self.window_id or not self.account_id:
            raise ValueError("buying window identifiers are required")
        if not self.evidence_ids or not self.trigger_ids:
            raise ValueError("buying window requires evidence and triggers")
        if self.opened_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise ValueError("buying window timestamps must be timezone-aware")
        if self.expires_at <= self.opened_at:
            raise ValueError("buying window must expire after it opens")
        if self.is_purchase_intent_claim:
            raise ValueError("buying windows cannot claim purchase intent")

    def transition(self, state: BuyingWindowState, at: datetime) -> "BuyingWindow":
        self.validate()
        if at.tzinfo is None:
            raise ValueError("transition timestamp must be timezone-aware")
        if at < self.opened_at:
            raise ValueError("transition cannot precede window opening")
        if self.state is BuyingWindowState.INVALIDATED:
            raise ValueError("invalidated buying windows are terminal")
        if state is BuyingWindowState.INVALIDATED:
            return replace(self, state=state)
        if at >= self.expires_at:
            return replace(self, state=BuyingWindowState.DORMANT)
        return replace(self, state=state)
