"""Evidence-preserving deterministic entity resolver."""

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable

from .models import Candidate, ResolutionResult, ResolutionState
from .normalization import normalize_domain, normalize_name


@dataclass(frozen=True, slots=True)
class OrganizationRecord:
    organization_id: str
    canonical_name: str
    domains: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()


class EntityResolver:
    def __init__(self, organizations: Iterable[OrganizationRecord]):
        self.organizations = tuple(organizations)

    def resolve(self, name: str | None, domain: str | None) -> ResolutionResult:
        normalized_name = normalize_name(name or "") if name else ""
        normalized_domain = normalize_domain(domain) if domain else None
        candidates: list[Candidate] = []

        for organization in self.organizations:
            canonical = normalize_name(organization.canonical_name)
            aliases = {normalize_name(alias) for alias in organization.aliases}
            domains = {normalize_domain(item) for item in organization.domains}
            domain_exact = normalized_domain is not None and normalized_domain in domains
            alias_exact = normalized_name in aliases if normalized_name else False
            similarity = (
                SequenceMatcher(None, normalized_name, canonical).ratio()
                if normalized_name
                else 0.0
            )
            confidence = min(
                1.0,
                (0.7 if domain_exact else 0.0) + (0.2 if alias_exact else 0.0) + 0.1 * similarity,
            )
            if confidence >= 0.35:
                candidates.append(
                    Candidate(
                        organization.organization_id,
                        organization.canonical_name,
                        next(iter(domains), None),
                        similarity,
                        domain_exact,
                        alias_exact,
                        confidence,
                    )
                )

        candidates.sort(key=lambda item: item.confidence, reverse=True)
        if not candidates:
            result = ResolutionResult(
                ResolutionState.UNRESOLVED, (), None, ("no candidate exceeded threshold",)
            )
        elif len(candidates) > 1 and candidates[0].confidence - candidates[1].confidence < 0.15:
            result = ResolutionResult(
                ResolutionState.AMBIGUOUS,
                tuple(candidates[:5]),
                None,
                ("top candidates are insufficiently separated",),
            )
        elif candidates[0].domain_exact and candidates[0].confidence >= 0.7:
            result = ResolutionResult(
                ResolutionState.MATCHED,
                tuple(candidates[:5]),
                candidates[0].organization_id,
                ("exact domain evidence",),
            )
        elif candidates[0].confidence >= 0.75:
            result = ResolutionResult(
                ResolutionState.PROBABLE,
                tuple(candidates[:5]),
                candidates[0].organization_id,
                ("strong multi-feature match",),
            )
        else:
            result = ResolutionResult(
                ResolutionState.AMBIGUOUS,
                tuple(candidates[:5]),
                None,
                ("candidate confidence is insufficient for automatic merge",),
            )
        result.validate()
        return result
