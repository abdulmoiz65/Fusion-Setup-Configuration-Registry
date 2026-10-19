# Performance Document Types Input Validation

Source: Oracle Fusion Cloud Talent Management, Overview of Performance Document Types.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Document type identity | Name | Stop planning | Provide a performance document type name. | Creating a performance document type | |
| Validity period | From Date and To Date | Stop planning | Provide a date range that contains the dates of each performance template that will use the document type. | The document type will be used in a performance template | |
| Availability status | Status | Stop planning | Set the status to Active when the document type must be available for performance templates or performance goal plans. | The document type must be available for use | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| From Date is after a target performance template From Date | Blocked | Set the document type From Date to the same date as or an earlier date than the template From Date. | |
| To Date is before a target performance template To Date | Blocked | Set the document type To Date to the same date as or a later date than the template To Date. | |
| Status is not Active and the document type must be available for a performance template or performance goal plan | Blocked | Set the status to Active. | |
| A request sets an in-use document type to Inactive | Blocked | Retain the document type as Active; the documented restriction prevents inactivation after template or goal-plan use. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name | Require a performance document type name. | Creating a performance document type | |
| Description | Accept an optional description. | A description is supplied | |
| From Date | Require a date on or before the From Date of every performance template that will use the document type. | The document type will be used in a performance template | |
| To Date | Require a date on or after the To Date of every performance template that will use the document type. | The document type will be used in a performance template | |
| Status | Require Active status for availability in performance templates and performance goal plans. | The document type must be available for use | |
| Inactivation | Reject setting the status to Inactive after the document type is used by a performance template or goal plan. | The document type is already used by a template or goal plan | |

| FSM CSV escaping | When creating or regenerating a CSV member, write headers and ordinary values without double quotes. Add double quotes only for an individual value containing a comma, double quote, carriage return, or line feed; double embedded quotes. Reject blanket-quoted CSV members. | FSM CSV import is prepared or revalidated | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.VALIDATE | decision | 10 | validate_input | valid->PERFORMANCE_DOCUMENT_TYPES.LOOKUP_CURRENT;invalid->PERFORMANCE_DOCUMENT_TYPES.STOP_INVALID | none | stop | A Performance Document Type is being created or changed. |
