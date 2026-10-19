# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task capability | Confirm the selected task code and task-native FSM artifact. |
| 2 | Geography evidence | Confirm the authoritative geography tuple and immediate parent for every node. |
| 3 | Country structure evidence | Confirm the current country-level mapping supports the node levels. |
| 4 | Package validation | Validate the final immutable ZIP and retain the result. |
| 5 | Import approval | Bind explicit approval to the exact ZIP and target environment immediately before import. |
| 6 | Result evidence | Retain the detailed FSM process-log result and post-import verification evidence. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| GHH.GEOGRAPHY_EVIDENCE | Authoritative node tuples | Yes | Every package | Verify | Authoritative source evidence supplied with the request | | The task must not infer master geography identity or parentage | Provide exact elements, identifiers, and immediate parents | Node values and parent relationships |
| GHH.STRUCTURE_EVIDENCE | Current country-level structure evidence | Yes | Every package | Verify | Approved country structure evidence supplied with the request | | Nodes must align with the country mapping | Provide the applicable country-level mapping evidence | Supported level mapping |
| GHH.PACKAGE | Validated immutable ZIP | Yes | Import request | Verify | Package validation result | | Approval must identify the exact artifact | Validate the final ZIP before seeking approval | ZIP fingerprint and validation result |
| GHH.APPROVAL | Fresh import approval | Yes | Import request | Verify | Explicit user approval | | Import changes Fusion setup data | Approve the exact ZIP and target environment immediately before import | Target environment and ZIP fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All mandatory evidence is present and consistent | No |
| Blocked | Any geography, structure, package, or approval evidence is absent | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHH.READINESS | decision | 20 | resolve_dependency | ready->GHH.DEFAULTS;blocked->GHH.DEPENDENCY_ISSUES | GHH.VALIDATE | stop | Input validation passed |
