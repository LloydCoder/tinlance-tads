"""Evidence-first deterministic signal classification."""

from dataclasses import dataclass
from typing import Any

from .models import DetectedSignal, SignalKind, SignalState


@dataclass(frozen=True, slots=True)
class SignalDetector:
    """Classifies only observed facts; it never infers purchase intent."""

    taxonomy_version: str = "m4-v1"

    def detect(
        self,
        observation_id: str,
        payload: dict[str, Any],
        evidence_ids: tuple[str, ...],
    ) -> tuple[DetectedSignal, ...]:
        if not evidence_ids:
            raise ValueError("signal detection requires evidence")
        provider = str(payload.get("provider", ""))
        title = str(payload.get("title") or payload.get("text") or "")
        text = str(payload.get("content") or payload.get("description_plain") or "")
        haystack = f"{title} {text}".casefold()
        signals: list[DetectedSignal] = []

        if provider in {"greenhouse", "lever"}:
            strength = (
                0.75
                if any(
                    token in haystack
                    for token in ("security", "application security", "devsecops")
                )
                else 0.55
            )
            signals.append(
                DetectedSignal(
                    SignalKind.HIRING,
                    "job_posting",
                    SignalState.VALIDATED,
                    strength,
                    1.0,
                    0.9,
                    observation_id,
                    evidence_ids,
                    ("structured hiring source", "observed job posting"),
                )
            )
            if any(token in haystack for token in ("security", "devsecops", "cloud security")):
                signals.append(
                    DetectedSignal(
                        SignalKind.SECURITY,
                        "security_hiring",
                        SignalState.VALIDATED,
                        0.85,
                        1.0,
                        0.9,
                        observation_id,
                        evidence_ids,
                        ("security-related hiring language observed",),
                    )
                )
        return tuple(signals)
