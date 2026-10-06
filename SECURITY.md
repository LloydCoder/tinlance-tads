# Security Policy

## Reporting a vulnerability

**Do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

Send a private report to **hello@tinlance.com** with:

- a concise vulnerability description;
- affected version, commit, or component;
- reproduction steps or a minimal proof of concept;
- impact and attack prerequisites;
- any relevant logs or screenshots with secrets and personal data removed.

Use the subject line `[TADS SECURITY]` where possible.

If email is unavailable, contact the repository maintainer privately through GitHub and request a private disclosure channel. Do not publish exploit details while a report is being triaged.

## Response targets

These are maintainer response targets, not a guarantee of remediation time:

| Stage | Target |
|---|---:|
| Initial acknowledgement | 3 business days |
| Initial severity/impact assessment | 7 business days |
| Status update for an unresolved report | Every 7 business days |
| Coordinated disclosure decision | Agreed with the reporter after remediation or mitigation |

Critical issues may be handled outside this cadence when operationally necessary.

## Scope

Security reports are especially useful for:

- tenant isolation or authorization bypass;
- SSRF or network-layer escape;
- source-policy bypass;
- secret leakage;
- evidence/provenance tampering;
- unsafe parser or resource-exhaustion paths;
- dependency or CI supply-chain compromise;
- injection and prompt-injection paths;
- privacy or retention-control failures;
- unsafe ReconOS/FadeReach integration behavior.

## Safe testing

Do not:

- access data belonging to other tenants;
- destroy or modify production data;
- perform denial-of-service testing against systems you do not control;
- publish credentials or personal data;
- bypass provider controls merely to test TADS.

Use isolated local fixtures or environments for research.

## Disclosure

Tinlance will coordinate disclosure with the reporter where appropriate. Credit will be offered when requested and when doing so does not create a safety, privacy, legal, or operational concern.

## Security posture

TADS uses defense-in-depth controls including tenant isolation, source authorization, immutable evidence boundaries, restricted network fetching, dependency auditing, least-privilege CI, and fail-closed Enterprise GA gates. See [docs/security/threat-model.md](docs/security/threat-model.md).
