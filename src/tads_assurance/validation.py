"""M13/M17/M18 readiness and assurance gates."""

from dataclasses import dataclass
from enum import StrEnum


class Readiness(StrEnum):
    READY = "ready"
    BLOCKED = "blocked"


class E2EStage(StrEnum):
    SOURCE = "source"
    OBSERVATION = "observation"
    EVENT = "event"
    ENTITY = "entity"
    ACCOUNT = "account"
    SIGNAL = "signal"
    TEMPORAL = "temporal"
    ACCOUNT_STATE = "account_state"
    OPPORTUNITY = "opportunity"
    RECONOS = "reconos"
    FADEREACH = "fadereach"
    OUTCOME = "outcome"
    FEEDBACK = "feedback"


@dataclass(frozen=True, slots=True)
class E2EValidation:
    completed: frozenset[E2EStage]

    def validate(self) -> None:
        missing = set(E2EStage) - set(self.completed)
        if missing:
            raise ValueError(
                "E2E validation is incomplete: "
                + ",".join(sorted(stage.value for stage in missing))
            )


@dataclass(frozen=True, slots=True)
class EnterpriseGate:
    ci_green: bool
    security_green: bool
    tenant_isolation_green: bool
    documentation_reconciled: bool
    e2e_validated: bool
    rollback_tested: bool
    governance_reviewed: bool
    provider_contracts_verified: bool = False
    production_deployed: bool = False
    backup_restore_verified: bool = False
    observability_verified: bool = False
    adversarial_validated: bool = False
    load_tested: bool = False
    disaster_recovery_tested: bool = False
    privacy_reviewed: bool = False
    supply_chain_verified: bool = False

    @property
    def readiness(self) -> Readiness:
        return (
            Readiness.READY
            if all(
                (
                    self.ci_green,
                    self.security_green,
                    self.tenant_isolation_green,
                    self.documentation_reconciled,
                    self.e2e_validated,
                    self.rollback_tested,
                    self.governance_reviewed,
                    self.provider_contracts_verified,
                    self.production_deployed,
                    self.backup_restore_verified,
                    self.observability_verified,
                    self.adversarial_validated,
                    self.load_tested,
                    self.disaster_recovery_tested,
                    self.privacy_reviewed,
                    self.supply_chain_verified,
                )
            )
            else Readiness.BLOCKED
        )


@dataclass(frozen=True, slots=True)
class RuntimeHealth:
    database: bool
    migrations: bool
    source_ingestion: bool
    integrations: bool

    @property
    def readiness(self) -> Readiness:
        return (
            Readiness.READY
            if all((self.database, self.migrations, self.source_ingestion, self.integrations))
            else Readiness.BLOCKED
        )
