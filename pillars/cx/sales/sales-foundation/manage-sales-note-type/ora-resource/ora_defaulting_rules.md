# Sales Note Type Defaulting Rules

Apply only task-intrinsic or explicitly documented defaults. Do not invent a business-object mapping, translation, or effective end date.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | ZMM_NOTE_TYPE scope and enabled creation behavior |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Lookup enablement and effective-date behavior |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| LookupType | ZMM_NOTE_TYPE | Always | No |  |
| EnabledFlag | Yes | Operation is Create, the requester wants the new type immediately usable, and EnabledFlag is omitted | No |  |
| EndDate | No automatic default | Create, Update, or Deactivate | No |  |
| SourceObjectCode | No automatic default | A mapping or runtime validation is requested | No |  |
| DefaultFlag | No automatic default | The downstream mapping task is required | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_NOTE.DEFAULTS | step | 4 | apply_default | defaults_applied->SALES_NOTE.DESIGN;no_default_needed->SALES_NOTE.DESIGN;invalid_default_context->SALES_NOTE.FAILED | SALES_NOTE.RUNTIME_LOOKUP | stop | Always |
