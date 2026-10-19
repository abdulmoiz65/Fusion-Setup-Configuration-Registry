# Sales Note Type Input Validation

Validate the requested note-type operation before presenting guided setup, checking runtime availability, or handing a CSV package to an authorized setup-data workflow. This resource does not perform a Fusion write.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | ZMM_NOTE_TYPE creation fields and the mapping follow-up |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Note-type purpose, business-object mapping, and default-note behavior |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Lookup codes, enablement, effective dates, configuration levels, translations, and deletion limits |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | Runtime mapped-code and meaning lengths and read-only response fields |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Operation: Review, Create, Update, Deactivate, Translate, Export, Import, or ValidateRuntimeAvailability | Block the workflow | State the intended note-type operation | Always |  |
| Note-type identity | NoteTypeCode | Block the workflow | Provide the exact lookup code | Review, Update, Deactivate, Translate, Export, Import, or ValidateRuntimeAvailability |  |
| New note-type definition | NoteTypeCode, Meaning, Description, EnabledFlag | Block guided setup or import preview | Provide the code, display meaning, description, and intended enabled state | Operation is Create |  |
| Effective dating | StartDate and EndDate when either is supplied | Block guided setup or import preview | Provide dates in an unambiguous ISO format and keep EndDate on or after StartDate | Operation is Create, Update, or Deactivate |  |
| Translation | Language, TranslatedMeaning, and optional TranslatedDescription | Block translation guidance | Provide one enabled target language and translated meaning per requested translation | Operation is Translate |  |
| Runtime object context | SourceObjectCode | Block the runtime lookup only | Provide the exact source object code whose available note types must be checked | Operation is ValidateRuntimeAvailability |  |
| CSV package | Current template or completed export ZIP for ZBS_MANAGE_SALES_NOTE_TYPE | Block import handoff | Export the current task-specific package and preserve its template-derived files and headers | Operation is Import |  |
| Approval | Immutable preview approval | Block import handoff | Obtain approval bound to the exact normalized package and preview | Operation is Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Fixed lookup type | Use ZMM_NOTE_TYPE. Reject a request that targets another lookup type as outside this setup task. | Create, Update, Deactivate, or Translate |  |
| Lookup code shape | Reject spaces in NoteTypeCode; use underscores between words. Treat a mapped runtime code longer than 30 characters as invalid. | NoteTypeCode is supplied |  |
| Meaning shape | Require a nonblank Meaning or TranslatedMeaning. Treat a mapped runtime meaning longer than 80 characters as invalid. | Create, Update, or Translate |  |
| Date order | Reject an EndDate earlier than StartDate. | Both dates are supplied |  |
| Deactivation intent | Require EnabledFlag=No, an EndDate, or both; do not infer which control the requester intends. | Operation is Deactivate |  |
| Editability | Do not promise an update or deletion until the lookup configuration level and predefined-data status permit it. | Update or Deactivate |  |
| Task boundary | Do not treat SourceObjectCode or a requested default mapping as a field of this task. Route object mapping to Manage Sales Note Type Mapping. | A business-object mapping is requested |  |
| CSV schema | Reject a hand-built or stale CSV schema. Accept only files and columns derived from the current package for task code ZBS_MANAGE_SALES_NOTE_TYPE. | Operation is Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_NOTE.VALIDATE | step | 1 | validate_input | valid->SALES_NOTE.DEPENDENCIES;missing_or_invalid->SALES_NOTE.FAILED | none | stop | Always |
