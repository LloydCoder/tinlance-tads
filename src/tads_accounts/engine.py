"""Evidence-preserving account state derivation."""

from collections.abc import Sequence

from .models import AccountSignal, AccountState


class AccountIntelligenceEngine:
    def __init__(self, state_version: str = "m6-v1"):
        self.state_version = state_version

    def derive(
        self, account_id: str, signals: Sequence[AccountSignal], *, momentum: float = 0.0
    ) -> AccountState:
        if not account_id:
            raise ValueError("account_id is required")
        if not 0 <= momentum <= 1:
            raise ValueError("momentum must be between 0 and 1")
        if not signals:
            return AccountState(
                account_id,
                0.0,
                0.0,
                momentum,
                0.0,
                0.0,
                0,
                self.state_version,
                ("no active signals",),
            )
        quality = sum(s.quality for s in signals) / len(signals)
        kinds = {s.kind for s in signals}
        negative = sum(1 for s in signals if s.direction < 0) / len(signals)
        confidence = sum(s.freshness for s in signals) / len(signals)
        evidence_ids = tuple(
            sorted({evidence_id for signal in signals for evidence_id in signal.evidence_ids})
        )
        drivers = tuple(
            sorted(
                {f"{s.kind}:quality={s.quality:.2f}" for s in signals if s.direction > 0},
                reverse=True,
            )[:5]
        ) or ("no positive drivers",)
        return AccountState(
            account_id,
            round(quality, 6),
            round(len(kinds) / len(signals), 6),
            round(momentum, 6),
            round(negative, 6),
            round(confidence, 6),
            len(signals),
            self.state_version,
            drivers,
            evidence_ids,
        )
