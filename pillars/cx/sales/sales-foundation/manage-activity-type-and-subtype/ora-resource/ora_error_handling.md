# Error Handling

Stop safely on missing setup context, ambiguous LOV results, an invalid or pending CSV source package, an unapproved CSV import, or an unselected execution route. The reviewed public Oracle sources document editing a completed CSV data-export package or using a setup-task CSV template package before CSV import. They do not document direct create or update methods for the CRM Activity Type LOV endpoints.

Sources: [Associate Activity Type with a Function and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/associate-activity-type-with-a-function-and-subtype.html), [Activity Type Lookups REST API](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitytypelookupslov-get.html), [Setup Task CSV Template Exports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-template-exports.html), and [Setup Task CSV Imports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html).

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required type, function, subtype, enablement, or conditional tag input is missing | Stop and request only the missing value. |
| The type is not returned for the supplied function | Treat it as a new-type candidate when change_mode is create; use the documented UI route. The supplied subtype-only data-export package cannot create the parent type. Do not claim a change was made. |
| A lookup result is ambiguous | Stop and ask the requester to correct the identifiers. |
| A read-only LOV request fails | Stop before guided setup, disclose the safe diagnostic, and do not retry automatically. |
| A task CSV template-export process is incomplete or has no result | Stop before preview and import. Record the task code and process identifier, then wait for the existing process result; do not automatically create another export process. |
| A task CSV template-export process completes with errors | Retrieve its ProcessLog once, disclose the result, and stop before import. |
| A supplied CSV source ZIP is not a completed export for this task or does not contain the documented subtype CSV schema | Block the import and request a valid task template ZIP or completed data-export ZIP. |
| A CSV import is requested without a verified source ZIP, immutable preview, and current approval | Block the import and request the missing gate. |
| A request uses the supplied subtype-only package to create a parent type or activity-function association | Block the CSV route and direct the request to the documented guided task UI. |
| A direct CRM Activity Type LOV create, update, enablement, or association request is made | Block that direct mutation. Use the documented setup-task CSV import route or the guided Setup and Maintenance UI; do not invent a CRM LOV write payload. |
| A CSV import reports a revision mismatch | Stop with SourceTargetDiffOkFlag at its documented default N; do not bypass the revision check. |
| A supported subtype mutation does not select a route | Default to the current task-specific package and core Data Loader preview-and-approval workflow; do not initialize browser control. |
| The requester explicitly selects manual UI | Prepare the documented guided procedure only; do not substitute a Data Loader import. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required setup value or task access is absent | Request the missing value or access. |
| PENDING | A template-export process has not produced a completed result | Wait for the existing process result; do not create another export automatically. |
| BLOCKED | A mapping, design gate, invalid source package, unsupported parent-type CSV change, or missing preview approval prevents progress | Correct the setup context, complete the approved CSV-import gates, or use the documented UI step. |
| FAILED | A read-only LOV request fails | Report the safe error context and stop before retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or mapping block | The missing or conflicting business value and the safe next action. |
| LOV failure | Resolver name, safe endpoint identity, response status when available, and the no-retry instruction. |
| CSV automation block | The task name, source-package or import process status, missing gate, and the no-retry instruction. |
| Direct CRM LOV write block | The task name, the documented setup-task CSV import route, and the guided UI path. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The CRM Activity Type LOV sources do not provide a direct write contract | Do not invent a CRM LOV write endpoint or payload. |
| The template export is pending or failed and no valid data-export ZIP was supplied | Do not submit a CSV import, create another template export automatically, or claim a template ZIP exists. |
| A data-export ZIP does not match this task, is incomplete, or has the wrong schema | Do not edit, repackage, or submit it. |
| The supplied subtype-only package is requested to create a parent type or activity-function association | Do not submit the CSV import for that change. |
| The CSV import preview is not approved | Do not upload or submit the package. |
| The import reports a source-target revision mismatch | Do not set SourceTargetDiffOkFlag to Y merely to continue. |
| Lookup result is absent or ambiguous | Do not choose an activity type or claim that a subtype was created. |
| LOV request fails | Do not retry automatically or substitute a different endpoint. |

## Documented Guided Setup — Explicit Manual UI Only

1. In Setup and Maintenance, use Offering Sales and Functional Area Sales Foundation, then open Manage Activity Type and Subtype.
2. Select the activity type and associate it with the intended activity functions.
3. On the subtype page, select the activity type, add or review the subtype, and select Enabled for a new subtype.
4. Save and Close. This guidance does not claim that a change has been performed or verified.

## Documented CSV Automation Route

| Sequence | Required Gate | What Must Happen |
|---|---|---|
| 1 | Source package | Use either the completed template-export ZIP for ORA_ZMM_MANAGE_ACTIVITY_TYPE_SUBTYPE or a verified completed data-export ZIP for that exact task. |
| 2 | Package preparation | For a completed data-export ZIP, extract it, add or update only the reviewed subtype row in ORA_ZMM_ACTIVITY_SUBTYPE.csv, and create a new ZIP that retains the task metadata. |
| 3 | Immutable preview | Validate the exact new ZIP and its existing parent activity type, then build the Data Loader preview. |
| 4 | Approval | Obtain approval bound to that exact preview. |
| 5 | Import | Submit the approved ZIP through the documented setup-task CSV import endpoint. |
| 6 | Verification | Retrieve the import result or ProcessLog once, then verify the subtype through the read-only LOV. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY.EXECUTION_GATE | decision | 8 | execution_gate | csv_import_candidate->ACTIVITY.IMPORT_READY;ui_guidance->ACTIVITY.UI_GUIDANCE_READY;default_data_loader->ACTIVITY.IMPORT_READY;ui_required_for_unsupported_scope->ACTIVITY.BLOCKED;direct_rest_requested->ACTIVITY.BLOCKED | ACTIVITY.VERIFY_CSV_SOURCE | stop | After validation: default supported subtype mutations to Data Loader/FSM import; manual UI is explicit or required when the subtype-only package cannot represent the requested scope. |
| ACTIVITY.IMPORT_READY | terminal | 9 | terminal | none | ACTIVITY.EXECUTION_GATE | continue | A verified task CSV source package for a supported subtype change is ready for the default Core Data Loader import adapter. |
| ACTIVITY.UI_GUIDANCE_READY | terminal | 10 | terminal | none | ACTIVITY.EXECUTION_GATE | continue | The requester explicitly selected manual UI and the documented procedure is ready for an authorized user; no Fusion side effect has been performed. |
| ACTIVITY.BLOCKED | terminal | 11 | terminal | none | none | continue | Input, task access, lookup, source-package, design, preview, approval, or direct-CRM-write gate blocks the requested work. |
| ACTIVITY.FAILED | terminal | 12 | terminal | none | none | continue | A documented read-only lookup, source-package validation, or template-status call fails. |
