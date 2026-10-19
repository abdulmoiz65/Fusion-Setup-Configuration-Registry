# Activity Standard Lookup Dependency Readiness

Resolve task scope, parent lookup type, target-code state, editability, impact,
execution authority, and migration prerequisites before preparing guidance or a
write handoff.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Configuration-level editability and Sales task ownership |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Predefined-data identification, code state, translations, effective dates, and session refresh |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Parent and child lookup REST resources |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Setup task package roles and handling |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-template-exports.html | Current task CSV template export contract |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/enable-default-task-status.html | Task-status default impact |
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-configure-default-activity-search-in-accounts.html | Activity-search order impact and supplied-value restrictions |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html | Activity Type function membership and required tag semantics |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitytypelookupslov-get.html | Function-specific Activity Type verification |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task scope and access | Confirm the setup user can use Manage Activity Standard Lookups and that the selected LookupType belongs to that task. |
| 2 | Parent lookup type | Resolve exactly one existing Standard Lookup type and capture its CustomizationLevel and canonical item link. |
| 3 | Current lookup code | Read the exact LookupCode or confirm its absence; capture all editable values and LastUpdatedBy before deciding the route. |
| 4 | Editability and impact | Apply configuration-level, predefined-data, tag, status-default, search-default, and downstream-impact rules. |
| 5 | Activity Type function design | For ZMM_ACTIVITY_TYPE Create, resolve the exact supplied function set and canonical function Tag before preview without requiring an export package. |
| 6 | Execution authority | For an Apps Common code write, resolve the exact target environment, authorized executor, immutable preview, and explicit approval. |
| 7 | CSV package and authority | For import, use a current package for this exact task and validate it through the shared setup-data workflow. |
| 8 | Verification plan | Define the exact post-change GET and, for an Activity Type, one function-specific LOV verification per selected function; include sign-out and sign-in validation when needed. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| task_scope | LookupType belongs to Manage Activity Standard Lookups | Yes | Always | Satisfied by a public documented type or current task-page or task-export evidence | Oracle documentation or current environment evidence | resolve_activity_standard_lookup_type | The Standard Lookups REST collection contains types outside this setup task. | Provide current task evidence for a type not in the documented list; do not use generic REST presence alone as task ownership. | LookupType, TaskScopeEvidence |
| parent_lookup_type | Exact Standard Lookup parent exists | Yes | Always | Satisfied when one exact parent is returned | Standard Lookups REST | resolve_activity_standard_lookup_type | Every lookup value is a child of an existing type. | Correct the parent type if it is missing or ambiguous. | LookupType, LookupTypeMeaning, CustomizationLevel, ModuleId, ParentItemLink |
| target_code_state | Exact current code state or confirmed absence | Yes | Review, Create, Update, Deactivate, Delete, Translate, or Validate | Satisfied when the result matches the selected operation | Standard Lookups child REST | find_activity_standard_lookup_code | Create requires absence; other maintenance requires one exact existing code. | Review the returned current state before previewing a mutation. | LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, LastUpdatedBy, CodeItemLink |
| lookup_editability | Configuration level and predefined-data status permit the requested fields | Conditional | Create, Update, Deactivate, or Delete | Satisfied only after the design matrix permits every requested field | Parent and code resolver output |  | Oracle restricts code insertion and maintenance by User, Extensible, or System configuration level and predefined-data state. | Remove disallowed fields or use only the operation permitted for the resolved row. | CustomizationLevel, LastUpdatedBy, RequestedFields |
| activity_type_function_design | Exact Activity Type functions and canonical Tag are resolved | Conditional | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | Satisfied when one or more unique supported functions produce one exact colon-wrapped Tag and the start date and enablement are explicit | Reviewed request and documented Activity function contract | derive_activity_type_function_tag | Activity Type visibility is function-specific and the canonical Tag carries the selected function membership. | Provide the exact subset of APPOINTMENT, TASK, and CALLREPORT; do not supply a conflicting Tag. | ActivityFunctionCodes, Tag, EnabledFlag, StartDateActive |
| status_default_impact | Lowest display-sequence impact is reviewed | Conditional | LookupType is ZMM_ACTIVITY_STATUS_CD and DisplaySequence changes | Satisfied after the preview shows whether the requested value becomes the default task status | Current lookup-code list | list_activity_standard_lookup_codes | The lowest display sequence defines the default task status. | Explicitly accept or revise the new default before a write. | CurrentLowestSequence, ProposedDisplaySequence, ProposedDefaultStatus |
| activity_search_impact | Activity-search order impact is reviewed | Conditional | LookupType is ORA_ZMM_ACTIVITY_FILTER_TYPE and DisplaySequence changes | Satisfied after the preview shows the resulting order and default search | Current lookup-code list | list_activity_standard_lookup_codes | Lookup order controls the Activity search Show filter and its default; Oracle documents the supplied list as fixed. | Explicitly accept the resulting filter order before a write; do not add, delete, or end-date a value. | CurrentFilterOrder, ProposedFilterOrder, ProposedDefaultFilter |
| apps_common_write_authority | Exact environment, immutable preview, and approval are current | Conditional | Create, Update, Deactivate, or Delete is requested for live execution | Satisfied only when approval matches current-state fingerprint, method, endpoint, and body or delete effect | Request plus current Apps Common reads |  | A lookup-code mutation changes shared Fusion configuration. | Approve the exact preview after all live reads; any changed field invalidates approval. | TargetEnvironment, Method, Endpoint, RequestBody, CurrentStateFingerprint, Approval |
| task_csv_package | Current task-specific package is available | Conditional | Export or Import | Satisfied when the package is for ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS, preserves metadata-derived files and headers, contains the existing parent, and has one reviewed row delta | Task export or template export | verify_activity_standard_lookup_csv_package | Setup-data import requires a task-specific ZIP package and the package is the authority for its file and column contract. | Do not use loose CSV, invent file names or columns, populate system audit fields on a new row, or use a package from another lookup task. | PackagePath, FileNames, Headers, TaskCode, PackageSha256, CandidateRow |
| import_authority | Setup-data executor and immutable package approval are current | Conditional | Import | Satisfied when shared validation and Data Loader authorization complete | Shared setup-data workflow |  | Import may change multiple lookup rows. | Validate the exact ZIP and obtain approval before handoff to core.data-loader. | AuthorizedExecutor, PackageFingerprint, Approval |
| activity_type_function_verification | New Activity Type is visible for every selected function | Conditional | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE after successful REST or import execution | Satisfied only when the exact code is returned once for every selected function with the expected meaning, enabled state, dates, and canonical Tag | Activity Type Lookups LOV | verify_activity_type_by_function | A base lookup code is not complete unless it is usable for its selected Activity functions. | Verify each selected function and do not claim completion from the Standard Lookup GET alone. | VerifiedActivityFunctionCodes, VerifiedLookupCode, VerifiedMeaning, VerifiedEnabledFlag, VerifiedStartDateActive, VerifiedTag |
| session_refresh | User-facing verification uses a new session when needed | Conditional | A saved change is not visible | Satisfied after affected users sign out and sign back in | Oracle lookup behavior |  | Oracle documents that lookup changes may require a new session. | Refresh the session before classifying the saved setup as ineffective. | RefreshedSessionEvidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| SATISFIED | Task scope, parent, target state, editability, impact, and route-specific gates are resolved | Continue to defaults and design enforcement |
| NOT_APPLICABLE | A conditional write, import, or impact dependency does not apply | Continue |
| BLOCKED | Required scope, parent, identity, editability, package, environment, preview, approval, or impact acceptance is missing | Stop before mutation or import handoff |
| FAILED | A live read fails or returns ambiguous evidence | Report the safe failure and stop without retrying a write |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_STD.DEPENDENCIES | step | 2 | resolve_dependency | ready->ACTIVITY_STD.LOOKUP_TYPE;blocked->ACTIVITY_STD.BLOCKED;failure->ACTIVITY_STD.FAILED | ACTIVITY_STD.VALIDATE | stop | Always |
