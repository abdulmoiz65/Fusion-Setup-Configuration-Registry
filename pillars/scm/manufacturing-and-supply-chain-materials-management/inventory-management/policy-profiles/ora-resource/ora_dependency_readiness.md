# Policy Profiles Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Policy Profiles Data Loader metadata | Run the current-environment metadata preflight for registered business object minMaxPolicyProfiles before preparing a Policy Profiles Data Loader operation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| min_max_policy_profiles_metadata | Policy Profiles Data Loader metadata | Yes | Before a Policy Profiles Data Loader operation | Verify | Current-run Data Loader attribute-details preflight for minMaxPolicyProfiles; BO registration was completed by the implementation owner | review_min_max_policy_profiles_metadata | Confirms the registered business object is visible in the configured target environment and provides the current Data Loader contract. | If the preflight is unavailable or fails, correct the environment, registration, or authentication issue and rerun it. Do not construct a direct REST write as a fallback. | metadata_preflight_status; attribute_details_artifact |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verified | The current-run metadata preflight succeeds for minMaxPolicyProfiles. | No create; proceed only with the selected read-only mappings and lookup. |
| Blocked | The metadata preflight is unavailable or fails. | No; stop before preparing a Data Loader operation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PP.CHECK_METADATA | decision | 1 | resolve_dependency | available->PP.SELECT_REQUEST;unavailable->PP.STOP_METADATA | none | stop | Before a Policy Profiles Data Loader operation |
