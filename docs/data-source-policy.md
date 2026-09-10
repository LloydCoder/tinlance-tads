# TADS Data Source Policy — M0

TADS is designed around legitimate, documented, licensed, or otherwise permitted data access. Source availability is not equivalent to authorization to collect or reuse data.

## Source classes

### Tier A — first-party / authenticated

Tinlance website activity, CRM records, customer-owned integrations, and authenticated provider APIs. These are tenant-scoped and purpose-limited.

### Tier B — public structured APIs / feeds

Examples include Greenhouse Job Board and Lever's public postings surface. Use documented read endpoints and respect provider terms, rate limits, and attribution requirements. Greenhouse documents its Job Board API as a public job-board interface for public jobs; Lever documents a publicly accessible Postings API for published postings. Contracts must be revalidated before production adapters are released.

### Tier C — public web pages

Company sites, press releases, public documentation, public changelogs, investor pages, public status pages, and other pages that are legally and technically permitted to access. Fetch through the controlled crawler boundary and preserve source metadata.

### Tier D — licensed / paid providers

External company, technographic, news, intent, or market datasets may be integrated through adapters. Contracts, permitted uses, retention, redistribution, and geographic restrictions must be recorded in the source registry before activation.

### Prohibited / restricted by default

- Unauthorized automated access to restricted platforms
- Credential-gated data without an authorized integration
- Circumventing access controls, rate limits, robots restrictions, CAPTCHAs, or technical barriers
- LinkedIn scraping or automated activity without explicit authorized access
- Data obtained from leaked, stolen, or unlawfully disclosed sources
- Collection of sensitive personal data without a documented lawful purpose and control

## Source registry requirements

Every source adapter records provider/source name, source class, access mechanism, terms/policy reference, permitted fields, geographic constraints, retention requirements, rate limits, authentication method, reliability profile, legal/privacy review status, and adapter version.

## Personal data

Account intelligence should prefer organization-level evidence. Where person-level data is necessary, apply purpose limitation, data minimization, accuracy, retention limits, access controls, and deletion/objection workflows. Applicable GDPR principles require these controls. A legitimate-interest basis may apply in some direct-marketing contexts, but it requires a balancing assessment and does not automatically authorize upstream collection or override ePrivacy requirements.

## Evidence policy

Source content is evidence only after provenance and extraction validation. Conflicting sources remain conflicting. A model may summarize or interpret evidence but may not invent missing facts.
