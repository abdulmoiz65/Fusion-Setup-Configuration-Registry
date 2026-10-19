# Time Device Export Data Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Description | No default | Description is omitted | No | |
| Start Date | No default | Start Date is omitted | No | |
| Number Of Days in Period | No default | Number Of Days in Period is omitted | No | |
| Number Of Objects in Batch | No default | Number Of Objects in Batch is omitted | No | |
| First Name | No default | First Name is omitted | No | |
| Last Name | No default | Last Name is omitted | No | |
| Badge ID | No default | Badge ID is omitted | No | |
| Payroll Time Types | No default | Payroll Time Types is omitted | No | |
| Schedule | No default | Schedule is omitted | No | |

## Defaulting Boundaries

| Situation | What Happens |
|---|---|
| An optional field is omitted | Preserve the omission; do not invent a value. |
| A user-facing default is actually applied by a documented rule | Include that default in Defaults Applied using its business label and verified business display value. |
| No default is applicable | Still generate Defaults Applied with its headers and no data rows. |

## Complete Summary Display Rules

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Identifier display | Replace an identifier with its resolved business display name | A populated identifier would otherwise be shown | No | |
| Code display | Replace a code with its verified business meaning | A populated code would otherwise be shown | No | |
| Checkbox display | Use Selected or Not selected when a verified business label is available | A populated checkbox value is shown | No | |
| Status display | Use a verified business-friendly status such as Draft or Submitted | A populated internal status is shown | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEDEXPORT_APPLY_DEFAULTS | step | 3 | apply_default | applied->TDEDEXPORT_ENFORCE_SUMMARY;not_applicable->TDEDEXPORT_ENFORCE_SUMMARY;blocked->TDEDEXPORT_DEFAULTS_BLOCKED | TDEDEXPORT_SEARCH_EXPORT_DATA | stop | A request passed input validation and the required criteria search |
