# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Catalog support | Confirm task-level CSV Export/Import remains enabled in the effective catalog. |
| 2 | Target comparison | Obtain a fresh unscoped target export before determining create or update behavior and before post-import readback. |
| 3 | Requested-row selection | Select only the requested profile parent rows and their child rows for the import ZIP. |
| 4 | Import ZIP validation | Validate the immutable, full-export-conforming ZIP before import. |
| 5 | Import authorization | Require Manage Recruiting Administration privilege and explicit approval before import. |
| 6 | Import completion | Require import status COMPLETED and post-import readback before success is reported. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DEP-001 | Catalog CSV support | Yes | Always | Verify | Effective task catalog |  | Prevents substitution of an unsupported route. | Stop if CSV Export/Import support is not enabled. |  |
| DEP-002 | Fresh unscoped target export | Yes | Before create/update determination or post-import readback | Lookup | Task-level FSM export | export_job_requisition_security_profiles | Supplies target state for exact Name determination and post-import readback. | Stop when target state is unknown. | Existing profile names and child rows |
| DEP-003 | Requested-row subset | Yes | Before any CSV import | Verify | User-supplied requested profile Names and the full export baseline |  | The import ZIP must include only requested parent rows and child rows that belong to those parents. Omitted profiles remain unchanged. | Stop and rebuild the ZIP if it contains an unrequested profile or child row. | Selected Names; selected parent rows; selected child rows |
| DEP-004 | Conforming import ZIP | Yes | Before any CSV import | Verify | Immutable ZIP supplied for import | verify_fsm_task_csv_metadata | Ensures the package retains the task's full-export metadata and required CSV structure. | Stop if the ZIP is missing a required member, has duplicate metadata, or does not conform to the full-export contract. | ZIP checksum; validated package identity |
| DEP-005 | Import authorization | Yes | Before any CSV import | Verify | Authenticated caller privilege evidence and approved implementation record |  | Import requires IRC_MANAGE_RECRUITING_ADMINISTRATION_PRIV and approval bound to the exact ZIP checksum, target, and create/update/merge summary. | Stop before import if privilege evidence or the exact approval record is unavailable. | Target environment; ZIP checksum; create/update/merge summary |
| DEP-006 | Import completion and readback | Yes | After CSV import submission | Verify | Import status and unscoped post-import export |  | A submitted import is not successful until status is COMPLETED and readback matches the supplied ZIP. | Stop without retry on a failed status or readback mismatch. | Completed status; matching parent fields; supplied child rows present |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The documented dependency is evidenced. | No |
| Lookup | Target state or an approved value must be resolved. | Lookup only |
| Verify | Security alignment or approval readiness must be checked. | No |
| Blocked | A mandatory dependency is missing, ambiguous, or unsupported. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| JRSP.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->JRSP.RESOLVE_RESPONSIBILITY_TYPE;blocked->JRSP.HANDLE_ERROR | JRSP.VALIDATE_INPUT | stop | Always |
