# Input Validation

## Source

- Oracle readiness: Streamline the Import and Export of Messaging Setup Data, 26C, https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/sccv26c/26C-sccv-wn-f46531.htm

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation and route | Task-CSV export/import through the shared task exporter or Core Data Loader, or all-object configuration-package migration | Stop | Select the intended operation and one documented route | Always | |
| Exact task identity | ORA_CMK_MNGE_SIMPLIFIED_COLLAB_MSG_CONFIG and Manage Simplified Collaboration Messaging Configuration | Stop | Select the matching setup task; reject task overrides | Task-CSV export/import | |
| Immutable task ZIP | One readable FSM ZIP, its SHA-256, matching task metadata, and completed populated export provenance; template-only or failed exports are not import sources | Stop before preview | Obtain a completed export for this task and rerun Core Data Loader preflight after any change | Standalone task-CSV import | |
| Target and approval | One configured destination host and Run Book context matching the Task Hook validated Core Data Loader preview for the exact ZIP and task | Stop before upload | Rebuild the preview for the intended target and obtain its single Core Data Loader approval | Standalone task-CSV import | |
| Implementation project scope | Implementation project containing this task and, for all-object migration, the Service Providers task | Stop | Create or select the implementation project with the intended scope | Configuration-package migration only | |
| Configuration package | Package associated with the implementation project; uploaded before package import | Stop this task's execution route | Select the separate project/package migration workflow; do not pass a configuration package to task-CSV Data Loader | Configuration-package migration only | |

## Migration Scope Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The requested configuration-package migration includes all Collaboration Messaging configuration objects | Verify that Manage Collaboration Messaging Service Providers is also in scope | Continue only when both tasks are selected | |
| The requested operation is configuration-package import | Require an uploaded configuration package and route outside this standalone task skill | Do not execute it through this task-CSV Data Loader route | |
| The requested operation is standalone task-CSV import | Do not require a configuration package or its prior upload; use Core Data Loader's FSM task route | Continue only after task ZIP, target, Task Hook preview, and approval checks pass | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| The selected task is Manage Simplified Collaboration Messaging Configuration | Accept task identity | Always | |
| The operation is task-CSV export/import or configuration-package migration | Reject an unspecified or mixed route | Always | |
| ZIP format and provenance | Require a readable FSM archive with ASM_SETUP_CSV_METADATA.xml identifying this task and a completed populated export | Task-CSV import | |
| ZIP integrity and target binding | Bind the final ZIP bytes and SHA-256, exact task, destination host, and Run Book to the approved Core Data Loader preview; changes require new validation and approval | Task-CSV import | |
| Outcome evidence | Retain the returned request/process ID, terminal task result, ProcessLog or result report, and target-state verification; upload acceptance is not completion | After task-CSV import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSC.VALIDATE_INPUT | step | 10 | validate_input | valid->CMKSC.RESOLVE_FEATURE_STATE;invalid->CMKSC.RETURN_ISSUES | none | stop | Always |
