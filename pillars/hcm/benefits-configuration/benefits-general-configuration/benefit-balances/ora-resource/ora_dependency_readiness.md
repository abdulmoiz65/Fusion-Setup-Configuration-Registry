# Benefit Balances Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Benefit Reporting Groups | Confirm the preceding catalog task is addressed where the implementation design requires reporting groups. |
| 2 | Source prerequisites | Confirm current, authoritative balance name, legal employer, and all current-sample-required configuration facts for each DAT record. |
| 2a | Per-section effective contract | Confirm date-effectivity, effectiveOf availability, and supported operations for every included section from the current Data Loader sample before derivation. |
| 2b | Supplied reference values | Run the four conditional, read-only LOV checks when the active workflow selects them; retain unverified_forbidden on 403. |
| 3 | Run Book and Data Loader preflight | Activate the Run Book and validate the immutable benefitBalances DAT through core.data-loader. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| benefit_reporting_groups | Benefit Reporting Groups | Conditional | The balance design references a reporting group | Verify | Approved benefits design | | Preserves catalog order and design consistency | Resolve the reporting-group dependency before preflight | Reporting group reference |
| source_prerequisites | Balance name, legal employer, and current-sample-required configuration facts | Yes | Create or merge, Update, or Delete | Verify | Authoritative implementation source and current sample | | Prevents a load that cannot be reconciled to the intended benefits configuration | Correct missing or ambiguous source facts | Current-schema record values |
| section_effective_contract | Date-effectivity, effectiveOf availability, and supported row operations for each included section | Yes | DAT preparation | Verify | Current core.data-loader sample and section metadata | | Prevents applying parent or sibling effective context to a section that does not support it | Confirm each section separately; stop on missing or ambiguous metadata | Per-section effective contract |
| supplied_reference_values | Balance usage, nonmonetary unit, legal employer, and currency names | Conditional | A benefitBalances row supplies any named field | Verify | Selected read-only REST LOVs or another workflow-approved authoritative check | | Distinguishes invalid values from access-denied checks | Run each applicable resolver; retain 403 as unverified_forbidden without failing field validation | Per-row field validation status |
| active_runbook | Active Run Book | Yes | Create or merge, Update, or Delete | Verify | Project Run Book state | | Associates the load with its approved implementation workflow | Create or select and activate a Run Book | Run Book context |
| validated_hdl_artifact | Validated HDL artifact | Yes | Create or merge, Update, or Delete | Verify | core.data-loader preflight | | Prevents a changed or malformed DAT submission | Preflight the immutable artifact | Artifact checksum and path |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All mandatory dependencies are verified | No |
| Missing | A prerequisite, Run Book, or validated artifact is absent or ambiguous | No |
| Approval blocker | A data-changing action lacks current approval | No |
| unverified_forbidden | A supplied reference field's lookup returned 403 | Continue independent validation; obtain authoritative verification before live load |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_BAL.CHECK_READINESS | decision | 20 | resolve_dependency | ready->BEN_BAL.LOOKUP_USAGE;missing->BEN_BAL.HANDLE_ISSUE | BEN_BAL.VALIDATE_REQUEST | stop | Verify prerequisites, active Run Book, and immutable Data Loader preflight readiness |
