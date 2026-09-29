# CI Security Hardening

TADS CI follows a least-privilege, reproducible workflow model.

## Controls

- Workflow permissions default to contents: read.
- Third-party GitHub Actions are pinned to full commit SHAs.
- Checkout disables credential persistence.
- PostgreSQL integration tests run against a dedicated ephemeral service.
- Static formatting, linting, strict mypy, pip-audit and pytest are mandatory.
- CI is required on pull requests and pushes to main.
- Security-sensitive workflow changes must be reviewed like application code.

GitHub recommends pinning actions to full-length commit SHAs because tags can move; immutable references reduce the supply-chain risk of a compromised action tag.

## Release boundary

CI green means the repository satisfies its automated gates. It does not by itself establish production security, lawful data use, disaster recovery or external-provider readiness. Those remain explicit M13–M18 release gates.
