# Benefit Reporting Groups Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task and environment | Select the catalog task and exact target environment through the project workflow. |
| 2 | Current HDL metadata | Confirm benefitReportingGroups, all supplied child sections, keys, field types, date-effectivity, effectiveOf availability, and supported operations before deriving row controls or authoring an artifact. |
| 3 | Date-effective contract | For each supplied section that exposes effectiveOf, confirm the selected-environment operation and effective-date parameter before derivation; for every other section, omit effectiveOf. |
| 4 | Run Book and loader | Confirm active project Run Book, immutable artifact, selected core.data-loader route, and loader approval workflow before a mutation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| reporting_group_hdl_contract | Selected-environment HDL object and child contract | Yes | Before derivation, artifact construction, or load | Verify | Current core.data-loader metadata | | Prevent guessed parent or child sections and unsupported effectiveOf fields | Confirm every included section's date-effectivity, effectiveOf availability, keys, and supported operations; stop on missing or ambiguous metadata | Confirmed per-section contract |
| reporting_group_effective_date_contract | Date-effective operation and per-row effective-date contract | Yes | A date-effective child row is supplied | Verify | Current core.data-loader metadata and active endpoint contract | | Prevent current-date fallback or a parent/sibling date being used | Confirm the operation and parameter that receives the row's effective date | Confirmed row operation and effective-date parameter |
| reporting_group_runbook | Active matching Run Book and loader route | Yes | Live mutation | Verify | Project state and core.data-loader workflow | | Preserve project execution controls | Activate the Run Book and complete loader preflight | Target and active Run Book reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| ready | All applicable dependencies are confirmed | Read-only lookups may run when selected; mutation still needs loader approval |
| missing | A mandatory selected-environment dependency is absent | No artifact construction or load |
| unverified_forbidden | A supplied reference field received 403 | Continue independent checks; no live load until reference is verified |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_RPTG.CHECK_READINESS | decision | 25 | resolve_dependency | ready->BEN_RPTG.LOOKUP_USAGE;missing->BEN_RPTG.HANDLE_ISSUE | BEN_RPTG.DERIVE_EFFECTIVE_OF | stop | Confirm the selected task, target, date-effective contract, and applicable metadata and Run Book gates |
