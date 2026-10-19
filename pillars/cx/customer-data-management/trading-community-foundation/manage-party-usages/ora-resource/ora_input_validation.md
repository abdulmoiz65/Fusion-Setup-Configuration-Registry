# Input Validation

Validate the fixed whole-task contract before any Fusion export or import POST.

## Required Groups

| Group | Requirement | Failure action |
|---|---|---|
| Operation | Exactly `export` or `import` | Stop before preview |
| Task identity | `Manage Party Usages` / `HZ_MANAGE_PARTY_USAGES` | Reject overrides; for export, search live by name without hierarchy filters and select the exact fixed code/name row |
| Environment | One exact configured source or target; automatically use the sole active configured environment | Ask only when configuration is missing or multiple active environments remain ambiguous; otherwise continue without a user question |
| Project | Existing `project_id` and task context, or permission from repository rules to create the prescribed draft project | Resolve or create before preview |
| Export | `template_only=false`, `export_criteria=[]`, fixed output path, 300-second wait, 10-second poll | Restore the fixed contract |
| Import package | One readable unchanged ZIP and SHA-256 | Stop before preview |
| Import route | `executionRoute=data-loader`, `executionAdapter=cx.customer-data-management.trading-community-foundation.manage-party-usages.native-fsm-import`, `packageType=FSM`, `targetEnvironment`, and a Data Loader-authorized native FSM adapter | Reject alternate or generic Data Loader routes |
| Approval | Approval bound to the complete immutable operation preview | Stop before POST |

## Field Validation

| Check | Rule |
|---|---|
| Catalog match | Resolve exactly one live row with name `Manage Party Usages`, code `HZ_MANAGE_PARTY_USAGES`, availability `Y`, and CSV support `Y`; use resolver `find_party_usages_task_by_name_then_exact_code` |
| Environment resolution | Read durable Fusion configuration first; select the sole active environment automatically and bind its identity to the preview; ask only for a genuinely missing or ambiguous choice |
| Preparation continuity | Authentication, browser sign-in, token refresh, project setup, live lookup, and other read-only checks never create an approval or `ready` handshake; continue automatically until preview-ready or genuinely blocked |
| Hierarchy evidence | Treat absent or blank live offering and functional-area fields as unavailable metadata and bind the fixed catalog context; reject contradictory nonblank hierarchy values |
| Export scope | Require an empty criteria array and non-template whole-task scope |
| Export path | Resolve inside `project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-party-usages/` |
| Export adapter | Require `shared.setup-export.task-level-export` |
| Export preview | Persist `export-approval-preview.json` with `status=ready_for_approval`; bind project, environment, fixed task, whole-task scope, output, adapter, empty criteria, and polling options; never require an archive hash before export |
| Import adapter | Require `core.data-loader` as orchestrator; classify the ZIP from `ASM_SETUP_CSV_METADATA.xml`, preserve it unchanged, and require Data Loader to authorize the task-local native FSM adapter, which reuses `shared.setup-import.fsm-csv-import` process mechanics |
| Native adapter capability | Require live `setupTaskCSVImports/{TaskCode}/child/SetupTaskCSVImportProcess` metadata to expose child-process create with `TaskCode`, `FileContent`, and `SourceTargetDiffOkFlag`; require the create response contract to expose root-level `ProcessId` |
| Cross-environment migration | The adapter always sends the native revision-tolerance value; cross-environment import behavior is unconditional and is not a preview option or override gate |
| Generic action exclusion | Reject `uploadDataLoaderFile`, `dataLoaderDataSets/action/initiateDataLoad`, `runID`, and `sourceType` for this FSM package; never route a setup-task archive through the generic action |
| ZIP signature | Require a valid ZIP with the `PK` signature |
| Metadata member | Require exactly one case-sensitive basename `ASM_SETUP_CSV_METADATA.xml` |
| FSM binding | Require exactly one metadata `ObjectShortName` equal to `HZ_MANAGE_PARTY_USAGES` |
| Immutable bytes | Do not extract, edit, normalize, or repack the submitted archive |
| Fingerprint | Require a lowercase 64-character SHA-256 calculated from the submitted bytes |
| Approval timing | Accept `approve` only for a persisted ready preview whose canonical fingerprint and bound values still match; an earlier `approve` triggers completion of preparation, not a POST |
| Partial scope | Reject record, business-object, criteria, and template-only filters |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PU.VALIDATE_CONTEXT | step | 2 | validate_input | valid->PU.VALIDATE_OPERATION;invalid->PU.ERROR | PU.LOOKUP_SETUP_TASK | stop | Before preview creation |
| PU.VALIDATE_OPERATION | step | 3 | validate_input | valid->PU.VALIDATED;invalid->PU.ERROR | PU.VALIDATE_CONTEXT | stop | Before export POST or Data Loader import preview |
