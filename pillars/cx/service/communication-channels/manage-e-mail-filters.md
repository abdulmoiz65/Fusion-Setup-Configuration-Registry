---
task_code: "ORA_SVC_MANAGE_EMAIL_FILTERS"
task_name: "Manage E-Mail Filters"
parent_skill_id: "cx.service.communication-channels"
pillar: "CX"
offering: "Service"
functional_area: "Communication Channels"
functional_area_code: "ORA_SVC_COMM_CHANNELS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage E-Mail Filters

## Setup Task Metadata

- Task name: `Manage E-Mail Filters`
- Task code: `ORA_SVC_MANAGE_EMAIL_FILTERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``


## FSM Contract

### ORA_SVC_INBOUND_MSG_FILTER

- `FilterTypeCd`: Use core.fusion-api.apps-common to read enabled standard lookup codes for ORA_SVC_INBND_FLTR_FIELD_TYPE, then set an approved enabled code. Required for a new filter; retain the exported value unless an approved update changes it.
- `FieldName`: Set only when required by the selected filter type; otherwise retain the exported value or omit only when same-task package evidence supports omission.
- `Pattern`: Set to the approved sender or subject regular-expression pattern. Required for a new filter; retain the exported value unless an approved update changes it.
- `OrderNumber`: Leave blank for a new filter. Retain the exported value for an update; do not populate or change filter order unless an explicitly approved change requires it.
- `Description`: Set to the approved description when supplied; otherwise retain the exported value or omit only when same-task package evidence supports omission.
- `CustomFilterFlag`: Required for a new filter. Set it to Y; do not leave it blank. For an existing filter, retain the exported value unless an approved change explicitly targets it.
- `DeletedFlag`: Required for a new filter. Set it to N; do not leave it blank or set it to delete a filter. For an existing filter, retain the exported value unless an approved change explicitly targets it.
- `ClientApplicationName`: Set to SvcMessagingClient for a new filter. Retain the exported value for an update unless an approved change explicitly supplies a different supported value.
- `CreatedBy`: Retain the exported value; do not supply a new value unless same-task package evidence requires it.
- `LastUpdatedBy`: Retain the exported value unless the completed same-task package and validation require an approved update value.
- `LastUpdateLogin`: Retain the exported value unless same-task package evidence requires an update.
- `ActionCd`: Use core.fusion-api.apps-common to read enabled standard lookup codes for ORA_SVC_INBND_FLTR_ACTION_TYPE, then set an approved enabled code. Required for a new filter; retain the exported value unless an approved update changes it.
- `UpdateFlag`: Retain the exported value when it is present. Otherwise leave the CSV column blank; do not use it as an inferred replacement for a missing FilterId.
- `DeleteFlag`: Retain the exported value when it is present. Otherwise leave the CSV column blank; do not use it to delete a filter.
- `ActionCdMeaning`: Retain the exported display value unless the completed same-task package and validation require it to change with ActionCd.
- `FilterTypeCdMeaning`: Retain the exported display value unless the completed same-task package and validation require it to change with FilterTypeCd.

### Exported Package

- `CSVMember`: Use ORA_SVC_INBOUND_MSG_FILTER.csv from the completed export of this same setup task.
- `XmlNodePath`: Use /InboundMsgFiltersVO/InboundMsgFiltersVORow.
- `NodeSequence`: Use 1.
- `UpdateIdentity`: FilterId and DisabledFlag are not members of this FSM CSV package. Resolve an existing row only from same-task export evidence and the approved update selection; do not add undeclared identity or state columns.
## Purpose

Manage inbound message filters that evaluate sender or subject patterns and reject matching inbound emails.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## Use Cases

### View Inbound Message Filters

View inbound message filters and their filter type, field name, pattern, action, description, and disabled status.

1. Retrieve inbound message filters with core.fusion-api.rest-api-client through the documented inboundMsgFilters REST GET endpoint.

### Create Inbound Message Filter

Create an inbound message filter for a sender or subject regular-expression pattern.

1. Export inbound message filters with shared.setup-export.task-level-export.
2. Use the completed export of the same setup task as the package baseline; preserve its package structure and modify only task-owned rows required for the approved change.
3. Provide FilterTypeCd, Pattern, ActionCd, CustomFilterFlag=Y, DeletedFlag=N, and ClientApplicationName=SvcMessagingClient for a new filter; optionally provide FieldName and Description. Leave OrderNumber, UpdateFlag, and DeleteFlag blank when absent from the same-task export.
4. Use core.fusion-api.apps-common to read enabled standard lookup codes for ORA_SVC_INBND_FLTR_FIELD_TYPE and ORA_SVC_INBND_FLTR_ACTION_TYPE, then validate the requested filter type and action codes and check the alternate key for a duplicate filter.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the created filter with a fresh export.

### Update Inbound Message Filter

Update an existing inbound message filter's field name, pattern, description, action, or disabled status.

1. Export inbound message filters with shared.setup-export.task-level-export.
2. Use the completed export of the same setup task as the package baseline; retain the selected filter's exported identity and change only approved fields.
3. Select the existing row using same-task export evidence and provide only approved FSM CSV fields to update; do not add FilterId because it is not a member of the exported package.
4. Retrieve the existing filter and use core.fusion-api.apps-common to validate any changed filter type or action lookup code against its enabled standard lookup codes.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the updated filter with a fresh export.

### Delete Inbound Message Filter

Delete an inbound message filter.

Not supported. Delete is outside the supported Manage E-Mail Filters workflow; do not generate or execute a delete operation from this task metadata.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Communication Channels`
- Setup task name: `Manage E-Mail Filters`
- Setup task code: `ORA_SVC_MANAGE_EMAIL_FILTERS`

## FSM Data Loader Package Requirements

1. Read the task's fsm_contract first when it is present. Treat its objects and field guidance as the task-specific starting point for classifying each requested change as an existing-root update, new root, existing-child update, new child of an existing parent, new relationship, or mixed package change.
2. Read `ASM_SETUP_CSV_METADATA.xml` in the task export package for business objects, XML paths, node sequence, attributes, scope, and relationships; reconcile it with the task's fsm_contract when one is present.
3. Use the fsm_contract object and field guidance together with metadata-defined node sequence and relationships to determine package order and required object coverage.
4. Verify the selected baseline or template package includes the members, file names, structure, headers, encoding, scope, relationship rows, and fsm_contract objects and fields required for the requested change.
5. Treat a completed export of this same setup task as authoritative evidence for package structure, headers, node order, key and linkage shape, and generated-identity handling. Use it to corroborate the fsm_contract and record provenance for copied template values.
6. For existing-row updates, retain exported identities and all unchanged values, parent rows, child rows, and relationships required by the fsm_contract and package evidence; do not carry unrelated baseline rows into the change package unless they are required for import integrity. Change only approved fields.
7. For a new child or relationship, retain the existing parent identity and use only linkage, keys, and required values specified by the fsm_contract or confirmed by same-task package evidence.
8. For greenfield rows, construct the create contract from the fsm_contract, task-specific documented requirements, `ASM_SETUP_CSV_METADATA.xml`, a completed export of this same task, and supported preview or dry-run results where available.
9. An export whose data CSV members contain only headers is valid structural evidence for a greenfield contract, not an automatic blocker. Use the fsm_contract, exported package structure, and explicit supported inputs to construct the rows; stop only when required fields, keys, relationships, or values remain unresolved or validation rejects the package.
10. Populate every root, child, scoped, localized, and relationship object required by the fsm_contract or confirmed package contract. Populate approved business keys, required values, and reference values; omit generated identities unless explicitly required.
11. Classify every populated fsm_contract field as request-provided, documented requirement, export-derived structural value, export-derived template value, generated or omittable, or unresolved.
12. A fsm_contract field may be omitted only when it is documented as generated or optional, is absent or consistently blank in semantically comparable exports of this same task, or is accepted as omitted by supported preview or dry-run validation. Do not infer a value solely from a field name or description.
13. Do not copy identities, reference keys, parent keys, scope values, localized values, lookup codes, or behavior-changing settings unless the fsm_contract, request, documented guidance, or approved compatible template default explicitly supports the value.
14. Verify every non-generated parent, lookup, code, scope, locale, and related-object reference required by the fsm_contract against approved same-task package evidence or the workflow's documented resolver; include required parents or relationship rows only when the package contract requires them.
15. Build the complete package required by the fsm_contract and package evidence; never use a child-only package or infer fields, defaults, identities, or relationships from another task or object type.
16. Validate package members, fsm_contract objects and fields, metadata, keys, scopes, references, relationships, node order, field-value provenance, and approved changes before import; confirm that no baseline identity, template-only setting, or unrelated row is introduced or modified unintentionally. Use preview or dry-run validation when available.
17. Stop when a required fsm_contract field or object, identity rule, parent-child linkage, scope, dependency, or behavior-changing setting remains unresolved and lacks an explicit approved value or sufficient same-task evidence. Do not block for fields evidenced as generated or validated-omittable.
## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage E-Mail Filters` under `Communication Channels`.
