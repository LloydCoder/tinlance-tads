"""Agent specifications and least-privilege contracts."""

from dataclasses import dataclass
from enum import StrEnum


class AgentRisk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class AgentTool:
    name: str
    purpose: str
    read_only: bool
    allowed_sources: frozenset[str]


@dataclass(frozen=True, slots=True)
class AgentSpec:
    name: str
    purpose: str
    risk: AgentRisk
    tools: tuple[AgentTool, ...]
    required_evidence: bool
    max_steps: int
    requires_human_approval: bool
    prohibited_actions: frozenset[str]
    failure_modes: tuple[str, ...]
    eval_criteria: tuple[str, ...]

    def validate(self) -> None:
        if not self.name or not self.purpose:
            raise ValueError("agent identity and purpose are required")
        if self.max_steps <= 0:
            raise ValueError("agent max_steps must be positive")
        if any(not tool.name or not tool.purpose for tool in self.tools):
            raise ValueError("every agent tool requires a name and purpose")
        if not self.required_evidence:
            raise ValueError("TADS agents require evidence")
        if self.risk is AgentRisk.HIGH and not self.requires_human_approval:
            raise ValueError("high-risk agents require human approval")
        if "send_outreach" not in self.prohibited_actions:
            raise ValueError("TADS agents must prohibit outreach")
