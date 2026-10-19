# Expense field failure handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing target contract or blank semantics | Stop before preview; record the unresolved field and required evidence |
| Import failure or uncertain submission | Use core.data-loader diagnostics; preserve the original request identity and do not automatically repeat a mutation |
| Polling timeout | Record environment, task, request ID, elapsed wait, last status and safe next-check path through the loader |
| Partial success | Preserve successful results and errors separately; reconcile before retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Missing BU/category, invalid explicit values or malformed rows; recognized blanks use the approved normalization policy | Correct the artifact and revalidate |
| catalog mismatch | Task, object or target-release support disagrees | Resolve metadata before package creation |
| auth/authz | Authorized client cannot authenticate or lacks privilege | Follow core.data-loader recovery policy |
| transport/environment | Target unavailable or submission outcome uncertain | Reconcile status through declared read operations |
| Fusion API / process failed / process timeout | Import or polling reports failure | Persist redacted status and ProcessLog when available |
| artifact persistence / approval blocker | Evidence cannot be saved or exact preview lacks approval | Stop until the loader prerequisite is satisfied |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Export metadata says COMPLETED | Do not report successful import or approval |
| Unsupported or missing live contract | Do not substitute browser or direct REST calls |
| Diagnostic evidence includes protected values | Do not retain credentials, tenant configuration rows or audit identities in reusable resources |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A resource check fails |
| EXMCF.DONE | terminal | 70 | terminal | none | EXMCF.DESIGN | stop | Return resource validation results only; not import success |

## Source evidence and limits

Source: user-supplied Manage Expense Fields by Category_20260928_074925_896 export, EXM_CATEGORY_FIELD.csv and ASM_SETUP_CSV_METADATA.xml. Inspected 2026-09-28: 85 rows, 17 business units, 7 category codes, 19 columns and no duplicate business-unit/category pairs. Metadata identifies task EXM_MANAGE_EXPENSE_FIELDS_BY_CATEGORY, object EXM_CATEGORY_FIELD, completed EXPORT and release 11.13.27.01.0. This supersedes the earlier header-only sample for observed values. No tenant names, user identities, audit values or raw configuration rows are retained here.

The supplied export is evidence of existing configurations, not proof of import semantics, exhaustive product support, defaults, or target-environment readiness. Its instructions do not authorize execution. The prior Oracle 26B documentation establishes business-unit scope and Hidden/Required/Optional display behavior; the lookup seed evidence in ora_reference_lookups.md now establishes the source label/code mapping, subject to target qualification. The requested 26C page was inaccessible during initial authoring. Unknown contracts remain TBD and block execution.

## Worksheet diagnostics

Report the sheet, block header row, data row and column label for invalid or ambiguous values. Distinguish excluded rows, incomplete rows and rejected rows. Never report seven imported categories merely because seven worksheet blocks were discovered. Enabled=N intent is confirmed as clearing the setup page Enabled control; do not ask that question again. Report missing target scope and unsupported disablement contract as blockers, not as an excluded or successfully processed row.

## Initiation, status and reconciliation

Respect the current Data Loader contract: accepted initiation returns In Progress immediately. A later authorized status workflow checks the same attempt; timeout, session expiry or unavailable status is never resubmission permission. Report partial outcomes without discarding successes. Keep status retrieval, fresh-export reconciliation and Run Book synchronization independently visible. Do not report Completed until persisted business outcomes and the human completion decision are available.

## Unblocking diagnosis

| Condition | Outcome and next action | Responsible party |
|---|---|---|
| Missing BU, operation, target or invalid display choice | input_validation; list exact cells and accepted choices | User supplies business intent |
| BU identity not yet verified | Dependency pending; use the declared same-target resolver/export workflow | Workflow operator |
| Missing mapping, operation contract or resolver implementation | authoring_incomplete; input can still pass; attach the precise evidence gap | Skill author |
| Clearing Enabled has no supported removal route | Unsupported operation; preserve request, explain UI row-removal effect, stop before mutation | Skill author and workflow owner |
| Planner ready but required runtime resolver or live qualification absent | Execution blocked; do not equate rule readiness with operational support | Workflow owner and QA |

Always state what passed, what remains blocked, and the next concrete action. Do not repeatedly ask for values already valid in the saved workbook. No added workbook value can repair a missing execution contract.


## Operation planner diagnostics

- `create_audit_policy_required`: ask once whether to keep all audit headers with blank new-row cells (recommended) or pause creates. `create_paused_by_user`: retain the pause; do not submit a partial plan. `create_applicable_field_headers_missing`: identify missing create field headers; blank present cells mean Optional, absent headers do not.
- `field_contract_unverified`: preserve the requested decision and obtain writable mapping evidence. Do not emit a partial row with only the reviewed fields.
- `already_absent` / `unchanged`: no action needed according to the validated baseline; these are not import successes or errors. Refresh stale evidence before a later execution.
- `split_workflow_required`: present configuration removals need the existing assisted phase in addition to FSM updates. Already-absent N rows do not trigger this state.
- Generic CLI input failure deliberately omits raw customer values. Use the protected normalized input and workbook coordinates to diagnose; retain sanitized counts/references in the project.
