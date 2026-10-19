# Benefit Regulations Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
| --- | --- | --- |
| 1 | Active Run Book | Confirm an active project Run Book before a data-changing action |
| 2 | Current HDL sample | Retrieve the current `benefitRegulations` sample and confirm date-effectivity, effectiveOf availability, and operation support for each included section |
| 3 | Resolved date-effective row | Confirm identity, applicable slice, and derived `effectiveOf` |
| 4 | Data Loader preflight | Validate the immutable DAT or ZIP with `core.data-loader` |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| active_runbook | Active Run Book | Yes | Any mutation | Verify | Project Run Book state | | Binds the load to its implementation task | Select and activate the Run Book | Run Book context |
| current_hdl_sample | Current HDL sample | Yes | Before derivation or any mutation | Verify | `core.data-loader` sample retrieval | | Establishes supported headers, actions, keys, and each included section's date-effective contract | Retrieve and review per-section metadata; stop on missing or ambiguous date-effectivity or effectiveOf availability | Sample reference, version, and per-section contract |
| resolved_effective_context | Resolved identity and date-effective context | Yes | Non-create operation | Verify | Validated request and current sample | | Prevents a mutation against an unintended slice | Provide exact identity, applicable date, and derived `effectiveOf` | Identity, slice date, derived value |
| validated_hdl_artifact | Immutable HDL artifact | Yes | Any mutation | Verify | `core.data-loader` preflight | | Prevents a changed or malformed submission | Preflight the final archive | Artifact checksum and path |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BEN_REG.CHECK_READINESS | decision | 30 | resolve_dependency | ready->BEN_REG.ENFORCE_DESIGN;missing->BEN_REG.HANDLE_ISSUE | BEN_REG.APPLY_DEFAULTS | stop | Verify Run Book, current sample, date-effective context, and immutable artifact |
