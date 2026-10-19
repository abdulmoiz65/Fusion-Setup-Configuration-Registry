---
task_code: "FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT"
task_name: "Manage Business Unit Set Assignment"
parent_skill_id: "erp.financials.organization-structures"
pillar: "ERP"
offering: "Financials"
functional_area: "Organization Structures"
functional_area_code: "ORA_ASK_ORGANIZATION_STRUCTURE"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Business Unit Set Assignment

## Setup Task Metadata

- Task name: `Manage Business Unit Set Assignment`
- Task code: `FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Acquire a same-task template/spec with `shared.setup-export.task-level-export`. Apply the parent no-full-data-export policy; current values come from declared GETs and verified current-workflow evidence. A populated export is allowed only through a named, authorized, genuinely scoped route; never request, consume or locally filter a full export as a substitute.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Organization Structures`
- Setup task name: `Manage Business Unit Set Assignment`
- Setup task code: `FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT`


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Business Unit Set Assignment` under `Organization Structures`.

## Implementation Evidence

Code Search identifies `FND_SETID_ASSIGNMENTS` as the persistence table for BU set assignments. The BU-facing view joins it to `FND_SETID_SETS_VL`, `FND_SETID_REFERENCE_GROUPS_VL`, and `HR_ORGANIZATION_V`, with `DETERMINANT_TYPE = 'BU'`, `DETERMINANT_VALUE = ORGANIZATION_ID`, and `CLASSIFICATION_CODE = 'FUN_BUSINESS_UNIT'`. Use this only for validation reasoning; use the fresh task template and the selected BUSA_FSM_ADD_OVERRIDE_V1 or BUSA_FSM_PARENT_KEY_V1 mapping as the import contract.

## Reference Data Set Design Guidance

Use set assignments to standardize reference data across BUs where the business process is common, and create BU-specific sets only for genuine policy, regulatory, or operational differences. Shared data reduces duplicated setup and configuration drift; BU-specific data provides control and local flexibility but increases maintenance, testing, and change-control effort.

- Identify each reference-data object's intended sharing scope, owner, approver, and change process before assigning a set to a BU.
- Validate that shared sets do not override a required country, tax, privacy, or BU-level policy boundary.
- Where local variation is required, record the rationale and the downstream functions, integrations, reports, and users affected by the BU-specific set.
- Reassess set assignments during BU changes; changing a shared-data boundary can alter defaults, transactions, and reporting behavior.

## Validation Checkpoints

For every BU-to-set assignment, verify the expected values and defaults in the enabled business functions, confirm least-privilege maintenance access, and test that a set change has no unintended effect on other assigned BUs.
  <!-- -->

## Saved BU and Assignment Evidence

Verify that the BU already exists or finish its creation first. Resolve only the requested reference groups and sets; do not generate all controlled group rows for a single override. Use the current task template to obtain the actual assignment CSV filename, headers and metadata. Verify saved group assignments through setIdAssignmentsBusinessUnit, not setIdAssignmentsSet.

Do not equate the inherited default set with a verified explicit override. Select BUSA_FSM_ADD_OVERRIDE_V1 in ora_bulk_intake.md first for an eligible current-workflow delta. It accepts exact parent Name and retained approved business values with blank unprovided OrganizationCode/effective dates; no missing-field waiver or populated export is required. Otherwise use BUSA_FSM_PARENT_KEY_V1 with exact permitted current parent keys/dates. Preserve unrequested BU/group values; never add a classification suffix or substitute a REST label. An existing assignment export is not required to prove this packaged mapping. A missing value still required outside the additive profile is a named permitted-source gap, not a reason to recreate the BU or request a full export.

Review the matching detailed FSM log before reporting processing success/failure, then verify the requested set and preservation of other visible explicit assignments through complete BU-determinant reads. Retained DefaultSetCode is current-workflow intent, not an independently read saved default set; disclose unexposed default/date certification limits. A same-set current-read no-op does not need an import.


## Verification and Outcome Reporting Policy

Apply the parent's endpoint-only policy to this task and all delegates. No Fusion UI, screenshots, browser inspection or user-assisted screen verification is allowed for duplicate checks, validation or saved results. Use declared core-client endpoints and permitted framework evidence; unavailable facts remain explicitly unverified. Only core.auth may hand login to the user, without agent UI inspection.

Before quoting results, apply [mandatory log review](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting). Review matching FSM logs for submitted imports, or actual client/evaluated-rule evidence for reads, native actions and unsubmitted validation. Processing success and independently verified saved values are separate outcomes.
