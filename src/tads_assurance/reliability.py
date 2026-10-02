"""M15 deterministic retry/idempotency policy."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.base_delay_seconds <= 0 or self.max_delay_seconds < self.base_delay_seconds:
            raise ValueError("retry delays are invalid")

    def delay(self, attempt: int) -> float:
        if attempt < 1:
            raise ValueError("attempt must be positive")
        return float(min(self.max_delay_seconds, self.base_delay_seconds * (2 ** (attempt - 1))))

    def should_retry(self, attempt: int) -> bool:
        return 1 <= attempt < self.max_attempts


@dataclass(frozen=True, slots=True)
class ReliabilityPolicy:
    max_in_flight: int = 32
    queue_capacity: int = 1000
    failure_threshold: int = 5
    recovery_seconds: float = 30.0

    def validate(self) -> None:
        if self.max_in_flight < 1 or self.queue_capacity < self.max_in_flight:
            raise ValueError("reliability capacity bounds are invalid")
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold must be positive")
        if self.recovery_seconds <= 0:
            raise ValueError("recovery_seconds must be positive")


@dataclass(frozen=True, slots=True)
class IdempotencyPolicy:
    key_max_length: int = 256
    required: bool = True

    def validate(self, key: str | None) -> None:
        if self.required and (key is None or not key.strip()):
            raise ValueError("idempotency key is required")
        if key is not None and len(key) > self.key_max_length:
            raise ValueError("idempotency key exceeds maximum length")
