---
skill_id: "erp.financials.organization-structures"
name: "Organization Structures Implementation Guidance"
description: "Provides ERP Financials implementation guidance for the Organization Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Organization Structures"
functional_area_code: "ORA_ASK_ORGANIZATION_STRUCTURE"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.8"
inputs:
  - "implementation_objective"
  - "project_context"
  - "organization_structures_scope"
  - "organization_structures_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.data-loader.task-hook"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/organization-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/organization-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/organization-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "FUN_MANAGE_BUSINESS_UNIT"
  - "FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION"
  - "FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT"
  - "FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Routes approved native reference-set creation through the core REST client."
  - "Routes approved BU and assignment imports through FSCR Data Loader."
  - "Reads declared references and persists stage evidence in the active project."
required_privileges: []
---

# Organization Structures Implementation Guidance

## Purpose

Provides ERP Financials implementation guidance for the Organization Structures functional area.

## When to Use

Use this functional-area skill after Financials scope is confirmed and the project needs organization structures setup planning, template acquisition, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Financials` (`XLE_FINANCIALS_JUR`)
- Functional area / Setup Object: `Organization Structures` (`ORA_ASK_ORGANIZATION_STRUCTURE`)

## Setup Tasks

1. [Manage Business Unit](manage-business-unit.md) (`FUN_MANAGE_BUSINESS_UNIT`)
2. [Assign Business Unit Business Function](assign-business-unit-business-function.md) (`FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION`)
3. [Manage Business Unit Set Assignment](manage-business-unit-set-assignment.md) (`FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT`)
4. [Manage Service Provider Relationships](manage-service-provider-relationships.md) (`FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS`)

## Inputs

- `implementation_objective`
- `project_context`
- `organization_structures_scope`
- `organization_structures_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For task inputs, lookup mechanics, defaults and dependency checks, read the task-scoped rows in [reference lookups](ora-resource/ora_reference_lookups.md), [input validation](ora-resource/ora_input_validation.md), [defaulting rules](ora-resource/ora_defaulting_rules.md), [dependency readiness](ora-resource/ora_dependency_readiness.md) and [bulk intake](ora-resource/ora_bulk_intake.md). Use a fresh same-task target template with its inspected metadata and headers for new-BU creation. Internal tables explain validation; they are not write endpoints or CSV layouts.

Create a new default reference set through the native `setIdSets` action declared in this BU guidance, then re-resolve it before BU import. Do not route this prerequisite to HCM Manage Reference Data Sets, add an HCM setup task to the Run Book, or invent a Data Loader discriminator for the native resource. Read-only HCM Sets, worker and location LOVs remain valid BU reference resolvers when applicable.

For a new BU, require a complete exact-name zero-match lookup, the resolved default set and the current template. No existing parent row or populated export is needed for that decision. For Manage Business Unit no-op/update decisions on existing BUs, compare all requested effective attributes using current evidence; unavailable fields are unknown, not identical. Do not apply this complete maintenance comparison to an eligible name-linked additive profile: BUF_FSM_ADD_FUNCTION_V1, BUSA_FSM_ADD_OVERRIDE_V1 or SPR_FSM_ADD_RELATIONSHIP_V1. Each has independent eligibility and evidence; no profile qualifies arbitrary parent updates. Resolve each supplied foundation identity exactly and, when both are present, verify the complete `legalEntitiesLOV` `LedgerFinder` association. Do not require an Assign Legal Entities export for this proof. A BU without financial functions may omit its ledger and legal entity. Financial-function assignment still requires the verified compatible foundation.

## Ordered BU Workflow

1. Collect only the requested business decisions: BU name, existing-set choice or new-set code/name, optional status, financial foundation, manager/location, and any requested later assignments. Select the active project, environment and canonical Run Book task context through the FSCR router. Enforce the no-full-data-export policy in ora_design_enforcement.md before any delegated acquisition. Do not infer a target from another run.
2. Perform the complete exact-name BU duplicate check before any prerequisite write; resolve an existing candidate through the no-op/update decision rather than creating a duplicate. Resolve the default set. If creation is requested, preview and approve the exact native set payload, create it once through the core REST client and re-query its exact code/name. This is a prerequisite action within BU guidance, not a separate HCM skill dependency.
3. Create the BU through template preparation, Data Loader preflight, Task Hook and the immutable approved FSM archive. Poll the recorded request and inspect its FSM log. Re-query the BU by exact name and retain its saved identity, active state and foundation before continuing.
4. Run only the requested assignments. Business functions and reference-group set overrides can follow the saved BU independently; complete any dependencies needed by the next stage. For financial functions, verify the stored BU foundation and ledger/LE association. Use each assignment task's current contract and present-day state. For an eligible additive function assignment, select BUF_FSM_ADD_FUNCTION_V1 in ora_bulk_intake.md before applying maintenance-only evidence requirements; do not demand unexposed generated keys, saved dates or ConfigurationStatus solely to prepare that path. For a current-workflow set override, independently select BUSA_FSM_ADD_OVERRIDE_V1 before imposing saved-key/date maintenance gates. Neither profile qualifies blind parent updates.
5. Create service-provider relationships after both parties exist and the required provider/downstream assignment and directed-pair evidence are verified. Select SPR_FSM_ADD_RELATIONSHIP_V1 for its qualified first active named-provider link; record bounded first-submission assurance and saved-row verification limits instead of demanding an unavailable relationship read or generated-key/date waiver for that eligible path. Reference-group overrides must precede dependent use when the requested process needs them; unrelated overrides are not mandatory for every relationship.
6. Report each stage separately. Before quoting success or failure for a submitted import, apply the [mandatory log-review gate](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting); status summaries alone are provisional. Initiated, in-progress, succeeded, failed, no-op and saved-state verified are distinct outcomes. A failed or uncertain prerequisite blocks its dependents while preserving earlier successes. Resume from the recorded request/state; do not recreate a successful BU or blindly repeat a POST.

A create-only request ends after BU verification. A later prompt to assign functions, sets or providers resolves the existing BU and invokes that task only. Keep task-local registry prerequisites within their own task; this parent workflow owns cross-task order. Use core OAuth for browser login only, core REST for declared lookups/native set creation, and FSCR export/validation/Data Loader for task imports. Never use the Fusion setup UI as a fallback.

## Evidence and Import Boundaries

A template proves package structure; it does not prove duplicates, saved configuration, role eligibility or membership. Record the source of every populated field: user decision, documented default, exact lookup, or current saved-state contract. Leave unsupported technical values blank on the tested new-BU path; do not invent flags, currency, dates, codes, IDs, filenames, release compatibility or endpoint behavior.

New-BU template imports have accepted omitted OrganizationCode and effective dates. Preserve explicit supplied values and validate them against the current target contract; do not promise that a requested date persisted when the read API cannot expose it. This finding does not automatically qualify dependent tasks. Each has its own independently tested profile in ora_bulk_intake.md: BUF_FSM_ADD_FUNCTION_V1 for additive functions, BUSA_FSM_ADD_OVERRIDE_V1 for group deltas, and SPR_FSM_ADD_RELATIONSHIP_V1 for its first named-provider link. Broader maintenance and preservation variants still require their own contract/evidence. Use declared current-state GETs and verified evidence from the active workflow. Full populated data exports are prohibited for every BU stage and its delegates, including preparation, duplicate checks, preservation and verification. A task template/spec export remains permitted. A genuinely scoped populated export is conditional on a named gap and its declared/authorized route; reject it if returned data exceeds the requested BU scope, and never treat locally filtering a full export as scoped acquisition. Select the operation-specific profile first. Only a field still required by that selected contract is a preparation gap; accepted technical omissions and unexposed saved-state certification are disclosed limits. Report genuine remaining gaps rather than requesting or consuming a full export.

## Business Unit Design Principles

Treat a Business Unit (BU) as a durable boundary for subledger transaction ownership, configuration, data access, and operational accountability—not as a direct copy of the organization chart. Prefer the smallest practical number of BUs. Create a separate BU only when a compliance or privacy boundary, enforceable BU-level policy difference, or ledger/tax operating-model constraint materially requires it; use reporting hierarchies, chart-of-accounts dimensions, and roles for reporting-only segmentation.

- Validate each proposed BU against its primary-ledger alignment, legal-entity processing model, required business functions, data-security boundary, reference-data strategy, and accountable owner.
- Do not use short-lived projects or frequently reorganized management structures as BU boundaries. Do not normally split one legal entity across multiple BUs; document and test any exception.
- Treat cross-country BUs as an exception requiring local compliance, tax, security, defaulting, and end-to-end process sign-off. A BU cannot span primary ledgers; a procurement BU is an exception to normal accounting-ledger behavior and must be associated with the finance BU in which purchase orders are created and matched to payables invoices.
- Design employee-assignment BUs with future Expenses, Projects, and Requisitioning effects in mind. Avoid cross-country employee-assignment BUs where finance is country-specific, and prefer broad alignment with Payables Invoicing; use hierarchies and shared reference data for HR reporting where possible.

## Required Design Evidence

Before configuration, record for each BU: business purpose and owner; reason a hierarchy or reporting dimension is insufficient; ledger and legal-entity relationship; business functions and dependencies; service-provider relationships; security/data-role scope; reference-data-set assignment; and the testing impact of the design. Reassess these decisions through change control because BU changes affect downstream access, approvals, defaults, configurations, and historical processing.

## Functional-Area Validation Checkpoints

- Confirm that each BU boundary is stable, necessary, and compatible with ledger, legal-entity, country, statutory, and tax requirements.
- Verify that the security model uses least-privilege roles and BU data access; BU segmentation alone does not satisfy segregation-of-duties requirements.
- Verify shared versus BU-specific reference data, including accountable owners and change control, to prevent configuration drift.
- Execute end-to-end tests for cross-BU payments, receipts, shared services, employee expenses, and any cross-country or multi-legal-entity exception in scope.
  <!-- -->

## Packaged Assignment Mapping

For an eligible current-workflow reference-group override, use `BUSA_FSM_ADD_OVERRIDE_V1` in ora_bulk_intake.md: exact parent Name, approved retained business decisions, requested group/set and independently tested blank technical keys/dates. Otherwise use `BUSA_FSM_PARENT_KEY_V1` with its exact required saved parent fields. Neither mapping requires an existing assignment CSV row. Use the current template for shape and the declared BU assignment GET for current/duplicate state. Resolve required values from permitted current sources; no profile fabricates generated OrganizationCode or saved dates. Do not demand a maintenance-only value or waiver after additive eligibility passes. Keep the default set and other assignments outside the requested delta, review process logs, then verify the saved override and preservation limits separately.

## Additive Function Assignment Selection

For a BU created and verified within the active workflow, use `BUF_FSM_ADD_FUNCTION_V1` in ora_bulk_intake.md when its eligibility checks pass. This independently tested path combines the fresh function template, explicit current-workflow business decisions, documented defaults and fresh declared lookups; no populated export, historical profile or missing-field waiver is needed. Missing generated keys, saved dates and unexposed ConfigurationStatus are not blanket preparation blockers for this eligible path. They remain verification limits, or actual blockers when a requested maintenance/preservation operation requires their exact values. Treat new assignment, existing identical state and supported maintenance as separate decisions. Never transfer the function omission contract to another task; the set and relationship profiles have their own independent acceptance evidence. Arbitrary BU maintenance remains outside these profiles.


## First Named-Provider Relationship Selection

For two BUs minimally created and verified in the active workflow, select `SPR_FSM_ADD_RELATIONSHIP_V1` in ora_bulk_intake.md before maintenance-only keys/dates or globally read duplicate requirements. The qualified route is the first active named-provider Billing and Revenue Management to Customer Payments link, with reviewed function receipts, fresh exact module/party checks, controlled pair evidence and reconciled workflow receipts. It requires no populated export or missing-field waiver. Current-workflow first submission is limited assurance, not independent proof of global absence. Prior/uncertain relationship writes, reused parties, known conflicting changes, unsupported pairs, Y handling and strict saved-field certification need their own evidence.

Report log-confirmed relationship processing separately from independently read saved configuration. A missing relationship reader is a verification limit for this qualified first submission; it is not permission to replay an uncertain write or claim a saved four-key row was read. Preserve stage receipts, exact payload fingerprints and visible assignment/function comparisons for later prompts. Repair local persistence errors by retrieving the existing recorded process, refresh authentication serially and never create a replacement object to resolve a later-stage error.


## Endpoint-Only Runtime Verification

This skill and every delegate must never access Fusion setup UI for discovery, duplicate checks, validation, review, configuration or result verification. Do not navigate task pages, inspect browser DOM/network state, operate controls, scrape grids, take screenshots or ask the user for UI evidence as a verification workaround. Screenshots and manually transcribed UI values are not authoritative runtime verification evidence.

Use only the declared FSCR core read clients and endpoint-backed status/diagnostic workflows for runtime checks. Complete exact-match lookup pagination and match the selected environment and identity. Inspect actual responses; failed, partial or unauthorized reads cannot prove absence, equality or success. Templates and approved framework artifacts retain their existing operation-specific source rules; packaged business rules explain accepted inputs but do not prove current saved state. Missing required endpoint facts are exact evidence gaps, not permission to invent an API, inspect UI or claim an unverified value. Qualified omission/first-submission profiles retain their stated limits and must not be represented as endpoint proof of global duplicate absence.

Authentication is the sole browser handoff: core.auth may open login for the user to complete. The agent must not inspect or operate the login, read credentials or navigate onward to task pages. Historical UI research retained as generic packaged knowledge never requires fresh runtime UI access.

Before quoting any result, apply the mandatory log-review and result-evidence rules in [error handling](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting). Submitted FSM imports require the actual matching process logs; lookups, native REST actions, validation and no-op results require their own actual response/diagnostic or evaluated-rule evidence. Do not invent an FSM log for an unsubmitted request or read-only action.
