from tads_resolution import EntityResolver
from tads_resolution.models import ResolutionState
from tads_resolution.normalization import normalize_domain, normalize_name
from tads_resolution.resolver import OrganizationRecord


def resolver() -> EntityResolver:
    return EntityResolver(
        [
            OrganizationRecord(
                "org-acme", "Acme Corporation", ("acme.example",), ("Acme Corp",)
            ),
            OrganizationRecord(
                "org-echo", "Acme Holdings", ("holdings.example",), ("Acme Group",)
            ),
        ]
    )


def test_normalization_is_conservative() -> None:
    assert normalize_name("ACME, Inc.") == "acme"
    assert normalize_domain("https://www.Acme.Example/jobs") == "acme.example"


def test_exact_domain_matches_canonically() -> None:
    result = resolver().resolve("Acme", "https://acme.example")
    assert result.state is ResolutionState.MATCHED
    assert result.selected_organization_id == "org-acme"


def test_ambiguous_names_do_not_silently_merge() -> None:
    result = resolver().resolve("Acme", None)
    assert result.state is ResolutionState.AMBIGUOUS
    assert result.selected_organization_id is None


def test_unknown_entity_is_explicit() -> None:
    result = resolver().resolve("Unrelated Company", "unknown.example")
    assert result.state is ResolutionState.UNRESOLVED
