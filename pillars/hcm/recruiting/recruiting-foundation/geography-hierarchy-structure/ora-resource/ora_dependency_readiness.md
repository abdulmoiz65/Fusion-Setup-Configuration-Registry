# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task capability | Confirm the selected task code and task-native FSM artifact. |
| 2 | Country design evidence | Confirm the approved country and level mapping. |
| 3 | Package validation | Validate the final immutable ZIP and retain the result. |
| 4 | Import approval | Bind explicit approval to the exact ZIP and target environment immediately before import. |
| 5 | Result evidence | Retain the detailed FSM process-log result and post-import verification evidence. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| GHS.COUNTRY_DESIGN | Approved country mapping | Yes | Every package | Verify | Approved design evidence supplied with the request | | The task must not infer a country mapping | Provide the country and approved level mapping | Country code and allowed levels |
| GHS.PACKAGE | Validated immutable ZIP | Yes | Import request | Verify | Package validation result | | Approval must identify the exact artifact | Validate the final ZIP before requesting approval | ZIP fingerprint and validation result |
| GHS.APPROVAL | Fresh import approval | Yes | Import request | Verify | Explicit user approval | | Import changes Fusion setup data | Approve the exact ZIP and target environment immediately before import | Target environment and ZIP fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All mandatory evidence is present and consistent | No |
| Blocked | Any approved mapping, validated ZIP, or fresh approval is absent | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHS.READINESS | decision | 20 | resolve_dependency | ready->GHS.DEFAULTS;blocked->GHS.DEPENDENCY_ISSUES | GHS.VALIDATE | stop | Input validation passed |
