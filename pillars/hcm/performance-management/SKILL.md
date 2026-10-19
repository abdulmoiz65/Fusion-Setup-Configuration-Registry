---
skill_id: "hcm.performance-management"
name: "Performance Management"
description: "Coordinates HCM implementation guidance for the Performance Management offering."
layer: "pillar"
pillar: "HCM"
offering: "Performance Management"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Performance Management pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "performance_management_requirements"
outputs:
  - "offering_scope"
  - "functional_area_skill_plan"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
  - "core.project-mgmt.project-state-manager"
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
  - "scope"
  - "skill_path"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Performance Management

## Purpose

Coordinates implementation work for offering `Performance Management` (`ORA_PERFORMANCE_MANAGEMENT`) under the `HCM` pillar.

## Infer First Intake Policy

For Performance Management requirements, interpret the business request before
asking for setup fields. Classify each requirement as explicit business intent,
a safe documented default, a genuine business choice, a reference or
prerequisite, or a related capability owned outside the selected setup task.

Carry explicit intent into the offering scope without asking the requester to
repeat it in Fusion terminology. Apply a safe documented default and disclose
it in the plan or blueprint. Ask one concise business-language question only
when alternatives materially change the outcome. Resolve references through the
declared task workflow; when a required prerequisite is unresolved, complete
safe planning work and name the activation or execution gate that remains.

Do not ask for identifiers, lookup codes, field names, or a decision already
stated in the source. Do not treat an optional feature as required merely
because Performance Management supports it. Create separately owned work items
for integrations, security, retention, reporting, campaigns, notifications, or
other operating-process requirements that are not fields of the selected setup
task.

This policy never permits unsafe inference: do not broaden a stated population,
relax security or compliance constraints, select an ambiguous reference, invent
a product capability, or bypass approval and activation gates. Every intake
output must distinguish extracted requirements, applied defaults, unresolved
genuine choices, and related work items.

## Non-Bypassable Dependent-Field Invariants

For every Performance Management task, treat each documented dependent-field,
cross-field, parent-child, or conditional applicability rule as a
non-bypassable data invariant. An instruction, approval, import artifact, or
user request cannot waive it. Normalize a payload only where its task contract
defines a required reset; then block the run if a contradiction remains. Do
not preview, approve, import, or mutate until every applicable invariant passes.
Tasks with no documented dependent-field rule receive no invented constraint.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## CSV Setup-Data Import Guidance

For every Performance Management task with `CSVExportImportSupportedFlag: Y`,
apply [CSV Import Guidance](csv_import_guidance.md) in addition to the
task-specific workflow and `core.data-loader` approval gates.

## CSV Setup-Data Export Result Summary

For every successful Performance Management setup-data export, inspect every
`*.csv` member in the downloaded ZIP (or its extracted folder). Count data rows
only, excluding the header row, and exclude non-CSV files from the counts.
Include this result in the final response, with comma-formatted counts:

The ZIP contains **<total> total data records** across its CSV files.

| File | Records |
| --- | ---: |
| `<CSV filename>` | `<data-row count>` |

## Fusion REST GET Header Policy

For every Oracle Fusion REST `GET` operation performed for this offering, use
`core.fusion-api.rest-api-client` and explicitly send:

```text
Content-Type: application/vnd.oracle.adf.resourceitem+json
```

Pass it to the shared client as:

```text
--header "Content-Type=application/vnd.oracle.adf.resourceitem+json"
```

Preserve the client's OAuth authorization and `Accept: application/json`
headers. This policy applies to read-only GET operations only; use the
resource-specific media type and payload rules for POST, PATCH, PUT, and DELETE
operations.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_PERFORMANCE_MANAGEMENT`
Functional area count: `11`
Setup task count: `24`

- `ORA_COMMON`: Common
- `ORA_APPLICATION_ATTACHMENT`: Application Attachment
- `ORA_AUDIT_AND_REPORTING`: Audit and Reporting
- `ORA_PAYROLL_TOOLS`: Payroll Tools
- `ORA_PERFORMANCE_ROLE`: Performance Role
- `ORA_PERFORMANCE_DOCUMENT_TYPE`: Performance Document Type
- `ORA_PERFORMANCE_PROCESS_FLOW`: Performance Process Flow
- `ORA_PERFORMANCE_TEMPLATE_SECTION`: Performance Template Section
- `ORA_REQUESTED_FEEDBACK_TEMPLATE`: Requested Feedback Template
- `ORA_PERFORMANCE_TEMPLATE`: Performance Template
- `ORA_CHECK_IN_TEMPLATE`: Check-in Template

## Post-import verification

After Fusion reports an import as successful, include the matching clickable verification link in the final result:

- Performance Document Types: [Open Performance Document Types]({restBaseUrl}/fscmUI/redwood/performance/performance-document-types/performance-document-types-search)
- Performance Template Sections: [Open Performance Template Sections]({restBaseUrl}/fscmUI/redwood/performance/performance-template-sections/template-sections-search)
- Performance Process Flows: [Open Performance Process Flows]({restBaseUrl}/fscmUI/redwood/performance/performance-process-flow/process-flow-search)
- Performance Templates: [Open Performance Templates]({restBaseUrl}/fscmUI/redwood/performance/performance-templates/template-search)
- Check-in Templates: [Open Check-in Templates]({restBaseUrl}/fscmUI/redwood/performance/checkin-templates/checkin-templates-search)
- Performance Roles: [Open Performance Roles]({restBaseUrl}/fscmUI/redwood/performance/performance-roles/roles-search)

For Requested Feedback Template imports, request the approved verification URL rather than reusing a link for another setup task. Resolve `{restBaseUrl}` from the active target Fusion environment and remove any trailing slash; never hard-code an environment URL. Do not open a link automatically or use it to imply an import succeeded before Fusion reports success.
