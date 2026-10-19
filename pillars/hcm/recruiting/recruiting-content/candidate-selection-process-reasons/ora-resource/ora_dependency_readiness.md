# Candidate Selection Process Reasons Dependency Readiness

## Purpose

Defines task-local prerequisites and operational evidence. No external upstream FSM task is required to create a reason or reason group.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current task-wide export | Validate the intended target, release, task identity, metadata, members, headers, and current-state evidence |
| 2 | Reason or group identity | Classify the exact code as absent or present according to the requested operation |
| 3 | Active reason | For a new association, resolve one exact reason whose current status is ORA_ACTIVE |
| 4 | Existing reason group | For a new association, resolve one exact existing group |
| 5 | Existing association | Determine whether the exact pair is absent or already satisfied |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_task_export | Approved task-wide export | Yes | Every authoring or verification request | Lookup | Current intended-target ORA_IRC_MANAGE_CSP_REASONS export | verify_csp_export_package | Establishes the local identity, language, package-shape, and reconciliation authority | Export the task for the intended target and provide the complete ZIP | Validated package path, target, release, member inventory, installed languages, and fingerprint |
| reason_identity | Exact reason or create-availability evidence | Conditional | Reason create, update, lifecycle, translation, or association work | Lookup | Validated reason and usage CSV rows | resolve_existing_reason | Prevents duplicate create, wrong-case update, or unresolved association identity | Provide the exact ReasonCode | ABSENT or PRESENT result, exact code, current status, and row fingerprint |
| reason_group_identity | Exact group or create-availability evidence | Conditional | Group create, update, lifecycle, translation, or association work | Lookup | Validated reason-group CSV rows | resolve_existing_reason_group | Prevents duplicate create, wrong-case update, or unresolved association identity | Provide the exact ReasonGroupCode | ABSENT or PRESENT result, exact code, current status, and row fingerprint |
| active_reason_for_association | Active reason | Conditional | A new reason-to-group association is requested | Lookup | Exact current base-reason row | resolve_existing_reason | The UI permits only an Active reason to be newly added to a group | Activate an approved reason first or provide another exact Active ReasonCode | Exact ReasonCode and ReasonStatusCode ORA_ACTIVE |
| existing_group_for_association | Existing reason group | Conditional | A new reason-to-group association is requested | Lookup | Exact current base-group row | resolve_existing_reason_group | An association cannot target a missing group | Provide one exact existing ReasonGroupCode | Exact ReasonGroupCode and current group status |
| association_identity | Exact reason-to-group pair | Conditional | Association create, replay, or verification | Lookup | Validated usage CSV rows | resolve_existing_association | Preserves idempotency and prevents duplicate usage rows | Provide the exact ReasonCode and ReasonGroupCode pair | Association ABSENT or PRESENT result and pair fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required identity and readiness evidence already resolves exactly | No |
| Lookup | A documented local export resolver can establish the required state | Read-only local lookup only |
| Not Applicable | The dependency condition does not apply to the requested operation | No |
| Needs Input | A required exact code, pair, export, or translation selector is missing | No |
| Unresolved | Evidence is stale, absent, ambiguous, wrong-target, or incompatible | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSPRSN.CHECK_DEPENDENCIES | decision | 40 | resolve_dependency | ready->CSPRSN.CHECK_DESIGN;not_required->CSPRSN.CHECK_DESIGN;needs_input->CSPRSN.HANDLE_ISSUES;unresolved->CSPRSN.HANDLE_ISSUES | CSPRSN.RESOLVE_REFERENCES | stop | After the request's exact identities and current task export resolve |
