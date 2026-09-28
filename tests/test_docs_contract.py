from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_required_architecture_documents_exist() -> None:
    required = (
        "README.md",
        "docs/architecture/README.md",
        "docs/architecture/data-model.md",
        "docs/security/threat-model.md",
        "docs/data-source-policy.md",
        "docs/implementation-plan.md",
        "docs/architecture/integration-boundaries.md",
        "docs/architecture/migration-baseline.md",
    )
    for path in required:
        assert (ROOT / path).is_file(), path


def test_docs_preserve_core_invariants() -> None:
    architecture = (ROOT / "docs/architecture/README.md").read_text(encoding="utf-8")
    model = (ROOT / "docs/architecture/data-model.md").read_text(encoding="utf-8")
    assert "Evidence invariant" in architecture
    assert "observation" in architecture.lower()
    assert "signal" in architecture.lower()
    assert "OpportunityHypothesis" in model
    assert "Recommendation" in model
