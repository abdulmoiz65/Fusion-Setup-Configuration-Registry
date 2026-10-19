# Manage Change Order Types Input Validation

Source: user-provided creation, update, export-package, and approval requirements.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Role Code | Explicit nonblank Role Code from the request or established task context; a role display name alone is insufficient | Stop with input validation error: Role Code is missing from your request. Please provide the Role Code for the role you want to assign. | Ask for the missing code; do not guess from a display name or substitute another role | Creating or updating a role assignment; not preserving an unchanged exported role | |
| Requested operation | Create or update; selected source type for creation or target type for update; requested changes | Return the missing operation, selection, or change details | Obtain the missing request details without introducing a confirmation gate for validation | Every package request | |
| Base Change Type | Explicit base/source change type name or code from the creation request or established task context | Stop with input validation error: Base Change Type is missing from your request. Please provide the name or code of the change type to copy before I can create the new change type. | Ask for the missing Base Change Type; do not default or infer it from the new type name or an unrelated prior selection | Creating a change type | |
| Export package | Exported change-type rows and dependent files, including EGO_CHANGE_HEADER_TYPE | Stop package preparation | Obtain the task export through shared.setup-export.task-level-export under the active workflow | Every package request | |
| Target environment | Exact import target environment | Block import handoff | Resolve the intended target through the active workflow | Before import | |
| Default lookup assignment | For PriorityCode or ReasonCode: exact code; display value when creating a code | Stop package preparation | Resolve through core.fusion-api.apps-common.lookups and the mapped creation task in ora_reference_lookups.md; route import through core.data-loader | When either field is assigned or changed to a nonblank code | resolve_default_lookup |
| Default lookup clearing | Explicit clear/remove request for PriorityCode or ReasonCode with a nonblank current value | Stop package preparation | Resolve the exported target header through ora_reference_lookups.md; validate the explicit clear through final ZIP validation in core.data-loader | When either field is explicitly cleared | resolve_default_lookup_removal |
| Attachment category | When `attachment_category` is supplied for creation: Category Name, User Name, Description, and optional association Start Date | Stop change-order-type package preparation | Route to Manage Attachment Categories for Product Management with Entity Name `EGO_ENGINEERING_CHANGES_B`; use the supplied values only if creation is needed, and use the supplied or defaulted Start Date only for the Change Policy association | Creating a change order type with an attachment category | resolve_attachment_category |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Attachment entity context | Default absent or blank Entity Name to EGO_ENGINEERING_CHANGES_B before invoking the attachment-category resolver; do not report missing Entity Name. Reject an explicitly different entity. Require fresh setup-data evidence for category and entity association; the default itself does not prove existence | An attachment category is requested through Manage Change Order Types | |
| Change Type header date conversion | Validate supplied Start Date and End Date values, then represent them using the corresponding format evidenced in the fresh exported CSV; reject invalid or ambiguous inputs and report when the format cannot be established instead of guessing. Require an omitted Start Date to use the current package-preparation date in that format and disclose the applied dates in the preview | Creating or updating a change type; header dates only | resolve_change_type_dependencies |
| Base Change Type selection | Require a nonblank explicit selection that resolves to exactly one exported type before preparing the creation package; reject an unknown or ambiguous selection and request a valid name or code | Creating a change type | resolve_change_type_relationship |
| Conflicting effectivity inputs | Clarify whether immediate effectivity or delayed effectivity is intended before applying either mapping | Immediate effectivity and positive item-effectivity days are both requested | |
| Effectivity day intent | Do not interpret zero or an omitted day value as a request for immediate effectivity; clarify an explicit day-change request that does not meet the positive-days rule | An explicit day-change request lacks a value greater than zero and immediate effectivity was not requested | |
| Requested field mapping | Validate requested changes against the supplied export's columns and values; report any field that cannot be mapped from the available evidence; do not invent columns or encodings | A requested change must be represented in the package | |
| Default lookup validity | Require one enabled exact code in the lookup mapped to the requested field. For a new code, require creation through the mapped task and a fresh enabled lookup read before setting the field. Never substitute a display value, disabled code, or similar code | PriorityCode or ReasonCode is assigned or changed to a nonblank code | resolve_default_lookup |
| Default lookup removal | Require an explicit removal request for each field to clear and an exported target header with a nonblank requested field. Validate each requested blank field in the exact final ZIP; do not treat an independently valid Start Date or other field change as a clearing validation error. Do not delete, disable, or alter the shared lookup; do not upload if validation rejects blank | PriorityCode or ReasonCode is explicitly cleared | resolve_default_lookup_removal |
| Attachment-category identity | If `attachment_category` is absent, skip this check. If supplied, require a nonblank Category Name and resolve one exact category for `EGO_ENGINEERING_CHANGES_B`; stop for zero or multiple matches | Creating a change order type with an attachment category | resolve_attachment_category |
| Attachment-category creation input | Require nonblank User Name and Description only when the exact category does not already exist and must be created. Pass Category Name, User Name, Description, and Entity Name `EGO_ENGINEERING_CHANGES_B` to the attachment-category skill | Creating a missing requested category | resolve_attachment_category |
| Attachment-category association Start Date | Validate a supplied effective date against the date format evidenced by the supplied Change Order Types export. If omitted, default it to the current date at package preparation in that format; record the applied date and source in the preview. Do not copy an unrelated association date | Creating a change order type with an attachment category | resolve_attachment_category |
| Change Policy association | Require the final package to contain the exact resolved category association for the target Change Policy and its exact nonblank `StartDate`, matching the supplied or recorded defaulted date | Creating a change order type with an attachment category | resolve_attachment_category |


## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COT.VALIDATE_INPUT | step | 10 | validate_input | valid->COT.RESOLVE_EXPORT;invalid->COT.REPORT_ISSUES | none | stop | A create or update package is requested |
