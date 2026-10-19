---
task_code: "FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS"
task_name: "Manage Service Provider Relationships"
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

# Manage Service Provider Relationships

## Setup Task Metadata

- Task name: `Manage Service Provider Relationships`
- Task code: `FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS`
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
- Setup task name: `Manage Service Provider Relationships`
- Setup task code: `FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS`


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Service Provider Relationships` under `Organization Structures`.

## Mandatory Import Gates

1. Resolve client and provider BUs exactly, and resolve both an upstream and a downstream function. A single undirected function is insufficient.
2. Read `AnyProvidersFlag` from the fresh task contract. When it is `N`, require the named provider BU to have the downstream assignment in fresh function-assignment evidence. When it is `Y`, do not require a named-provider equality match; use fresh target evidence for BUs eligible to perform the downstream function. Do not impose a client-upstream assignment requirement without target evidence.
3. Require exact approved directed-pair evidence as the compatibility gate. For SPR_FSM_ADD_RELATIONSHIP_V1, the controlled related-function seed mapping qualifies the tested pair without a live table query solely to restate it; other requested behavior needs its own evidence. Record its `OUTSOURCING_POLICY_CODE`, but do not infer the meaning of a policy code: obtain authoritative policy semantics when the proposed behavior depends on it. Select the qualified first-submission assurance or supported current four-key relationship comparison for the operation. Known supported identical relationships are a no-op; conflicting/ambiguous state or an uncertain prior write blocks a new submission.
4. Derive function IDs from current approved mappings only; do not reuse IDs from another environment.

Code Search confirms that `FUN_BU_SERVICE_PROVIDERS` has the four-column relationship key and individual foreign keys for upstream and downstream functions; it does not have a composite foreign key to `FUN_RELATED_FUNCTIONS`. The application code recognizes `AnyProvidersFlag` values `Y` and `N`; `N` requires provider/downstream equality, while the `Y` path bypasses that equality. The flag is non-null in the entity model. Do not supply any other value or manufacture a provider value for the `Y` path.

## Shared-Services Design Guidance

Use service-provider relationships to make centralized processing explicit while preserving appropriate BU-level transaction ownership. This is generally preferable to creating extra BUs solely to represent a shared-services team.

- Requisitioning service providers can process requisitions and negotiate supplier terms for client BUs.
- Payables Payments service providers can make payments on behalf of client BUs; confirm the applicable shared-ledger and payment-on-behalf-of operating model.
- Customer Payments service providers can process customer payments for client BUs that perform Billing and Revenue Management.
- For other centralized activity, design and test the data-role and security context that grants shared-services users access to the required BUs. Service-provider relationships do not replace least-privilege role design or segregation-of-duties controls.

## Validation Checkpoints

Document provider and client BU ownership, supported functions, approval and exception handling, ledger/legal-entity constraints, and security roles. Test a provider user's permitted client-BU transactions and verify that access is not granted to unrelated BUs.
  <!-- -->

## Chronological Execution

Finish and verify creation of both BUs, then complete any required provider/downstream function assignment before preparing this task. Do not create another BU because a role prerequisite is missing. Re-resolve parties on a later prompt; do not trust historical identities, initial effective dates or unverified earlier success.

Use a fresh matching template, then select SPR_FSM_ADD_RELATIONSHIP_V1 in ora_bulk_intake.md for its eligible first active named-provider link between two minimally created current-workflow BUs. Its independent accepted payload omits unprovided technical party keys/dates and uses exact names, retained approved parent business values, controlled pair and fresh role evidence. No missing-field/read waiver or populated export is required. Do not transfer the BU creation contract to this task or extend the qualified relationship profile to Y handling, arbitrary existing parties or maintenance. Outside eligibility, report the exact required evidence gap rather than manufacture values.


## Processing and Independent Verification

The qualified profile uses reconciled current-workflow first-submission evidence, not an assertion that a failed ServiceProviderFinder proved absence. That finder returns BU LOV data and may require target context unavailable through its published variables; use only target-supported parameters and never invent a BusinessUnitId finder argument. A read failure remains a documented read failure.

Review the matching detailed FSM log for the relationship and both parent rows, then re-read party identities/foundations, module membership and visible set assignments. If no permitted source exposes the saved four-key relationship, report log-confirmed processing with that explicit independent-verification limit. Do not claim the payload/log proves every saved attribute or repeat the import to obtain a read result. Existing-state equality, prior/uncertain submissions and explicit strict verification remain outside first-link eligibility.


## Verification and Outcome Reporting Policy

Apply the parent's endpoint-only policy to this task and all delegates. No Fusion UI, screenshots, browser inspection or user-assisted screen verification is allowed for duplicate checks, validation or saved results. Use declared core-client endpoints and permitted framework evidence; unavailable facts remain explicitly unverified. Only core.auth may hand login to the user, without agent UI inspection.

Before quoting results, apply [mandatory log review](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting). Review matching FSM logs for submitted imports, or actual client/evaluated-rule evidence for reads, native actions and unsubmitted validation. Processing success and independently verified saved values are separate outcomes.
