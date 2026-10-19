# Inventory Task Configurations Dependency Readiness

When FSM Import is explicitly selected, core Data Loader classifies the final archive by its `ASM_SETUP_CSV_METADATA.xml` marker. FSM uses one flattened `InvZoneTaskConfigurationVO` row and does not use this REST parent-child dependency chain. A classified FSM source is ready when its metadata is preserved and it contains exactly the six exported CSV columns with `Yes` or `No` flags.

## FSM Readiness

| Dependency | What Must Happen |
|---|---|
| FSM template source | Use a reusable verified empty template-only export for `ORA_INVENTORY_TASK_CONFIGURATIONS`, or obtain a replacement through the approved task-level export workflow. Do not use a current-data export, manufacture metadata XML, or package a loose CSV as FSM. |
| Template provenance and integrity | Before reuse, verify the recorded task code, target environment, compatible Fusion release, ZIP fingerprint, exactly one metadata marker, native CSV member/header, and absence of exported configuration rows. |
| Classified source identity | Preserve `ASM_SETUP_CSV_METADATA.xml` and the native `ORA_INVENTORY_TASK_CONFIGURATION.csv`. Do not treat a loose CSV, a REST request, or `CSVExportImportSupportedFlag` alone as FSM evidence. |
| Native parameter contract | Provide exactly `OrganizationName`, `ParCount`, `CycleCount`, `PhysicalInventory`, `PickConfirm`, and `ReceiptDelivery`, with the exact strings `Yes` or `No` for the five task-generation values. |
| Immutable package preparation | Copy the verified template and add only approved rows to the native CSV. Preserve metadata XML, CSV header, encoding, member names, and ZIP structure; restart validation and approval when the template or rows change. |
| REST separation | Do not run REST BO registration, organization/default-zone lookups, ZoneName derivation, activityUsages preparation, grouping-level defaults, RestAction, or ZoneId processing. |
| Core handoff | Hand the unchanged, classified FSM ZIP to `core.data-loader`, which validates the final immutable artifact and owns the single approval and FSM import initiation. |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Default-zone route selection | Resolve zero or one default zone for the selected OrganizationId. Create proceeds only with zero; Update proceeds only with one. REST Data Loader only. |
| 2 | Parent and child artifact | Prepare one parent-root XLSX containing the parent row and its activityUsages rows. |
| 3 | Child relationship contract | Use the published ParentUserKeys OrganizationName,ZoneName contract; ZoneId is resolved internally by the BO. |
| 4 | Activity usage preparation | Translate all five UI sections into `PICK`, `CC`, `PC`, `PAR`, and `DEL` child rows. Populate `TasksEnabled`, the canonical grouping level, the operation-specific RestAction (`POST` for Create; `PATCH` for Update), child OrganizationName, and derived ZoneName; do not source ZoneId. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| default_zone_route | Default-zone existence route | Yes | REST Data Loader request containing activityUsages. | Ready when the read-only resolver returns exactly zero or one default-zone row and matches the requested operation: zero for Create, one for Update. | inventoryZoneTaskConfigurations filtered by OrganizationId and DefaultZone Y. | resolve_default_zone_by_organization_id | Redwood creates only when the default zone is absent and upserts the existing default-zone configuration when it is present. | Do not select the first of multiple rows. Do not use the returned ZoneId as child input. | Route decision; current activity values are retained only for Update overlay. |
| inventory_zone_task_configuration | Parent inventory zone task configuration and activity usages | Yes | REST activityUsages request. | Ready when the XLSX contains exactly the requested `PICK`, `CC`, `PC`, `PAR`, and `DEL` child rows, each with OrganizationName and derived ZoneName accepted by ParentUserKeys. | Live activityUsages template, published BO registration metadata, canonical activity matrix, and default-zone resolver result. | resolve_inventory_organization_by_name | The BO resolves its internal parent ZoneId from child ParentUserKeys within the one parent-root artifact. | Prepare one immutable XLSX. A No setting becomes TasksEnabled N; it does not omit the child. Apply the canonical activity matrix; do not manually source child ZoneId. | Parent: OrganizationName, ZoneName, Description, StartDate, StatusCode. Child: OrganizationName, ZoneName, ActivityTypeCode, TasksEnabled, TaskGroupingLevel, RestAction. |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| BLOCKED | Default-zone lookup fails or is ambiguous, the requested operation does not match default-zone existence, ParentUserKeys support is absent, a child row lacks required values, or the five supplied UI choices do not yield five child rows. | No |
| READY | The parent-root XLSX includes the parent row and all five mapped child rows, each carrying the required relationship and activity values. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV_TASK_CONFIG.CHECK_PARENT_CHILD_READINESS | step | 40 | resolve_dependency | ready->INV_TASK_CONFIG.DATALOADER_HANDOFF;blocked->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.APPLY_ACTIVITY_DEFAULTS | stop | REST Data Loader request containing activityUsages. |
| INV_TASK_CONFIG.CHECK_FSM_READINESS | step | 41 | resolve_dependency | ready->INV_TASK_CONFIG.FSM_DATALOADER_HANDOFF;blocked->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.VALIDATE_FSM_ARCHIVE | stop | Classified FSM archive passed native-contract validation and core package validation. |
