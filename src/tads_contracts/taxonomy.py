"""Stable TADS enumerations. Values are API/storage identifiers."""

from enum import StrEnum


class SourceClass(StrEnum):
    FIRST_PARTY = "first_party"
    PUBLIC_STRUCTURED = "public_structured"
    PUBLIC_WEB = "public_web"
    LICENSED = "licensed"


class SignalType(StrEnum):
    COMPANY = "company"
    PEOPLE = "people"
    HIRING = "hiring"
    TECHNOLOGY = "technology"
    PRODUCT = "product"
    SECURITY = "security"
    REGULATORY = "regulatory"
    DIGITAL = "digital"
    COMMERCIAL = "commercial"


class RecommendationAction(StrEnum):
    IGNORE = "IGNORE"
    MONITOR = "MONITOR"
    RESEARCH = "RESEARCH"
    ENRICH = "ENRICH"
    QUEUE_FOR_FADEREACH = "QUEUE_FOR_FADEREACH"
    REQUEST_HUMAN_REVIEW = "REQUEST_HUMAN_REVIEW"
    CREATE_OPPORTUNITY = "CREATE_OPPORTUNITY"
    EXPAND_RESEARCH = "EXPAND_RESEARCH"


class ResolutionState(StrEnum):
    MATCHED = "matched"
    PROBABLE = "probable"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"
