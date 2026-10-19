# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope/baseline | Exact target and complete scoped baseline; an empty create baseline is valid, not missing template data |
| 2 | Route/references | Require complete write route for execution; complete supported reference checks and retain nonblocking authority/parity warnings |
| 3 | Intervals/use | Line keys/precedence and protected-use state validate |
| 4 | Preview/approval | Route-specific immutable preview is approved |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RATE.SCOPE | Task/target | Yes | Every request | Verify | Catalog/context | verify_rate_scope | Prevent cross-target write | Supply target | Scope |
| RATE.BASELINE | Full schedule/lines | Yes | Update/copy/delete | Lookup | REST/FSM export | find_rate_schedule | Safe diff/idempotency | Refresh baseline | IDs/rows |
| RATE.CREATE_BASELINE | Complete identity search | Yes | Create | Lookup | Baseline supplied by selected workflow | find_rate_schedule | Prove absence without requiring pre-existing schedules | Accept a complete empty result; missing/incomplete search is unresolved | Existing match or evidenced absence |
| RATE.TEMPLATE | FSM metadata/member/column contract | Conditional | Selected route is FSM CSV | Verify | Fresh template-only export supplied by selected export workflow | verify_rate_route | Build package independently of sample rows | Template-only export is valid; do not demand populated export data or silently export extra data | Exact members/headers/metadata; no borrowed customer rows |
| RATE.ROUTE | Operation/field coverage | Yes | Every write | Verify | Target REST/FSM contract | verify_rate_route | Prevent unsupported write/fallback | Select one route | Route/capabilities |
| RATE.REFERENCES | Subtype dependencies | Conditional | Referenced values | Lookup | Authorities in ora_reference_lookups.md | resolve_rate_references | Prevent proven invalid keys without inventing membership | Accept resolvable code/name/translation/natural-language intent; disclose unsupported checks | Canonical CSV names/codes; eligibility results and warnings |
| RATE.LINES | Intervals/values/precedence | Conditional | Line change | Lookup | Current/request lines | resolve_rate_lines | Prevent ambiguous rate derivation | Correct keys/dates | Canonical lines |
| RATE.USE | Consumer state | Conditional | Protected existing mutation/delete otherwise eligible after baseline checks | Lookup | Target use evidence | resolve_rate_use | Prevent costing/billing disruption | New create needs no prior-use proof; known header-with-children conflict needs no extra use lookup to report rejection | Counts/protection |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All dependencies ready | Yes |
| Missing artifact | Required mutation baseline/capability/use/template absent | No affected mutation; continue independent supported validation |
| REFERENCE_UNRESOLVED | LOV authority or eligibility parity not supported; Warning, blocking=false | Continue all supported lookups/checks and preview without waiver; no substitute export or developer tools |
| Conflict | Immutable header, duplicate/overlap, invalid dependency/value, active use | No |
| Unsupported | No route covers operation/fields or post-approval fallback requested | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE.RESOLVE_DEPENDENCIES | step | 7 | resolve_dependency | ready->RATE.ENFORCE_DESIGN;warning->RATE.ENFORCE_DESIGN;missing->RATE.RETURN_ISSUES;conflict->RATE.RETURN_REFUSAL | RATE.ROUTE_OPERATION | stop | Before preview/validation completes; unresolved LOV warning is not missing mutation artifact |

## Refined Operational Readiness

- **BP-074 — Operational control:** Reconcile employee-rate rows using supported assignment evidence; flag known terminated workers, future-dated assignments, duplicates, overlaps and job-rate equivalence. Do not invent current-date filters or claim reconciliation complete when assignment authority is unavailable. Missing lookup authority warns and continues supported validation/preview; operational readiness remains explicitly unverified.
- **BP-079 — Operational control:** Test derivation for multiple assignments, job fallback, organization fallback, overtime, nonlabor resource, and project/task override scenarios.
