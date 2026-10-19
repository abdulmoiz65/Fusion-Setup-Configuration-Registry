---
task_code: "FUN_MANAGE_BUSINESS_UNIT"
task_name: "Manage Business Unit"
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

# Manage Business Unit

## Setup Task Metadata

- Task name: `Manage Business Unit`
- Task code: `FUN_MANAGE_BUSINESS_UNIT`
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
- Setup task name: `Manage Business Unit`
- Setup task code: `FUN_MANAGE_BUSINESS_UNIT`


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Business Unit` under `Organization Structures`.

## Mandatory Import Gates

1. Resolve an existing Default Reference Set to exactly one current set. If **Create New** is selected, require Set Code and Set Name, create the set through the native setIdSets route in ora_reference_lookups.md, and re-resolve it before preparing the BU row.
2. Before every create/import, perform an exact complete-page lookup by BU name. Zero matches classify New and require no existing parent export. For an existing candidate, compare every requested effective attribute with current saved-state evidence: Existing-Identical is a no-op; Existing-Different, Ambiguous or unverified comparable fields block a create/no-op claim.
3. Use the matching fresh target template metadata and headers for a new BU. Populate selected business fields and documented defaults; leave unprovided OrganizationCode and effective dates blank on this create path. Do not copy another BU or a historical run to fill technical fields. See ora_bulk_intake.md for the bounded create contract and stronger maintenance checks.

## Business Unit Design Checklist

Before creating a BU, document its durable operational purpose, accountable owner, transaction types, required business functions, and why a reporting hierarchy, chart-of-accounts segment, or role-based control cannot meet the need. Prefer fewer BUs where controls and policies can be managed without a separate transaction/configuration boundary; every additional BU increases setup, security administration, testing, supplier-site maintenance, and risk of configuration drift.

- Align the BU to one primary ledger. Confirm the legal-entity processing model and do not normally divide a single legal entity across multiple BUs.
- Confirm that country, tax, statutory, privacy, and data-residency requirements support the proposed boundary. Cross-country BUs require explicit compliance, security, defaulting, and end-to-end testing approval.
- Select a reference-data-set strategy that shares standard data and isolates only genuinely distinct policy data. Identify the owner and change-control process for each set.
- For employee-assignment BUs, assess Expenses, Projects, Time and Labor, and Requisitioning impacts. Avoid a cross-country employee-assignment BU when the finance model is country-specific; many detailed employee-assignment BUs can create expense-template, intercompany, and access-provisioning overhead.

## Validation Evidence

For each configured BU, retain the ledger, legal-entity relationship, location, reference-data set, enabled functions, manager/owner, security scope, rationale for separation, and exception approvals. Test the resulting ledger/defaulting behavior, transaction access, and required downstream flows before production use.
  <!-- -->

## Completion and Follow-On Work

After creation, use the FSM log and an exact current BU lookup to confirm the saved BU before invoking any requested function, set or provider assignment. A successful creation does not require all later tasks to be requested or completed. Later prompts reuse the resolved existing BU; they do not repeat its creation. Follow the parent skill's ordered workflow and each task's own evidence gates.


## Verification and Outcome Reporting Policy

Apply the parent's endpoint-only policy to this task and all delegates. No Fusion UI, screenshots, browser inspection or user-assisted screen verification is allowed for duplicate checks, validation or saved results. Use declared core-client endpoints and permitted framework evidence; unavailable facts remain explicitly unverified. Only core.auth may hand login to the user, without agent UI inspection.

Before quoting results, apply [mandatory log review](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting). Review matching FSM logs for submitted imports, or actual client/evaluated-rule evidence for reads, native actions and unsubmitted validation. Processing success and independently verified saved values are separate outcomes.
