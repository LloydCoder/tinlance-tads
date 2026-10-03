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
        "docs/remaining-phases.md",
        "docs/architecture/integration-boundaries.md",
        "docs/architecture/migration-baseline.md",
        "docs/architecture/source-control-plane.md",
        "docs/architecture/data-quality.md",
        "docs/architecture/signal-operations.md",
        "docs/architecture/change-intelligence.md",
        "docs/architecture/intelligence-graph.md",
        "docs/architecture/buying-windows.md",
        "docs/architecture/alerts.md",
        "docs/architecture/evaluation-platform.md",
    )
    for path in required:
        assert (ROOT / path).is_file(), path


def test_docs_preserve_core_invariants() -> None:
    architecture = (ROOT / "docs/architecture/README.md").read_text(encoding="utf-8")
    model = (ROOT / "docs/architecture/data-model.md").read_text(encoding="utf-8")
    implementation = (ROOT / "docs/implementation-plan.md").read_text(encoding="utf-8")
    assert "Evidence invariant" in architecture
    assert "observation" in architecture.lower()
    assert "signal" in architecture.lower()
    assert "OpportunityHypothesis" in model
    assert "Recommendation" in model
    for phase in ("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"):
        assert phase in implementation
