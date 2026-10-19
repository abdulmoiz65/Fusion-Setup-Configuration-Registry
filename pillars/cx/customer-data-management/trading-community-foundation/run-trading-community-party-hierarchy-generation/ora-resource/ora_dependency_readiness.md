# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion target | Resolve exactly one configured environment before the consolidated approval and any live lookup, tracking, or submission. Select it automatically when exactly one is configured. |
| 2 | Supported parameter combination | Require one documented hierarchy type and one documented flattening method, using their declared argument1 and argument4 transport values. |
| 3 | Hierarchy scope | Preserve supplied hierarchy name as argument2 and supplied Version as argument3; when omitted, show all-hierarchy scope and active/default version in the consolidated confirmation and omit the applicable transport value. |
| 4 | ESS transport contract | Use application CrmEss, the declared jobDefinitionId, four ordered STRING parameters named submit.argument1 through submit.argument4, retries 0, and separate requestId polling. |
| 5 | Durable submission checkpoint | Require project_id, immutable preview, correlation description, target identity, and a separate submit-only checkpoint before polling. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PHG.ENV | Fusion environment | Yes | Consolidated approval, live lookup, tracking, or submission | Satisfied only when exactly one configured environment is resolved | Configured environment context |  | Prevent cross-environment resolution or submission without creating a redundant approval | Automatically use the sole configured target; request selection only when none or multiple are resolvable | Environment identity |
| PHG.TYPE_TRANSPORT | Party hierarchy type transport | Yes | Live execution | Satisfied for CUSTOMER, DUNS_AND_BRADSTREET, PARTNER, and TRADING_COMMUNITY_PARTY | CUSTOMER maps to HZ_CUSTOMER_HIERARCHY; DUNS_AND_BRADSTREET maps to HZ_DNB_HIERARCHY; PARTNER maps to HZ_PARTNER_HIERARCHY; TRADING_COMMUNITY_PARTY maps to HZ_PARTY_HIERARCHY |  | Prevent display labels or guessed codes from entering argument1 | Select one documented hierarchy type | argument1 transport value |
| PHG.METHOD_TRANSPORT | Flattening method transport | Yes | Live execution | Satisfied for INCREMENTAL and FORCE | INCREMENTAL maps to INCREMENTAL_FLATTENING; FORCE maps to FORCE_FLATTENING |  | Prevent display labels or guessed codes from entering argument4 | Select Incremental or explicitly select Force | argument4 transport value |
| PHG.SCOPE | Hierarchy name/version transport | Yes | Every preview | Satisfied for preview when exact supplied values or documented omitted-value behavior is shown; live submission additionally requires the consolidated confirmation | argument2 exact hierarchy-name text or omitted value; argument3 exact user-supplied Version value or omitted value |  | Preserve the business inputs without exposing transport terminology or adding an optional-field question round | Confirm the displayed all-hierarchy scope in the single consolidated execution approval when name is omitted | argument2 and argument3 values |
| PHG.ESS_CONTRACT | Party Hierarchy Generation ESS transport contract | Yes | Any live submission or task-specific request tracking | Satisfied for every documented type and method combination | Application CrmEss; declared jobDefinitionId; submit.argument1-submit.argument4; STRING types; complete hierarchy-type and flattening-method mappings; exact user-supplied Version value; retries 0; UI success evidence; separate polling |  | Reuse the established repository ESS payload and safety convention without relying on undocumented compatibility | Submit through core.fusion-api.ess-job-submitter | Exact executable payload and requestId checkpoint policy |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact environment and source-backed contract values are present | Read-only lookup only where documented; no create |
| Unsupported | A requested hierarchy type or method is outside the documented option set | No |
| Blocked | A required target or known mapping is absent or ambiguous | No |
| Approval Blocker | The single consolidated submission approval is absent, stale, or not bound to the exact target and immutable preview | No until one exact approval is bound to every execution detail |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PHG.DEPENDENCY_READINESS | decision | 3 | resolve_dependency | satisfied->PHG.DESIGN_GATE;blocked->PHG.RETURN_ISSUES | PHG.APPLY_DEFAULTS | stop | Before presenting execution readiness or tracking an existing request as this task. |
