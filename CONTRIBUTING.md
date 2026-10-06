# Contributing to TADS

Thank you for contributing to Tinlance TADS. TADS is a proprietary repository, so contributions are accepted only when the maintainer has authorized the change and the contribution does not disclose confidential information.

## Before you start

1. Read [README.md](README.md) and the relevant architecture documents.
2. For security-sensitive work, read [SECURITY.md](SECURITY.md) and do not disclose vulnerabilities in public issues.
3. Check existing issues and pull requests before starting duplicate work.
4. For architectural changes, update the relevant contract/documentation in the same change.

## Development setup

Requirements:

- Python 3.12+
- PostgreSQL 17+ for database integration tests
- Git

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Set a PostgreSQL connection when running integration tests:

```bash
export DATABASE_URL='postgresql://postgres:postgres@127.0.0.1:5432/tads_test'
```

Run the same gates used by CI:

```bash
python -m ruff format --check src tests
python -m ruff check src tests
python -m mypy
python -m pip_audit --strict
python -m pytest
```

## Branch and pull-request flow

1. Fork the repository if you have been authorized to contribute from a fork.
2. Create a focused branch from `main`.
3. Make the smallest coherent change that satisfies the issue or design decision.
4. Add or update tests for behavior and security invariants.
5. Update documentation and changelog entries when user-visible behavior changes.
6. Run all local quality gates.
7. Push the branch and open a pull request against `main`.
8. Explain the problem, solution, verification, security impact and documentation impact.
9. Address review feedback without rewriting unrelated history.
10. Merge only after required checks and maintainer review are complete.

## Coding standards

- Target Python 3.12+.
- Keep the modular-monolith boundaries explicit.
- Prefer deterministic, replayable domain logic.
- Preserve evidence lineage for material derived intelligence.
- Treat external content and model output as untrusted data.
- Never use model output as authorization.
- Preserve ambiguity rather than making weak identity merges.
- Do not add outreach execution, a generic agent runtime, a CRM, or a second OSINT engine to TADS.
- Keep database changes in forward-only migrations.
- Do not rewrite historical evidence to make a test or evaluation pass.

## Commits

Use concise Conventional Commit-style subjects when practical:

- `feat:` — new behavior
- `fix:` — bug/security correction
- `docs:` — documentation only
- `test:` — tests only
- `refactor:` — behavior-preserving refactor
- `ci:` — CI/tooling
- `chore:` — maintenance

Keep commits reviewable. Do not include secrets, customer data, provider credentials, or generated local artifacts.

## Pull requests

A PR should state:

- what changed;
- why it changed;
- tests and commands run;
- security/privacy implications;
- migration implications;
- documentation changes;
- any remaining environment-dependent release gates.

A green CI run is required but does not by itself establish Enterprise GA.

## License and contribution rights

TADS is proprietary. A pull request does not grant a broad license to the repository contents. Contributions may be accepted only under terms agreed by Tinlance Limited.
