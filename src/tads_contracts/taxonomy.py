"""Stable M0 enumerations. Values are API/storage identifiers."""

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
    IGNORE = "ignore"
    MONITOR = "monitor"
    RESEARCH = "research"
    ENRICH = "enrich"
    QUEUE_FOR_FADEREACH = "queue_for_fadereach"
    REQUEST_HUMAN_REVIEW = "request_human_review"
    CREATE_OPPORTUNITY = "create_opportunity"
    EXPAND_RESEARCH = "expand_research"


class ResolutionState(StrEnum):
    MATCHED = "matched"
    PROBABLE = "probable"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"
