# Inventory Task Configurations Input Validation

Data Loader and Fusion own business-object required fields, types, domains, and server-side validation. These rules preserve only Redwood UI conditions and payload normalization before Data Loader handoff.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| FSM template eligibility | Accept an FSM source only when it comes from a verified empty template-only export for `ORA_INVENTORY_TASK_CONFIGURATIONS`, or an equivalent project-local template that passed task code, target environment, release, fingerprint, metadata-marker, member/header, and empty-row checks. | Before native FSM row preparation. | |
| FSM source shape | After core Data Loader classifies an archive containing `ASM_SETUP_CSV_METADATA.xml` as FSM, accept only the exported flattened `ORA_INVENTORY_TASK_CONFIGURATION.csv` columns: OrganizationName, ParCount, CycleCount, PhysicalInventory, PickConfirm, and ReceiptDelivery. | Classified FSM source. | |
| FSM task-generation value | Preserve or map friendly task-generation input to the exact FSM strings Yes and No. Reject REST Y or N values in a classified FSM source. | Classified FSM source. | |
| FSM package preservation | Add approved rows only to the native CSV. Preserve metadata XML, CSV header, encoding, member names, and package structure; reject any artifact that manufactures metadata or replaces the verified template with a loose CSV. | Before Task Hook and Data Loader handoff. | |
| FSM and REST separation | Do not apply REST organization/default-zone lookups, derived ZoneName, activityUsages rows, TaskGroupingLevel, RestAction, or ZoneId rules to a classified FSM source. | Classified FSM source. | |
| Organization XLSX shaping | Apply the organization-resolution contract. Populate OrganizationName in the parent and child rows; leave OrganizationId and OrganizationCode blank. | REST Data Loader source containing OrganizationName. | resolve_inventory_organization_by_name |
| Operation selection | Treat an unqualified request as Create. Accept Update only when the caller explicitly requests it. Create requires no existing default zone; Update requires exactly one existing default zone. | REST Data Loader source. | resolve_default_zone_by_organization_id |
| Start date | Require a calendar date and render it in the XLSX as YYYY-MM-DD. Do not include a time component, localized date format, or spreadsheet serial value. | Every inventoryZoneTaskConfigurations parent row. | |
| Task generation enabled value | Accept the canonical values Y and N. Map approved boolean friendly input to Y or N before handoff; do not send the Redwood UI array representation. | REST activityUsages row supplies TasksEnabled. | |
| UI activity-to-child mapping | Convert every supplied UI section to its child row: Pick confirm -> PICK, Cycle count -> CC, Physical count -> PC, PAR count -> PAR, Receipt delivery -> DEL. Emit all five rows when these five choices are supplied; a No value sets TasksEnabled to N and does not suppress the row. | REST Data Loader request. | |
| Task grouping level | Require the grouping rule from the canonical activity matrix. Resolve a supplied display value only when the matrix allows a CC or PC override. | Every emitted REST activityUsages row. | resolve_activity_task_grouping_level |
| Child relationship fields | Populate OrganizationName and derived ZoneName as the parent identity accepted by the published ParentUserKeys contract. Do not use ParentIdentifier or manually source ZoneId. | Every REST activityUsages row in the parent-root XLSX. | resolve_inventory_organization_by_name |
| Atomic parent and child preparation | For Create, include the new parent row and all activityUsages rows in one XLSX with RestAction POST. For Update, include the identified parent and all activityUsages rows in one XLSX with RestAction PATCH. | REST default-zone route is selected. | resolve_default_zone_by_organization_id |
| Child-row completeness | Block Data Loader handoff when a REST request that supplies the five UI activity choices does not produce exactly five activityUsages rows, or when a child row omits ActivityTypeCode, TasksEnabled, TaskGroupingLevel, RestAction, OrganizationName, or ZoneName. | Before REST Data Loader handoff. | |
| Update value preservation | Read the existing default-zone activity usages and overlay only the fields the user requests to change. Preserve the current value for each unspecified activity setting, then emit all five rows. Do not add ZoneId or ZoneActivityUsageId to the XLSX. | REST Update. | resolve_default_zone_by_organization_id |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV_TASK_CONFIG.CLASSIFY_IMPORT_ROUTE | step | 5 | validate_input | rest->INV_TASK_CONFIG.VALIDATE_CONDITIONAL_ATTRIBUTES;fsm->INV_TASK_CONFIG.VALIDATE_FSM_ARCHIVE;blocked->INV_TASK_CONFIG.RETURN_ISSUES | none | stop | Every request. Use core.data-loader source classification; REST is the task manifest default and FSM applies only to an explicitly selected FSM archive containing `ASM_SETUP_CSV_METADATA.xml`. |
| INV_TASK_CONFIG.VALIDATE_CONDITIONAL_ATTRIBUTES | step | 10 | validate_input | valid->INV_TASK_CONFIG.RESOLVE_INVENTORY_ORGANIZATION;blocked->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.CLASSIFY_IMPORT_ROUTE | stop | Classified REST Data Loader request containing activityUsages. |
| INV_TASK_CONFIG.VALIDATE_FSM_ARCHIVE | step | 11 | validate_input | validated->INV_TASK_CONFIG.CHECK_FSM_READINESS;blocked->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.CLASSIFY_IMPORT_ROUTE | stop | Classified FSM archive. Validate the native six-column task contract and exact Yes/No values; do not apply REST rules. |
