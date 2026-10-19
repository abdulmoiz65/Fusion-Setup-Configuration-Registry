# Dependency Readiness

Resolve option identity, SITE eligibility, lookup values, cross-option prerequisites, and package readiness before preview.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fixed task and environment | Resolve one target and the exact catalog task |
| 2 | Profile definition and SITE value | Confirm exact inventory membership, application id, SITE eligibility, and current value |
| 3 | Stored-value authority | Resolve an active lookup code or apply the documented numeric contract |
| 4 | Cross-option prerequisites | Validate the proposed set as a whole, not row by row in isolation |
| 5 | FSM artifact or direct-update target | Bind exact bytes or exact SITE target to the preview |
| 6 | Executor approval | Use Core Data Loader approval for import or exact Apps Common approval for update_one |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CDMO.PROFILE | Exact profile definition and SITE record | Yes | Every option view or change | Verify | Live profileOptions definition and children | read_cdm_option_definition | Prevents wrong code, level, application id, and stale current value | Select only a setting exposed by this task | ApplicationId, current value, SITE eligibility, SITE key |
| CDMO.LOOKUP | Active stored lookup code | Conditional | SqlValidation names one lookup type | Lookup | Live standard lookup codes | resolve_cdm_option_lookup_code | UI meanings are not safe CSV values | Use the exact active stored code shown in preview | LookupCode, Meaning |
| CDMO.SOURCE_TRACKING | Attribute source tracking | Conditional | Attribute selection is ORA_ZCH_SC_OLDEST or ORA_ZCH_SC_NEWEST | Verify | Proposed and current task option set | read_cdm_option_definition | Source-confidence selection requires tracking | Include ZCH_ENABLE_SURVIVORSHIP=Y | Source tracking result |
| CDMO.RESTRICTED_SCOPE | Compatible restricted merge design | Conditional | ORA_ZCH_MERGE_SCOPE=CDM_HV | Verify | Proposed and current task option set | read_cdm_option_definition | Restricted scope cannot invoke incompatible business or Groovy rules | Choose compatible master, attribute, and agreement settings | Compatibility result |
| CDMO.FSM_BASELINE | Immutable exact-task ZIP and existing profile row | Conditional | Prepare_import or import | Satisfied | Task-level export and local ZIP validation | | Prevents fabricated rows and package drift | Export the task and preserve the original | ZIP path, SHA-256, row identity |
| CDMO.APPROVAL | Executor-owned exact approval | Yes | Import or update_one | Blocked | Core Data Loader or Apps Common preview | | Approval must match the exact target and content | Approve only the latest unchanged preview | Approval fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All mandatory facts and applicable conditional dependencies pass | Yes for read-only lookups; no create |
| Lookup | A live profile definition or lookup code must be read | Yes, read-only only |
| Blocked | Identity, SITE eligibility, value, package row, compatibility, or approval is missing or invalid | No |
| Export discrepancy | A documented live profile is missing from the completed FSM export | Yes for read-only profile verification; never create an FSM row |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDMO.DEPENDENCY_READINESS | decision | 4 | resolve_dependency | satisfied->CDMO.APPLY_DEFAULT;blocked->CDMO.ERROR | CDMO.RESOLVE_STORED_VALUE | stop | Before default evaluation, design review, preview, approved execution, or status continuation |
