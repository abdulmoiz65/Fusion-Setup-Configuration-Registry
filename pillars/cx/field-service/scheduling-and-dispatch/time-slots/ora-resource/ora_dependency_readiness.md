# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Workbook input | Validate the supplied Time Slots workbook and required worksheet fields. |
| 2 | Field Service API access | Confirm read-only access to the Time Slots collection in the selected environment. |
| 3 | Time-slot identity | Resolve the requested label and determine whether it is absent for create or present for read, update, enable, or disable. |
| 4 | Design enforcement | Apply all applicable Time Slots design rules before a preview is considered. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| time_slots_api_access | Field Service API access | Yes | A Time Slots lookup is requested | Verify | Read-only Time Slots collection response | verify_time_slots_api_access | UI access does not prove Field Service API access | Resolve the selected FSCR environment profile, then run the declared read-only preflight | API access result |
| time_slot_identity | Existing time slot record | Yes | Read, create, update, enable, or disable is requested | Lookup | Read-only item lookup by label | find_time_slot_by_label | Create must not overwrite an existing slot and updates require current state | Provide an exact time-slot label | Current record or not-found state |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Workbook input, API access, and identity checks are satisfied | Yes |
| Input Blocked | Workbook input is missing or invalid | No |
| Authorization Blocked | The read-only Time Slots API preflight is rejected | No |
| Identity Blocked | The requested label conflicts with the requested operation | No |

## Direct REST Write Handoff

Direct REST write readiness is deliberately owned by `ora_rest_execution.md`, not this Resource Authoring graph. A selected `ora_rest_execution` route must stop before preview until its describe-backed payload mapping is approved. Keeping that unresolved write-only contract out of the shared read/validation graph prevents it from blocking read-only discovery and design validation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.DEPENDENCIES | step | 2 | resolve_dependency | ready->TS.DEFAULTS;blocked->TS.DESIGN_BLOCKED | TS.VALIDATE_WORKBOOK | stop | Before Time Slots defaults, lookups, and design enforcement. |
