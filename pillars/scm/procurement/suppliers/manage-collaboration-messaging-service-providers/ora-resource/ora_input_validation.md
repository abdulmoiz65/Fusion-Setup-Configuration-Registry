# Service Providers FSM Task-CSV Import Validation

This validation applies only to importing an existing CSV setup-data ZIP for
`Manage Collaboration Messaging Service Providers`. It does not define a
manual provider-creation form or permit changing CSV values after preflight.

Oracle documents task CSV packages as a migration mechanism and requires the
exported ZIP plus the task code used for export before import. The target task
validates that the ZIP contains setup data for that task. [S1][S2]

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Immutable source package | One readable ZIP that has passed the core Data Loader FSM preflight | Stop before approval or upload | Re-export the task data or repeat the Data Loader preflight after any package change | Task CSV import | |
| Exact task identity | Task code ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER and the matching task name | Stop because the package cannot be bound safely to this task | Select the matching setup task or export the intended task again | Task CSV import | |
| Exported task-data provenance | ZIP metadata identifies ObjectShortName ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER, ProcessType EXPORT, and a completed export | Stop before upload | Obtain a completed setup-task data export; do not use a template-only or unrelated ZIP | Task CSV import | |
| Target and Run Book binding | Data Loader preflight confirms the selected target environment and active Run Book context for the immutable ZIP | Stop before upload | Select the intended target and repeat preflight | Task CSV import | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ZIP format and integrity | Accept only a readable ZIP that the Data Loader classifies as FSM setup data; reject an unreadable archive or an archive that lacks the FSM metadata member | Task CSV import | |
| Task-code match | Require the package metadata and task context to identify ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER; do not import a package for another task through this task route | Task CSV import | |
| Export completion | Require completed export metadata before import; a failed, incomplete, or template-only export is not an import source | Task CSV import | |
| Immutable artifact | Bind approval to the preflighted ZIP bytes; any change to the ZIP requires a new preflight and approval | Task CSV import | |
| Target binding | Require the preflighted environment to be the approved target; an environment mismatch stops the workflow | Task CSV import | |
| Post-import verification | On an accepted import, use the returned process identifier and ProcessLog or result report to determine the outcome; do not infer success from upload acceptance | After import process completion | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSP.INPUT_CONTRACT | step | 10 | validate_input | validated->CMKSP.RESOLVE_PREREQUISITES;issues->RETURN_ISSUES | none | stop | A task CSV import is requested |

## Sources

[S1]: https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/Task_CSV_Import.html
[S2]: https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/Task_CSV_Export.html
