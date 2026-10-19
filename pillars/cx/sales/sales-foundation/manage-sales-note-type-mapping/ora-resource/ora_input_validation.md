# Sales Note Type Mapping Input Validation

Validate the requested mapping operation, object context, note-type code, default decision, effective date, and migration inputs before presenting guided setup or an authorized CSV handoff. This resource does not perform a Fusion write.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Mapping fields, object selection, optional end date, and explicit Default decision |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Object-specific mapping and Default Note Types behavior |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | Runtime source-object and mapped-code field shapes |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-object-metadata.html | Object Metadata REST boundary; its `ObjectCode` must not be substituted for the mapping `SourceObjectCode` |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | ZMM_NOTE_TYPE lookup-code verification |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Operation: Review, Create, Update, EndDate, Export, Import, or ValidateRuntimeAvailability | Block the workflow | State the intended mapping operation | Always |  |
| Business-object selection | BusinessObjectName for guided setup, or SourceObjectCode for runtime validation | Block only the affected operation | Supply the exact catalogued UI business object or source-object code from `ora_supported_object_codes.md` | Review, Create, Update, EndDate, or ValidateRuntimeAvailability |  |
| Mapped note type | MappedLookupCode | Block the mapping-specific workflow | Supply the exact ZMM_NOTE_TYPE lookup code | Create, Update, EndDate, or ValidateRuntimeAvailability | find_active_sales_note_type_code |
| Default decision | DefaultFlag: Y or N | Block guided setup or import preview | State whether the mapping is a default according to the approved design | Create, or Update changes the Default field |  |
| First object-specific mapping decision | PreserveEffectiveList: Preserve or Restrict | Block the workflow | State whether the object should retain all currently effective values or only the explicitly requested values | Create when the current export has no persisted mapping row for the object | find_effective_note_type_for_object |
| Mapping end date | EndDate in ISO YYYY-MM-DD format | Block end-date guidance or import preview | Supply an unambiguous end date | Operation is EndDate, or Update supplies EndDate |  |
| Runtime object context | SourceObjectCode | Block the runtime lookup only | Supply the exact source object code whose effective note types must be checked | Operation is ValidateRuntimeAvailability |  |
| CSV package | Current template or completed export ZIP for ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING | Block import handoff | Export the current task-specific package and preserve its template-derived files and headers | Operation is Import |  |
| Approval | Immutable preview approval | Block import handoff | Obtain approval bound to the exact normalized package, target environment, and preview | Operation is Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task boundary | Use ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING. Route creation or maintenance of ZMM_NOTE_TYPE lookup codes to Manage Sales Note Type. | Always |  |
| Business-object identity | Reject a blank, approximate, or inferred business object. Treat Default Note Types as an explicit setup selection, not as an unnamed object. | A mapping object is required |  |
| Supported object and code | Use the exact UI-label-to-`SourceObjectCode` pair in `ora_supported_object_codes.md`. Do not uppercase, snake-case, pluralize, or substitute the `ObjectCode` returned by Object Metadata; several mapping codes use a different form. For a code absent from the catalog, require a current UI selection or positive runtime evidence before proceeding. | A mapping object or source code is supplied |  |
| Exported object list | The absence of an exact business object from `ZMM_OBJECT_LOOKUP_MAPPING.csv` is no evidence that the object is unsupported. Every imported mapping row must have a matching parent row in `ORA_OBJECT_LOOKUP.csv`. Use the exported parent row when present. When it is absent but the exact UI label and `SourceObjectCode` are catalogued in `ora_supported_object_codes.md`, add the controlled parent row defined there: `ObjectCode=SourceObjectCode`, `ObjectName=Setup-page business object`, `ObjectDesc=` blank, `DeletedFlag=N`, `ModuleId=` blank, and `LastUpdatedBy=` the authorized setup owner evidenced by the fresh target export. Do not construct a parent for a code absent from that catalog. | Create or Import |  |
| Mapped-code shape | Reject spaces and a MappedLookupCode longer than 30 characters. Preserve the exact stable lookup code. | MappedLookupCode is supplied |  |
| Existing enabled note type | Require exactly one applicable ZMM_NOTE_TYPE row whose LookupCode equals MappedLookupCode and whose enabled and effective state permits use. | Create, Update, EndDate, or ValidateRuntimeAvailability | find_active_sales_note_type_code |
| Default flag | Accept only Y or N; do not infer the value from the operation or from another mapping. | DefaultFlag is supplied or required |  |
| End-date shape | Require ISO YYYY-MM-DD. Do not invent an end date or treat omission as deactivation. | EndDate is supplied |  |
| Explicit mapping identity | Treat BusinessObjectName or SourceObjectCode plus MappedLookupCode as the business identity for review and preview. Do not select an approximate row. | Update or EndDate |  |
| First object-specific mapping scope | When the current export has no persisted row for the exact object, require an explicit Preserve or Restrict decision. Preserve requires the complete desired list and each row's DefaultFlag; Restrict permits only the explicitly approved rows. Do not copy inherited Default Note Types merely because they are effective at runtime. | Create | find_effective_note_type_for_object |
| CSV schema | Reject a hand-built or stale CSV schema. Accept only files and columns derived from the current package for task code ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING. | Operation is Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.VALIDATE | step | 1 | validate_input | valid->NOTE_MAPPING.DEPENDENCIES;missing_or_invalid->NOTE_MAPPING.FAILED | none | stop | Always |
