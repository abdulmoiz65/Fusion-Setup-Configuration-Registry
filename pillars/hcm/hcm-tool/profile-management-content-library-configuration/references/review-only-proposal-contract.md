# Complete Review-Only Proposal Contract

## Purpose

Define the canonical supplied-configuration output required before provider
work. The proposal is immutable, review-only, and terminal. It cannot create a
package or change Fusion.

## Required Sections

Every proposal must include all sections below, even when a section contains `not-applicable`, `evidence-unavailable`, or a blocker.

| Section | Required content |
|---|---|
| request_identity | Project ID, complete-set ID, proposal status, and proposal schema version |
| source | Input method, sanitized source filename, source fingerprint, sheet/row references when available, and source preservation statement |
| optional_business_context | Backward-compatible optional container for context the user volunteered; never required or used to infer task ownership or missing values |
| confirmed_scope | Selected task names/codes, confirmation evidence, and complete-set boundary |
| assumption_ledger | Proposed technical mappings and unresolved required fields with source, sanitized evidence, confidence, materiality and review status; no invented optional values |
| values_and_provenance | Every supplied, inferred, confirmed, blocked, and not-applicable material value with owning task, source, sanitized evidence, confidence, materiality, review status, and exact source reference |
| mappings_and_omissions | Normalized-to-task mappings, mapping readiness, omitted source values, unavailable technical fields, and reasons |
| validation | Field, identity, uniqueness, sequence, date, parent-child, endpoint, and scope-boundary results |
| dependencies | Parent, endpoint, Rating Model, lookup, value-set, profile-option, and provider dependency results |
| exact_match_results | One supported exact-key result per independently identifiable parent/child using exact, not-found, multiple-exact or evidence-unavailable; retain actual matched identifiers and source references, including customer/seeded origin when applicable; no similarity or reuse analysis |
| references | Sanitized source, documentation, catalog, export, and lookup evidence references with freshness where applicable |
| exclusions | Rating Models, Profile Types, Content Sections, profile instances, downstream configuration, unsupported bulk routes, and any routed-away scope |
| provider_readiness | Per-task proposal status plus separate create-only package eligibility; proposal review never authorizes package construction or mutation |
| approval_separation | Statement that proposal review and `Prepare configuration` authorize only local proposal refinement |
| fingerprints | Source fingerprint, normalized-input fingerprint, evidence fingerprints, and proposal fingerprint |
| safe_next_action | Exactly one review or evidence-resolution action; never a Fusion mutation |

## Canonical Fingerprint Input

Compute SHA-256 over canonical UTF-8 JSON using sorted object keys and compact separators. Fingerprint only the material proposal body:

```text
request_identity
source
optional_business_context
confirmed_scope
assumption_ledger
values_and_provenance
mappings_and_omissions
validation
dependencies
exact_match_results
references
exclusions
provider_readiness
approval_separation
```

Do not include the fingerprint field itself, presentation timestamps, transient file paths, or reviewer comments. Any material change creates a new proposal fingerprint and invalidates prior confirmation.

## Completion Rules

- A preliminary proposal may be `review-ready` when the supplied object scope
  is unambiguous, all supplied values are represented, and unresolved mappings
  or required values remain visible in the assumption ledger.
- A proposal is `configuration-ready` only after technical normalization and
  review of every material assumption.
- Missing field contracts, dependencies, or current evidence remain visible blockers; they must never disappear from the output.
- CSV intake review must include both `records` and `unmapped_records`, retaining
  every supplied value and source row. An unmapped row has an unresolved owning
  task, not an inferred one. Reconcile their combined nonblank count against
  `source_record_count`; an unknown count or unresolved row prevents any claim
  of a complete configuration-ready set and blocks downstream exact/package work.
- One exact duplicate stops creation for that independently identifiable record and displays its actual matched identifier without a reuse recommendation.
- Keep the canonical proposal classification as `exact`. When the fresh-customer-first overlay resolves a Content Type or Content Item, record `customer` or `seeded` separately as the match/evidence source; do not add source-specific values to the proposal classification enum.
- Compare case or normalization only according to the provider's declared exact semantics. Do not display fuzzy, near-match or intelligent reuse warnings. Preserve real provider Name/code collision guards.
- A proposal with `evidence-unavailable` cannot claim a value is new.
- Provider readiness may report `eligible-for-separate-package-review` only for
  Content Types, Content Items, catalog-only or phase-one anchored Content Item
  Catalogs, or the separate controlled-certification new-catalog portable-child
  set under the [new-set contract](new-catalog-set-contract.md), or Educational
  Establishments when every requirement in the approved
  create-only FSM import contract is met, or for the explicitly selected verified
  GOAL exception when every requirement in its [isolated fallback contract](verified-fallback-contract.md)
  is met. GOAL eligibility is separate from combined FSM preview readiness and
  original FSM-only acceptance; it does not authorize package construction or a
  load. Missing selection, complete-request, lifecycle, target, evidence or
  exact-identifier gates remain `blocked`; every other unsupported route remains
  `unsupported`.
- New-set eligibility is single-task and non-production only, never inherited
  from the anchored-child certification or a canonical mixed-task preview.
  Preserve unsupported supplied rows; proposal review cannot trim the request
  or authorize either package preparation or submission.
- Proposal confirmation cannot transition to package construction, creation, import, update, merge, delete, end-date, or auto-correction.

## Required Review Text

End every user-facing proposal with an equivalent statement:

```text
Prepare configuration means refine and persist this local review-only proposal only.
It does not authorize package construction, a Fusion create/import, or another provider operation.

Prepare configuration | Review assumptions
```

## Synthetic Golden Scenario

The repository fixture `tests/fixtures/complete-review-only-proposal.json` demonstrates the complete contract with synthetic values only. It is local regression evidence; it does not establish live acceptance and is not a provider payload.
