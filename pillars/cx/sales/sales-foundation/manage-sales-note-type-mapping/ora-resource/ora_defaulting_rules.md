# Sales Note Type Mapping Defaulting Rules

Apply only documented application fallback behavior. Do not invent a business object, default decision, mapping end date, or explicit mapping row.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Mapping field choices and optional end date |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Default Note Types fallback behavior and impact |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| LookupType | ZMM_NOTE_TYPE | A mapped note-type code is validated | No |  |
| BusinessObjectName | No automatic default | Review, Create, Update, or EndDate | No |  |
| SourceObjectCode | No automatic default | Runtime validation is requested | No |  |
| DefaultFlag | No automatic default | Create or Update | No |  |
| EndDate | No automatic default | Create, Update, or EndDate | No |  |
| EffectiveNoteTypeSource | Default Note Types | The selected business object has no object-specific note type mapping | No; this is documented application fallback behavior |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.DEFAULTS | step | 5 | apply_default | defaults_applied->NOTE_MAPPING.DESIGN;no_default_needed->NOTE_MAPPING.DESIGN;invalid_default_context->NOTE_MAPPING.FAILED | NOTE_MAPPING.RUNTIME_LOOKUP | stop | Always |
