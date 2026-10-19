---
skill_id: "erp.risk-and-security.activate-algorithms.activate-audit-policies"
name: "Activate Audit Policies"
description: "Guides an approval-gated, Core Audit Setup activation of the repository-managed Risk Management audit catalog."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Activate Algorithms"
functional_area_code: "ORA_GTG_ACTIVATE_ALGORITHMS"
task_code: "ORA_GTG_ACTIVATE_AUDIT_POLICIES"
task_name: "Activate Audit Policies"
parent_skill_id: "erp.risk-and-security.activate-algorithms"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "Risk Management implementation"
version: "0.3.0"
inputs:
  - "project_context"
  - "fusion_environment_context"
  - "execution_approval"
outputs:
  - "reviewed Core Audit Setup operation set"
  - "verified business-object audit status"
  - "runbook_lifecycle_result"
  - "manually persisted Core results and token-usage records"
depends_on: []
uses_core:
  - "core.fusion-api.audit-setup"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run_and_artifact"
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
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/activate-algorithms/activate-audit-policies/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
side_effects:
  - "Preview — read-only Fusion Audit inventory and object-status checks through core.fusion-api.audit-setup."
  - "Live — one approval-gated Core Audit Setup update-status operation per fixed catalog object, followed by object-status verification."
required_privileges:
  - "Fusion privileges appropriate to view and manage audit setup."
---

# Activate Audit Policies

## Purpose

Enable the fixed Risk Management audit catalog at
[`references/audits-to-enable.json`](references/audits-to-enable.json). This
catalog is the complete business scope: the skill accepts no user-supplied
audit objects or attributes and does not derive them from algorithms, UI labels,
or preceding workflows.

## Consultant-facing behavior

Follow the offering [Consultant Interaction Contract](../../references/consultant-interaction-contract.md).
Before asking for approval, present a compact Markdown table with **Business
area**, **Audit area**, **Current result**, and **Proposed result**. Derive each
consultant row by `userFacingAuditGroup` when present, otherwise by
`businessLabel`. Use the catalog's `businessArea` and `businessLabel`; do not
show business-object names or individual audit fields to the consultant.

The fixed projection contains exactly these six workbook-defined audit areas:

| Business area | Audit area |
| --- | --- |
| Supplier Model | Audit - Supplier Bank Accounts |
| Supplier Model | Audit - Supplier Payment Methods |
| General Ledger | Audit - Accounting Period Status |
| Oracle Middleware Extensions for Applications | Audit - Key Flexfield Cross Validation Rule |
| Compensation | Audit - Salary |
| Global Payroll | Audit - Personal Payment Method |

The Key Flexfield group is one audit area in the consultant view, even though
it has several underlying setup entries. Its result is enabled only when every
internal member is enabled and verified.

Ask plainly: **"Do you approve enabling the recommended audit coverage in
[environment]?"** The workflow records the exact internal operation plan after
that approval. It never asks a consultant to inspect or approve the plan,
field list, command, JSON, or diagnostic files.

## Usage

Use this skill when planning, sequencing, or validating the **Activate Audit
Policies** setup task under **Activate Algorithms**.

## Core Delegation Boundary

Use only `core.fusion-api.audit-setup` for Fusion authentication, REST
transport, token refresh, and Audit Setup response handling. This skill has no
local executable runner. Use the Core skill's currently documented
`get-setup`, `check-status`, and `update-status` operations; Core alone owns
its executable entry point, option syntax, authentication behavior, and
transport implementation. This skill supplies the fixed catalog scope, saves
Core output, and follows the approval gate below. Do not add a direct REST
client, OAuth handling, or a pillar-local retry mechanism.

## Execution

Before beginning any Core preview call, validate the fixed catalog projection
and construct the internal eight-row operation plan from that catalog. The
plan must contain each catalog row exactly once, an enabled object state, and
one enabled field entry for every configured attribute. A row without an
`attributeList` has no field entry. A local validation failure is a
preparation issue: stop before Fusion access and correct the catalog conversion.

Validate the consultant projection locally before any Fusion call:

```text
jq -e 'length == 8 and ([.[] | {area: .businessArea, audit: .businessLabel, group: (.userFacingAuditGroup // .businessLabel)}] | group_by(.group) | map({area: .[0].area, audit: .[0].audit}) | sort_by(.audit)) == [{area:"General Ledger",audit:"Audit - Accounting Period Status"},{area:"Oracle Middleware Extensions for Applications",audit:"Audit - Key Flexfield Cross Validation Rule"},{area:"Global Payroll",audit:"Audit - Personal Payment Method"},{area:"Compensation",audit:"Audit - Salary"},{area:"Supplier Model",audit:"Audit - Supplier Bank Accounts"},{area:"Supplier Model",audit:"Audit - Supplier Payment Methods"}]' references/audits-to-enable.json
```

This check must return `true`; it validates display grouping only and does not
replace the eight-row operation-plan validation above.

Run a read-only preview first, using one selected Core properties file for the
entire run. The environment reported in every Core result is the target
environment; do not proceed if it differs from the environment being reviewed.

Persist every Core result under:

```text
project/<project>/artifacts/pillars/erp/risk-and-security/activate-algorithms/activate-audit-policies/current/
```

When evaluating or presenting a `userFacingAuditGroup`, evaluate every member
row. Show the group as enabled only when every member is enabled and verified.
If any member is unavailable, disabled, or fails verification, show one
plain-language group exception and do not represent the audit area as complete.
The internal operation plan and execution still retain and process every
catalog row separately.

### Full-preview completion barrier

The catalog has eight internal rows and six consultant rows. Complete every
required `get-setup` inventory and all eight `check-status` operations before
showing the six-row consultant table. A returned Core request plan, a single
application inventory, or a single status result is an internal continuation
condition, never a final consultant response. Execute the next declared
read-only batch and re-evaluate until the complete six-row table or a genuine
business-facing exception is available.

Before live execution, validate the internal operation plan against the fixed
catalog. It must prove that every catalog row appears exactly once with an
enabled object state and that every configured `attributeList` entry appears
exactly once as an enabled Core field argument (`ATTRIBUTE=true`). A row without
`attributeList` has no field argument. Complete this cross-check before any
Core update-status operation is submitted. A validation failure blocks the
business approval and must be presented as a plain-language preparation issue.

Perform the following conversion from each validated row in
[`references/audits-to-enable.json`](references/audits-to-enable.json):

1. Deduplicate `application` values and run Core `get-setup` once for each
   application except `Ledger`. Require an exact business object, parent
   binding, and every configured attribute in the saved inventory result.
2. For every catalog row, run Core `check-status` with its exact
   `businessObject` and `parentBusinessObject`, saving the result under the
   project artifact directory.
3. Prepare one Core `update-status` operation per catalog row. Supply the
   exact `businessObject`, `parentBusinessObject`, an enabled object state, and
   every `attributeList` entry as enabled. A row without `attributeList` has
   no attribute-state input.

Review the exact target environment and the complete ordered Core operation set
before live execution. Record the explicit approval and the operation set under
the project artifact directory. The approval must acknowledge that Core handles
a rejected cached token according to its own documented behavior. Execute one
Core `update-status` operation per catalog row, in catalog order. If any
operation fails, stop; do not submit the remaining operations or manually retry
the failed operation without a new approval.

After every update succeeds, run Core `check-status` again for every catalog
row and require an enabled object state. Save every Core result and record the
token-usage entry and skill-run record manually under the project workspace.

The Ledger object is not excluded from the catalog, status checks, update
operations, or post-write verification; only its `get-setup` inventory preflight
is skipped. Do not invoke `get-setup` for `Ledger`: that endpoint does not
return for the application. The fixed catalog is the approved source for its
object, parent, and attributes.

An `ON` object status does not expose the current enabled-attribute selection.
Therefore, even when every object is already `ON`, the approved Core operation is
still submitted to ensure the fixed attribute list is requested. A successful
update is evidence only that those attributes were submitted; it is not an
independent read-back of attribute state.

## Approval and Failure Handling

- The approved Core operation set binds the fixed catalog conversion and the target
  environment reported by Core. Any changed catalog row, properties file, or
  operation requires a new review and approval.
- Core handles a rejected cached token according to its documented behavior.
  The operator must not manually rerun a failed live operation without a new
  approval.
- A Core operation that exits nonzero requires a redacted failure diagnostic
  beside the intended Core result. Include the stage, affected application or
  business object, verified target environment, failure classification, safe
  message summary, and recommended next action. Never persist token-cache
  contents, credentials, or a raw sensitive error payload. Stop the run and
  preserve completed Core result files.
- A missing object, parent binding, or configured attribute is a
  `catalog_or_metadata_mismatch` and blocks before mutation.
- Any post-write state other than `ON` is a verification failure. Save the Core
  result and request a new preview and approval before another write.

## Durable Outputs

Save Core preview and live results, the approved Core operation set, and any failure
diagnostic under:

```text
project/{project_id}/artifacts/pillars/erp/risk-and-security/activate-algorithms/activate-audit-policies/current/
```

Each assisted run also records a skill-run entry under
`project/{project_id}/state/runs/` and appends the project token-usage log.
Artifacts must not contain token-cache or credential contents.

Return `completed_verified` only after every fixed catalog row is verified
enabled. An explicit consultant deferral records outstanding audit coverage and
returns `deferred`; a catalog, Core, or verification failure returns `blocked`.
