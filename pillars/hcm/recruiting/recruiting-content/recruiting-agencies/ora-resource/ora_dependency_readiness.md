# Recruiting Agencies Dependency Readiness

## Purpose

Defines the authorities and evidence that must be ready before package generation or import handoff.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 0 | Project execution context | For Create, Update, or Import, resolve the generated task context and active Run Book through the owning core workflows before candidate preparation; not required for Retrieve |
| 1 | APPS_COMMON_LOOKUPS | Resolve every supplied Referral Type, Contract Type, and Exclusivity Length as one enabled exact Meaning or LookupCode |
| 2 | FRESH_AGENCY_EXPORT | Verify a fresh immutable target-environment export and its agency CSV contract |
| 3 | Agency identity | Apply the operation-specific exact Agency Name rule |
| 4 | Candidate package proof | Generate only from the verified target-release structure |
| 5 | CANDIDATE_AGENCY_ZIP approval | Complete Data Loader preflight and Task Hook validation first, then bind explicit approval to the immutable ZIP fingerprint, target, task, agency, and operation |
| 6 | APPROVED_DATA_LOADER | Hand off once to core.data-loader after every prior gate passes |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| project_execution_context | Core project and Run Book context | Yes | Create, Update, or Import; not Retrieve | Verify | core.project-mgmt.project-workspace-initializer and core.runbook | | Required by core Data Loader Task Hook before task validation and preview | Follow Project execution context below; do not invent bindings | Generated task context, active Run Book reference, and selected environment |
| referral_type_lookup | APPS_COMMON_LOOKUPS Referral Type | Conditional | Create or Referral Type supplied | Lookup | core.fusion-api.apps-common.lookups | resolve_referral_type | Prevents unsupported or disabled referral values | Supply an enabled Referral Type code or text | LookupCode and Meaning |
| contract_type_lookup | APPS_COMMON_LOOKUPS Contract Type | Conditional | Contract Type supplied | Lookup | core.fusion-api.apps-common.lookups | resolve_contract_type | Prevents unsupported or disabled contract values | Supply an enabled Contract Type code or text | LookupCode and Meaning |
| exclusivity_lookup | APPS_COMMON_LOOKUPS Exclusivity Length | Conditional | Exclusivity Length supplied or Referral Type is Person Specific | Lookup | core.fusion-api.apps-common.lookups | resolve_exclusivity_length | Enforces the Person Specific exclusivity requirement | Supply an enabled Exclusivity Length code or text | LookupCode and Meaning |
| fresh_agency_export | FRESH_AGENCY_EXPORT | Yes | Retrieve, Create, or Update | Verify | shared.setup-export.task-level-export | verify_fresh_agency_export | Establishes current identity and the target-release package contract | Obtain a fresh Recruiting Agencies export from the intended target | Agency rows, metadata, verified header, and fingerprint |
| exact_agency_identity | Exact Agency Name result | Yes | Create or Update | Verify | Fresh exported agency rows | verify_agency_identity | Prevents duplicates and unintended operation conversion | Create requires no exact match; Update requires exactly one | Identity classification and exact Update row |
| proven_package_template | Verified target-release package structure | Yes | Create or Update package generation | Verify | FRESH_AGENCY_EXPORT or approved target-release template | verify_fresh_agency_export | Prevents invented columns, members, keys, and child data | Provide current package proof | Verified members, header, and metadata |
| immutable_import_approval | CANDIDATE_AGENCY_ZIP | Yes | Before Import | Blocked until approved | Candidate ZIP fingerprint and explicit approval | verify_candidate_agency_zip | Prevents import of a different artifact or target | Approve the exact target, agency, operation, and SHA-256 | Approval receipt and matching immutable ZIP |
| approved_loader | APPROVED_DATA_LOADER | Yes | After immutable approval | Satisfied | core.data-loader | verify_candidate_agency_zip | Uses the approved FSM execution contract | Keep the artifact unchanged and submit once through core.data-loader | Validated ZIP and task identity |

## Project execution context

This is a core execution prerequisite for Create, Update, and Import, not an agency
business field. Retrieve does not invoke this prerequisite.

1. Use the selected project and catalog-resolved task mapping for Recruiting /
   Recruiting Content / Recruiting Agencies (`ORA_IRC_MANAGE_AGENCIES`). Preserve
   any other mapped tasks. Do not initialize a second project to evade a blocker.
2. When no initialized project exists, delegate to
   `core.project-mgmt.project-workspace-initializer`. It owns task mapping and
   generation of `artifacts/shared/runbook/current/task-context.json`, the setup
   task plan, and the Run Book plan. Follow its automatic initial creation route
   through `core.runbook`, including its approval and dashboard requirements.
   Do not ask the user to supply a Run Book ID, create task-context.json, or approve
   an extra Run Book setup plan for this default initial creation. Do not pass
   `--no-create-runbook` unless the user explicitly deferred creation. Use the
   current checkout's catalog and core skills; never depend on another chat's
   artifacts, another machine's absolute paths, or a remembered Run Book ID.
   After successful creation and the required dashboard, resume the original
   agency request automatically; a second create-agency prompt is unnecessary.
3. For an existing project with missing planning artifacts, return to the
   initializer's mapping and artifact-refresh workflow. An interrupted initial
   setup that was not explicitly deferred continues through its original automatic
   creation route once the core preconditions are satisfied. Do not treat every
   missing context as a user-deferred project. Refresh is local planning;
   it does not activate a Run Book or overwrite existing Run Book state. Do not
   hand-write task-context.json or set `runbook_control.status` to `active`.
4. Require an active project Run Book with its real reference and the selected
   environment binding before Task Hook. A deferred project's later Run Book
   creation requires an explicit request under `core.runbook`; ask specifically
   for that operation when it is missing. Failed or unknown creation outcomes
   require reconciliation through the owning workflow, not automatic retry.
   A configured Data Loader runID alone does not establish project readiness.
5. Select the exact agency task and sequence from the generated context. Complete
   Data Loader's persisted preflight, then use Task Hook `data-load`, evaluate its
   returned rules, and use its preview, approval, and archive-verification commands.
   Pass the returned task-validation envelope unchanged to Data Loader. These are
   core operations; never fabricate a binding or call Task Validator directly.

Check this context before candidate preparation so the user gets the actual
project setup action early. During internal Task Hook validation, verify the
supplied context and artifacts only; do not initialize a project, create a Run
Book, repeat an export, or invoke Data Loader recursively. If the binding or
artifact changes after preview, restart the core validation and approval cycle.


## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The required evidence or approval already resolves exactly | Only the next declared step |
| Lookup | A declared read-only lookup can resolve the value | Read-only lookup only |
| Verify | Export, identity, package, or artifact evidence needs inspection | No mutation |
| Needs Input | A required business value is absent | No |
| Blocked | Evidence is stale, ambiguous, malformed, unapproved, or mismatched | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RA.CHECK_DEPENDENCIES | decision | 50 | resolve_dependency | ready->RA.CHECK_DESIGN;needs_input->RA.HANDLE_ISSUES;blocked->RA.HANDLE_ISSUES;failed->RA.HANDLE_ISSUES | none | stop | Create, Update, or Import after reference resolution and identity validation |
