---
task_code: "ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS"
task_name: "Manage Action Plan Actions"
parent_skill_id: "cx.service.action-plans"
pillar: "CX"
offering: "Service"
functional_area: "Action Plans"
functional_area_code: "ORA_SVC_ACTION_PLANS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Action Plan Actions

## Setup Task Metadata

- Task name: `Manage Action Plan Actions`
- Task code: `ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``






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
## Use Cases

### Review Action Plan Actions

Review existing Action Plans actions before defining or changing an action.

1. Export Action Plans actions with shared.setup-export.task-level-export.
2. Review each action's name, business unit, stripe code, category, type, context, duration, visibility, description, attribute mappings, status mappings, dependencies, and errors.

### Create Action Plan Action

Create an Action Plans action for later selection in an action-plan template.

1. Export Action Plans actions with shared.setup-export.task-level-export.
2. When attribute mappings are requested, resolve the complete candidate attribute list for the selected ObjectEntityName through resolve_object_entity_attribute_metadata before asking the user to select mappings. Do not treat attributes observed in existing Action Plans exports as the complete supported set.
3. Use the completed export of the same setup task as the package baseline and add an action with its approved name, business unit, stripe code, category, type, context, duration, visibility, and required attribute mappings. Do not ask for or populate ActionNumber for a new action; Fusion generates it and fresh read-back establishes the resulting identity.
4. Derive the FSM package shape from the task export, ASM_SETUP_CSV_METADATA.xml, and task-specific documented requirements. Do not require a sample or known-good successful create package; resolve any remaining field through an explicit requested value, documented rule, or validated omission.
5. Add only approved status mappings, dependencies, error handling, and attachment-copy behavior that are supported for the selected action type and context.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the action and its configured mappings with a fresh export.
9. For an Actions-only create or update, do not ask for or include TemplateNumber. Only when the user separately requests a template creation or update that links the action, collect the target TemplateNumber, generated action identity, order, and mandatory setting, then route linkage to Manage Action Plan Templates as a separate preview and approval-controlled operation.

### Update Action Plan Action

Update an existing Action Plans action without changing its identity or type unintentionally.

1. Export Action Plans actions with shared.setup-export.task-level-export.
2. When adding or changing attribute mappings, resolve the complete candidate attribute list for the action's exported ObjectEntityName through resolve_object_entity_attribute_metadata before asking the user to select mappings. Do not treat attributes observed in existing Action Plans exports as the complete supported set.
3. Retain the selected action's exported identity and update only approved business unit, stripe code, category, context, duration, visibility, description, attribute mappings, status mappings, dependencies, errors, or attachment-copy behavior.
4. Retain required mappings and validate that every changed setting is supported for the action's existing type and context.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the action and its configured mappings with a fresh export.

### Configure Dynamic Process Action Mappings

Configure attribute mappings or a status mapping for a Dynamic Process action.

Not supported. Dynamic Process actions cannot include attribute or status mappings.
## Purpose

Create actions that will be used in templates and action plans.
## FSM Contract

### ORA_SVC_AP_ACTIONS

- `ActionNumber`: Omit the column for a new root action; Fusion generates it. Retain the exported identity for an existing-root update.
- `ActionCategoryCd`: Populate only an approved category code supported by the same-task export.
- `DeletedFlag`: Retain the exported value unless an approved supported lifecycle change requires it.
- `Description`: Populate only the approved description.
- `LastUpdatedBy`: Retain the exported value when the package contract requires it.
- `LeadTime`: Populate only the approved duration.
- `LeadTimeUnit`: Populate only the approved duration unit supported by the same-task export.
- `Name`: Populate the approved action name.
- `ObjectEntityName`: Populate only the approved action context.
- `ParentEntityName`: Populate only the approved parent context.
- `VisibilityCd`: Populate only the approved visibility code.
- `OperationCd`: Populate only the approved operation code.
- `ObjectEntityType`: Populate only the approved action type.
- `OriginalSystemReference`: Retain the exported value or omit only when the create contract accepts omission.
- `ProcessConnectionTypeCd`: Populate only an approved Dynamic Process connection type.
- `ProcessMetadataId`: Populate only an approved Dynamic Process metadata identifier.
- `UseDefaultVersionFlag`: Populate only an approved Dynamic Process default-version setting.
- `StripeCd`: Set to the applicable Service Request category stripe, such as ORA_SVC_CRM, ORA_SVC_HCM, ORA_SVC_HRHD, or ORA_SVC_ISR. Retain the exported value for an existing category.
- `BUOrgId`: Retain the exported value for an existing action; do not infer it for a new action.
- `BusinessUnitName`: Populate only the approved business unit and do not infer it from another action.
- `LeadTimeUnitMeaning`: Retain the export-derived display value when required by the package contract.
- `ActionCategoryCdMeaning`: Retain the export-derived display value when required by the package contract.
- `VisibilityCdMeaning`: Retain the export-derived display value when required by the package contract.
- `OperationCdMeaning`: Retain the export-derived display value when required by the package contract.
- `StripeCdMeaning`: Retain the export-derived display value when required by the package contract.
- `ObjectEntityNameMeaning`: Retain the export-derived display value when required by the package contract.
- `ParentEntityNameMeaning`: Retain the export-derived display value when required by the package contract.
- `ObjectEntityTypeMeaning`: Retain the export-derived display value when required by the package contract.
- `ProcessMetadataNumber`: Retain or populate only with approved Dynamic Process metadata evidence.
- `ProcessMetadataProcessMetadataId`: Retain or populate only with approved Dynamic Process metadata evidence.
- `ObjectEntitySubtype`: Populate only when approved and supported by the selected action type and context.
- `ObjectLinkTypeId`: Populate only a verified object-link-type identity.
- `CopyAttachmentsFlag`: Populate only the approved attachment-copy behavior.
- `ObjectLinkTypeNumber`: Populate only a verified object-link-type number.
- `UsageTypeCd`: Retain or populate only when supported by the selected action type and context.
- `AiFlag`: Omit for a new root action; retain the exported value for an existing-root update.
- `AiModeCd`: Omit for a new root action; retain the exported value for an existing-root update.
- `AsyncModeCd`: Omit for a new root action; retain the exported value for an existing-root update.

### ORA_SVC_ACTION_ATTRIBUTE

- `ORA_SVC_AP_ACTIONS.ActionNumber`: Use the owning action's exported or fresh-read-back ActionNumber as parent linkage.
- `AttributeName`: Populate only an approved attribute supported by the selected action type and context.
- `AttributeValue`: Populate only the approved value for AttributeName.
- `AttributeValueContextCd`: Populate only the approved attribute-value context.
- `DeletedFlag`: Retain the exported value unless an approved supported lifecycle change requires it.
- `LastUpdatedBy`: Retain the exported value when the package contract requires it.
- `UsageCd`: Populate only the approved attribute usage.
- `DisplayLabel`: Populate only the approved display label.
- `ActionNumber`: Retain the child identity/linkage value only when required by the same-task package contract.
- `ActionActionId`: Retain the exported child identity for an existing-child update; do not invent it for a new child.
- `UsageCdMeaning`: Retain the export-derived display value when required by the package contract.
- `AttributeValueContextCdMeaning`: Retain the export-derived display value when required by the package contract.
- `ChildAttributeFlag`: Populate only the approved child-attribute behavior.

### ORA_SVC_ACTION_CONDITION

- `ORA_SVC_AP_ACTIONS.ActionNumber`: Use the owning action's exported or fresh-read-back ActionNumber as parent linkage.
- `ActionStatusCd`: Populate only an approved action status supported by the selected action type and context.
- `Condition`: Populate only the approved condition expression.
- `CompletionFlag`: Populate only the approved completion behavior.
- `Description`: Populate only the approved description.
- `LastUpdatedBy`: Retain the exported value when the package contract requires it.
- `Name`: Populate only the approved condition name.
- `ActionNumber`: Retain the child identity/linkage value only when required by the same-task package contract.
- `ActionActionId`: Retain the exported child identity for an existing-child update; do not invent it for a new child.
- `ActionStatusCdMeaning`: Retain the export-derived display value when required by the package contract.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create or update records. The only deletion exception is no-ship test rollback of independently created, group-owned actions through `actions/{ActionNumber}` after separate explicit approval and a fresh read-back. This exception must never target a pre-existing action, substitute for FSM restoration, or be used for normal setup work.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Action Plans`
- Setup task name: `Manage Action Plan Actions`
- Setup task code: `ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Action Plan Actions` under `Action Plans`.
