"""Deterministic registry for versioned TADS agent specifications."""

from collections.abc import Iterable

from .models import AgentSpec


class AgentRegistry:
    def __init__(self, specs: Iterable[AgentSpec] = ()):
        self._specs: dict[str, AgentSpec] = {}
        for spec in specs:
            self.register(spec)

    def register(self, spec: AgentSpec) -> None:
        spec.validate()
        if spec.name in self._specs:
            raise ValueError(f"agent already registered: {spec.name}")
        self._specs[spec.name] = spec

    def get(self, name: str) -> AgentSpec:
        return self._specs[name]

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._specs))
