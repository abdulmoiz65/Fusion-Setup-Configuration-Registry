# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Project target and catalog | Verify the exact target, task, loader mode, client route, privileges, metadata, and artifact destination before live lookups |
| 2 | Organization routing evidence | Search the exact requested name, resolve ambiguity, and derive the action; stop when already a Project Unit |
| 3 | Existing classification label | For USE_EXISTING_ORGANIZATION, resolve the exact selected returned ClassificationCode through organizationClassificationsLOV before generation |
| 4 | Parent linkage and package | Bind exact names, classification, dates, component order, and immutable archive checksum |
| 5 | Data Loader terminal outcome | Return In Progress immediately after accepted initiation; only a later explicit status request may check the same request ID through core.data-loader; nonterminal status or timeout returns In Progress without automatic continuation |
| 6 | Post-load state | Only after terminal load success, verify the active classification and sequence-1 Project Unit Code EFF row before task completion |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PUORG.SCOPE | Project target and catalog | Yes | Every request | Verify | Project and catalog | verify_project_unit_setup_scope | Prevent cross-target writes | Resolve before external calls | VerifiedScope |
| PUORG.PERSISTENCE | Durable acceptance and resume binding | Yes | Before submission and later explicit status requests | Verify | Selected project, immutable approved archive and registered acceptance record | verify_project_unit_setup_scope | Preserve request-to-approval identity across sessions | Preflight declared project services and safe writable receipt/run/token destinations; resume only from matching registered evidence | ProjectId, AcceptanceReceiptRef, ArchiveChecksum, ApprovalRef, SkillRunRef |
| PUORG.ROUTING | Organization search and derived action | Yes | Every request | Lookup | Routed target evidence | find_active_organization | Select the correct create, existing, already-defined, or selection-required outcome | Search exact name and resolve ambiguity before defaults | DerivedAction, ActiveOrganizationMatches, SelectedOrganization, Classifications |
| PUORG.SELECTION | Exact existing organization selection | Conditional | DerivedAction = USE_EXISTING_ORGANIZATION | Lookup | Routed organization search and unfiltered classifications | find_active_organization | Name alone is not identity | Choose ID, classification, location and dates when selection is required | SelectedOrganization, ClassificationsComplete, Classifications |
| PUORG.EXISTING_CLASSIFICATION | Exact existing classification display label | Conditional | DerivedAction = USE_EXISTING_ORGANIZATION | Lookup | SelectedOrganization.ClassificationCode | resolve_organization_classification | The existing Organization anchor must use the selected code's exact LOV display label | Resolve one exact organizationClassificationsLOV row before generation | ResolvedOrganizationClassification |
| PUORG.LINKAGE | Exact HDL parent references | Yes | Both actions | Verify | Request and selection | resolve_project_unit_member_linkage | Child rows must resolve correct parent | Preserve names and dates exactly | ParentName, ParentClassification, EffectiveDates |
| PUORG.PACKAGE | Immutable HDL archive | Yes | Import preview | Verify | Generated ZIP and evidence | verify_project_unit_package_contract | Protect payload identity | Generate one action-specific DAT and checksum ZIP | ArchiveChecksum, ComponentRows |
| PUORG.LOAD_COMPLETION | Terminal HDL load status | Conditional | Later explicit status request for the accepted load | Verify | Core Data Loader status result for the retained request ID bound to the same target and task | | Initiation success is asynchronous and does not prove load completion | Check only on explicit request; nonterminal status or timeout returns In Progress and waits for another status request | LoadTerminalStatus, LoadStatusEvidenceRef, ObjectTotalCount, ObjectLoadedCount, ObjectErrorCount |
| PUORG.POST_LOAD | Verified Project Unit state | Yes | Terminal Data Loader success | Lookup | Durable loader receipt, terminal status evidence and exact requested values | verify_project_unit_after_load | Terminal loader success alone does not prove both required records | Verify classification and EFF before reporting task success | PostLoadClassificationVerified, PostLoadAttributesVerified, VerificationEvidenceRef |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Scope, derived action, selection and package pass | Continue to preview and approved loading |
| In progress | Initiation accepted, or requested status check is nonterminal or times out | Return immediately; resume the same request ID only on a later explicit status request |
| Input validation | Evidence missing, stale, incomplete or ambiguous | No generation; collect exact evidence |
| Catalog mismatch | Task, target or loader contract differs | Stop and correct route |
| Approval blocker | Required runtime client/adapter route or execution approval absent | No external operation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUORG.RESOLVE_DEPENDENCIES | step | 6 | resolve_dependency | ready->PUORG.ENFORCE_DESIGN;missing->PUORG.RETURN_ISSUES;conflict->PUORG.RETURN_ISSUES | PUORG.APPLY_DEFAULTS | stop | Before generation and immutable HDL preview |

## Execution Persistence and Resume Contract

Delegate live loading and requested status checks to `core.data-loader`, and local
project continuity to the declared artifact-version, artifact-registry and
project-state services. Keep Data Loader's concise user-facing response while
writing the internal records required by project governance. Local persistence
adds no Fusion call, automatic status check, separate approval or user-facing report.

### Before Submission

Resolve one existing `project_id`, exact target, immutable approved archive,
SHA-256, approval reference and row/action mapping. Require the declared project
services and safe writable destinations under that project's workspace. Allocate
an unused append-only acceptance-record location before invoking the loader.
Missing identity, unavailable services, path escape or overwrite conflict blocks
the load. Preserve immutable preparation and approval evidence through the
artifact-version and artifact-registry services.

### Acceptance Handoff

After one accepted initiation, save this minimal redacted binding under
`project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-organizations/current/execution-receipts/`:

| Field | Required value |
|---|---|
| project_id | Selected implementation project |
| skill_id and task_code | This skill and `PJF_MANAGE_PROJECT_UNIT_ORGANIZATIONS` |
| target_environment | Exact validated target identity |
| request_id | Exact server-issued Data Loader request ID; never synthesized |
| data_set_name | Exact returned name when available |
| archive_ref and archive_sha256 | Registered immutable approved archive and its SHA-256 |
| approval_ref and row_mapping_ref | Approval evidence and ordered rows/actions tied to that archive |
| status and accepted_at | `In Progress` and acceptance time; never terminal success inferred from initiation |

Use `core.project-mgmt.artifact-registry-manager` to register the receipt with
artifact type `other`, producing skill, location, version, status, timestamps and
checksum. Use `core.project-mgmt.project-state-manager` to update only declared
task-sequence/validation references and append the skill run under
`project/{project_id}/state/runs/`. Log token usage at the manifest's shared
token-log path and include the same estimate in the skill-run record. Do not
store tokens, credentials, raw sensitive responses or full tenant payloads.

The execution gate's `initiated` outcome requires both server acceptance and
successful local persistence and registration of this binding. Return `In Progress`
immediately afterward, without status reads, counts, error queries or post-load
verification. Keep one binding per accepted action archive in a mixed batch;
retain each accepted ID independently if a later archive fails. Never replay an
accepted archive.

Failure disclosure and repair are owned by
ora_error_handling.md#acceptance-persistence-and-status-recovery.

### Later Explicit Status Request

Load the registered binding from the selected project. Require an exact match
for project, target, task, request ID, approved archive hash and approval reference.
Missing, inconsistent or unregistered evidence blocks status execution. A supplied
request ID alone is insufficient. If local acceptance persistence previously
failed, reconcile and register the binding using retained server acceptance and
approved preparation evidence before entering the status gate.

Only then call core Data Loader for that ID. Append a status record linked to the
unchanged acceptance binding, retaining returned status/counts, available redacted
diagnostics and the next action; record the run and token usage. Apply status
outcomes and recovery from ora_error_handling.md#acceptance-persistence-and-status-recovery.
Retain verification evidence through the declared project services before marking
the task complete.
