# Opportunity Marketplace Jobs Configurations Defaulting Rules

Source: Developer-approved Recruiting Type DefaultFlag bootstrap rule.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| DefaultFlag | Established value from the fresh package contract | A new Recruiting Type child row is prepared and the fresh source contains one or more Recruiting Type child data rows | Yes; system-derived, never ask the user or accept an override | derive_recruiting_type_default_flag |
| DefaultFlag | N | A new Recruiting Type child row is prepared and the structurally valid fresh source member contains zero Recruiting Type child data rows | Yes; approved initial-configuration bootstrap, never ask the user or accept an override | derive_recruiting_type_default_flag |

## Decision Evidence

Persist the resolved DefaultFlag, source child-row count, fresh export
reference/fingerprint, and derivation branch in the task validation/preflight
artifact before preview. For bootstrap, persist DefaultFlag: N and the exact
reason: No Recruiting Type rows exist in the fresh Jobs Configuration export; applied approved bootstrap default.
For existing rows, persist the reused value and source-row evidence. If no
Recruiting Type filter is supplied, record not applicable and add no child row.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JC.DERIVE_REC_TYPE_DEFAULT | decision | 45 | apply_default | derived->JC.GENERATE_PACKAGE;not_applicable->JC.GENERATE_PACKAGE;invalid->JC.RETURN_ISSUES | JC.VALIDATE_IDENTITY | stop | A new Job Configuration passed identity validation; derive DefaultFlag for supplied Recruiting Type rows or record not applicable |
