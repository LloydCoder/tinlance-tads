"""Explainable opportunity scoring; never predicts purchase."""

from dataclasses import dataclass

from .models import ICPProfile, OpportunityResult


@dataclass(frozen=True, slots=True)
class OpportunityEngine:
    score_version: str = "m7-v1"

    def evaluate(
        self,
        account_id: str,
        *,
        industry: str | None,
        geography: str | None,
        employees: int | None,
        capabilities: set[str],
        signal_strength: float,
        momentum: float,
        negative_evidence: float,
        data_confidence: float,
        profile: ICPProfile,
        evidence_ids: tuple[str, ...],
    ) -> OpportunityResult:
        if not account_id:
            raise ValueError("account_id is required")
        if not evidence_ids or any(not item for item in evidence_ids):
            raise ValueError("opportunity evaluation requires evidence")
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("opportunity evidence identifiers must be unique")
        values = (signal_strength, momentum, negative_evidence, data_confidence)
        if any(value < 0 or value > 1 for value in values):
            raise ValueError("score inputs must be between 0 and 1")
        if employees is not None and employees < 0:
            raise ValueError("employee count cannot be negative")
        fit_parts = [
            bool(industry and industry.casefold() in {x.casefold() for x in profile.industries}),
            bool(geography and geography.casefold() in {x.casefold() for x in profile.geographies}),
            employees is not None and employees >= profile.min_employees,
            profile.max_employees is None
            or (employees is not None and employees <= profile.max_employees),
            profile.required_capabilities.issubset(capabilities),
        ]
        icp_fit = sum(fit_parts) / len(fit_parts)
        score = max(
            0.0,
            min(
                1.0,
                0.30 * icp_fit
                + 0.30 * signal_strength
                + 0.20 * momentum
                + 0.10 * data_confidence
                - 0.10 * negative_evidence,
            ),
        )
        confidence = data_confidence * (0.5 + 0.5 * icp_fit)
        reasons = tuple(
            item
            for item in (
                "ICP industry match" if fit_parts[0] else "",
                "ICP geography match" if fit_parts[1] else "",
                "employee-range fit" if fit_parts[2] and fit_parts[3] else "",
                "required capabilities present" if fit_parts[4] else "",
                "recent signal momentum" if momentum >= 0.5 else "",
            )
            if item
        ) or ("insufficient positive evidence",)
        unknowns = tuple(
            item
            for item in (
                "industry" if industry is None else "",
                "geography" if geography is None else "",
                "employee count" if employees is None else "",
            )
            if item
        )
        recommendation = (
            "CREATE_OPPORTUNITY"
            if score >= 0.7 and confidence >= 0.6
            else "RESEARCH"
            if score >= 0.45
            else "MONITOR"
        )
        hypothesis = (
            "Observed evidence indicates this account may warrant Tinlance attention; "
            "the score is not a prediction of purchase."
        )
        return OpportunityResult(
            account_id,
            round(icp_fit, 6),
            round(signal_strength, 6),
            round(momentum, 6),
            round(negative_evidence, 6),
            round(score, 6),
            round(confidence, 6),
            hypothesis,
            recommendation,
            reasons,
            unknowns,
            tuple(evidence_ids),
        )
