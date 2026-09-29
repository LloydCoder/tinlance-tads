"""Fail-closed runtime health/readiness contract."""

from dataclasses import dataclass
from enum import StrEnum


class ComponentHealth(StrEnum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


@dataclass(frozen=True, slots=True)
class RuntimeReadiness:
    database: ComponentHealth
    migrations: ComponentHealth
    ingestion: ComponentHealth
    integrations: ComponentHealth

    @property
    def ready(self) -> bool:
        return all(
            component is ComponentHealth.HEALTHY
            for component in (self.database, self.migrations, self.ingestion, self.integrations)
        )
