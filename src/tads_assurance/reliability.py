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
