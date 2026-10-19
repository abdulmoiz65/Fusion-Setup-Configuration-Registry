# Advanced Inventory Parameters Dependency Readiness

## Readiness Rules

The table below applies to the REST-backed route. FSM uses the separate readiness contract below; REST BO registration and DFF visibility are not prerequisites for an FSM archive.

| Dependency | Status | Evidence | Handling |
| --- | --- | --- | --- |
| Registered parent BO | Registration and hierarchy confirmed; live load metadata validation required | User-provided registration and Data Loader hierarchy evidence identify `advancedInventoryParameters`; this alone does not verify current template, attributes, or operation keys. | Let core.data-loader validate live parent metadata for the actual load before handoff. Report failures with the missing metadata item; do not equate registration with runtime readiness. |
| Parent-template DFF child section | Parent registration confirmed; live parent-template child-section visibility pending evidence | User-provided registration evidence identifies `InvAdvancedInvParamsDFF` as a child section of `advancedInventoryParameters`; the live parent template, attributes, binding, and sample packaging remain unverified. | For requests containing DFF data, let `core.data-loader` validate the parent template and its child section. Do not require separate child registration, a separate child sample, or a separate child invocation. |
| Target inventory organization | Required | User confirmed that a BO-level SQL query resolves internal `OrganizationId` from mandatory `OrganizationCode`. The query itself has not been independently inspected. | Require one unambiguous `OrganizationCode` before handoff; do not require a caller-supplied internal ID or duplicate the BO SQL. |
| Inventory Management setup | Required | The Advanced Inventory Management task mapping lists Inventory Management as a dependency. | Confirm prerequisite setup is available before handoff. |

## FSM Readiness

| Evidence | Current knowledge | Required handling |
| --- | --- | --- |
| CSV contract | Supplied exports show 73-column and 78-column schemas. User confirmed that the five additional fields listed in `SKILL.md` are newly added and patch-dependent across environments. | Preserve the native schema and retain all 78 fields as knowledge; do not infer obsolescence or require a fixed column count. |
| Target patch-dependent field availability | Optional for the five additional fields; use target-native FSM export/metadata to establish presence. | Include supplied values when supported; otherwise ignore/defer those fields for now and report skipped requested values. Their absence or unknown availability is not a patch-readiness blocker. Native package validation still applies. |
| Complete package and task identity | Unverified: only the supplied CSV header has been reviewed, not a complete FSM package. | Block an FSM load until core.data-loader validates the package and its task identity. |
| Supported operation and delete protection | Import-operation validation belongs to the shared workflow. | Reject explicit delete requests or known delete settings and honor shared validation failures. No task-specific operation marker or independent non-delete evidence gate is required. |
| Native field semantics | Accepted domains, blanks, requiredness by operation, defaults, lookup domains, and DFF context requirements remain unverified. | Resolve applicable requirements through FSM metadata/validation; do not invent local constraints. In particular, do not infer Supply Expected Days requiredness from Include Expected Supply. |
| Execution evidence | Shared Data Loader supports FSM; no successful task-specific import has been verified. | Retain this limitation in reporting. Prior success is not a prerequisite for a first load once all package-specific validation passes. |

FSM DFF data uses `AttributeCategory` and inline segment columns in the observed CSV. It does not require verification of the REST parent-template DFF child section.

### FSM Evidence Procedure

Verify package task identity using native metadata and authoritative task information. `ObjectShortName` extraction alone is not proof of task compatibility. Do not infer that the CSV basename, FSM object name, and `ORA_ADVANCED_INVENTORY_PARAMETERS` are identical.

Reject explicit delete intent or known delete settings. Delegate import-operation validation to the shared workflow; do not demand an unverified package marker, independent non-delete certificate, or invented preflight procedure. An `EXPORT` process label alone does not establish import behavior and must not independently block the task. Preserve concrete shared-loader or Fusion operation diagnostics and resolve them before proceeding.

Native field validation belongs to the shared loader/FSM. Require evidence only for checks needed by the task's approved rules; a historical list of unknown domains must not cause blanket local revalidation of every column.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ADV_INV_PARAMS.CHECK_READINESS | step | 20 | resolve_dependency | ready->ADV_INV_PARAMS.RESOLVE_REFERENCE_LOOKUPS;blocked->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.VALIDATE_PARENT_IDENTITY | stop | Parent identity passed local validation. |
| ADV_INV_PARAMS.CHECK_FSM_READINESS | step | 21 | resolve_dependency | ready->ADV_INV_PARAMS.FSM_DATALOADER_HANDOFF;blocked->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.VALIDATE_FSM_ARCHIVE | stop | FSM package validation passed; honor shared readiness results and reject explicit or known delete operations before handoff. |
