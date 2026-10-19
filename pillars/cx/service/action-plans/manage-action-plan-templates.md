---
task_code: "ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES"
task_name: "Manage Action Plan Templates"
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

# Manage Action Plan Templates

## Setup Task Metadata

- Task name: `Manage Action Plan Templates`
- Task code: `ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES`
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

### Review Action Plan Templates

Review existing Action Plans templates and their action flows before creating or changing a template.

1. Export Action Plans templates with shared.setup-export.task-level-export.
2. Review each template's name, calendar, category, context, stripe code, effective dates, publication and auto-start settings, description, action order, prerequisites, and mandatory settings.

### Create Action Plan Template

Create a parent-only Action Plans Template for later selection in an action plan.

1. Export Action Plans templates with shared.setup-export.task-level-export.
2. Ask whether Template Actions are requested. If yes, offer selection from existing Fusion actions or separately approved creation of new actions; if no, record the explicit parent-only choice.
3. For a requested link to an existing template, verify the selected existing or freshly created action identity through the supported Fusion read API, then collect its target TemplateNumber, order, and mandatory setting. Omit TemplateNumber for a new parent; Fusion generates it and fresh read-back establishes it before separately approved linkage.
4. When a calendar or coverage value is supplied, resolve it through subscriptionCoverageSchedules with expand=SubscriptionCoverageInterval. Do not ask for a schedule or populate CalendarId when no value is supplied.
5. Use the completed export of the same setup task as the package baseline and add a parent ORA_SVC_AP_TEMPLATES row with only the supplied parent CSV fields: ActionPlanTypeCd, CalendarId, DeletedFlag, Description, EnabledFlag, EndDate, Name, ObjectEntityName, StartDate, StripeCd, ObjectEntityNameMeaning, StripeCdMeaning, and ActionPlanTypeCdMeaning. Populate CalendarId only from a matched supplied schedule value.
6. Do not require or synthesize TemplateNumber, action identities, TemplateActionNumber, or child linkage for a parent-only import.
7. Omit ORA_SVC_TEMPLATE_ACTION and ORA_SVC_ACTION_RELATION data when the template has no action-flow mappings or prerequisites.
8. Validate the FSM package with shared.validation.setup-data-validator.
9. Import the approved ZIP with core.data-loader.
10. Verify the parent template with a fresh export.

### Create Template Action

Add one existing action to an Action Plans Template action flow.

1. Ask the user to identify the target template by TemplateNumber and provide the selected action, order, and mandatory setting for every link.
2. Verify every selected ActionNumber through the supported Fusion read API before package construction.
3. Export Action Plans templates with shared.setup-export.task-level-export.
4. Retain the selected parent ORA_SVC_AP_TEMPLATES row and add an ORA_SVC_TEMPLATE_ACTION row using the parent's TemplateNumber as linkage, plus the selected action identity, order, and mandatory setting. Omit TemplateActionNumber for a new child; retain it only for an existing-child update.
5. Omit ORA_SVC_ACTION_RELATION data unless prerequisite relationships are requested.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the template action flow with a fresh export.

### Create Template Action Prerequisite

Create a prerequisite relationship between two actions already added to the same Action Plans Template.

Not supported. Oracle documentation supports selecting prerequisite actions for a template action, but the repository has no authoritative FSM import contract for ORA_SVC_ACTION_RELATION rows, the related template-action identities, or RelationId values; do not construct or import relationship rows.

### Update Action Plan Template

Update an existing unpublished Action Plans template while retaining its validated action flow.

1. Export Action Plans templates with shared.setup-export.task-level-export.
2. Retain the selected template's exported identity and update only approved calendar, category, context, stripe code, effective dates, auto-start setting, description, action order, prerequisites, or mandatory settings.
3. Retain the exported action flow and modify only approved actions and relationships; do not introduce unsupported child rows or infer generated identities.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the template and action flow with shared.setup-export.task-level-export.
## Purpose

Create templates that will be associated to action plans.
## FSM Contract

### ORA_SVC_AP_TEMPLATES

- `TemplateNumber`: Omit the column for a new parent template; Fusion generates it. Retain the exported identity for an existing-parent update.
- `ActionPlanTypeCd`: Populate only the approved template category code.
- `CalendarId`: Populate only from a matched supplied schedule value; otherwise omit it for a new parent.
- `DeletedFlag`: Retain the exported value unless an approved supported lifecycle change requires it.
- `Description`: Populate only the approved description.
- `EnabledFlag`: Populate only the approved enabled state.
- `EndDate`: Populate only the approved effective end date.
- `Name`: Populate the approved template name.
- `ObjectEntityName`: Populate only the approved template context.
- `StartDate`: Populate only the approved effective start date.
- `StripeCd`: Set to the applicable Service Request category stripe, such as ORA_SVC_CRM, ORA_SVC_HCM, ORA_SVC_HRHD, or ORA_SVC_ISR. Retain the exported value for an existing category.
- `BUOrgId`: Retain the exported value for an existing template; omit it for a new parent unless the supported create contract requires it.
- `BusinessUnitName`: Retain the exported value for an existing template; omit it for a new parent unless the supported create contract requires it.
- `ObjectEntityNameMeaning`: Retain the export-derived display value when required by the package contract.
- `StripeCdMeaning`: Retain the export-derived display value when required by the package contract.
- `ActionPlanTypeCdMeaning`: Retain the export-derived display value when required by the package contract.
- `AutoStartFlag`: Retain the exported value for an existing template; omit the column for a new parent.
- `UsageTypeCd`: Retain the exported value for an existing template; omit the column for a new parent.

### ORA_SVC_TEMPLATE_ACTION

- `ORA_SVC_AP_TEMPLATES.TemplateNumber`: Use the fresh, selected parent TemplateNumber as parent linkage.
- `ActionId`: Populate only a selected, verified action identity.
- `OrderNumber`: Populate the approved action-flow order.
- `DeletedFlag`: Retain the exported value unless an approved supported lifecycle change requires it.
- `MandatoryFlag`: Populate the approved required or optional behavior.
- `ObjectEntityType`: Populate only the selected action's supported object entity type.
- `SystemUpdate`: Retain the export-derived value when required by the package contract.
- `ActionNumber`: Populate only the selected, verified action number.
- `TemplateActionNumber`: Omit the column for a new child; Fusion generates it. Retain the exported identity only for an existing-child update.

### ORA_SVC_ACTION_RELATION

- `ORA_SVC_AP_TEMPLATES.TemplateNumber`: Retain the selected parent's exported TemplateNumber as parent linkage for an existing relationship.
- `ORA_SVC_TEMPLATE_ACTION.ActionId`: Retain the exported dependent action identity for an existing relationship.
- `ORA_SVC_TEMPLATE_ACTION.OrderNumber`: Retain the exported dependent action order for an existing relationship.
- `DepTemplateActionId`: Retain the exported prerequisite action identity for an existing relationship.
- `DeletedFlag`: Retain the exported value unless an approved supported lifecycle change requires it.
- `ActionStatusCd`: Retain the exported relationship status when required by the package contract.
- `TemplateActionNumber`: Retain the exported dependent template-action identity for an existing relationship.
- `TemplateActionTemplateActionId`: Retain the exported prerequisite template-action identity for an existing relationship.
- `ActionStatusCdMeaning`: Retain the export-derived display value when required by the package contract.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create or update records. The only deletion exception is no-ship test rollback of independently created, group-owned fixtures: after separate explicit approval, delete each recorded template-action link through `actiontemplates/{TemplateId}/child/templateAction/{TemplateActionId}`, then each recorded template through `actiontemplates/{TemplateId}`, and finally each recorded action through `actions/{ActionNumber}`. Verify every deletion with a fresh read. This exception must never target a pre-existing record, substitute for FSM restoration, or be used for normal setup work.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Action Plans`
- Setup task name: `Manage Action Plan Templates`
- Setup task code: `ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Action Plan Templates` under `Action Plans`.
