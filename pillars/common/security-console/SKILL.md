---
skill_id: "common.security-console"
name: "Security Console"
description: "Routes Common-pillar Oracle Fusion Security Console, FSM security setup, user-security, role-provisioning, and data-security work to the appropriate focused skill."
layer: "pillar"
pillar: "Common"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "FSCR Security team"
version: "1.0.3"
inputs:
  - "implementation_objective"
  - "project_id"
  - "target_environment"
  - "requested_operation"
outputs:
  - "security-console-skill-routing-plan"
  - "diagnostics"
depends_on:
  - "common.security-console.user-security-common"
  - "common.security-console.manage-security-fsm-skill"
  - "common.security-console.manage-job-roles"
  - "common.security-console.manage-duties"
  - "common.security-console.manage-data-security-policies"
  - "common.security-console.manage-hcm-role-provisioning-rules"
  - "common.security-console.manage-hcm-ldap-user-account-options"
  - "common.security-console.bulk-user-role-provisioning"
uses_core: []
persists_project_state: false
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

# Security Console

Use this Common-pillar entry point for Oracle Fusion Security Console and
related Functional Setup Manager security work. It classifies the objective and
routes to the focused child skill; it does not call Fusion directly.

## Purpose

Provide a discoverable Common-pillar home for reusable Security Console skills
without changing the execution contracts owned by the child skills.

## Cross-Pillar Catalog Scope

This is a Common-pillar router used by every implementation pillar, not one
FSM setup task. It intentionally has no singular `task_code` or
`dataloader_import_mode`; focused child skills declare those fields only when
they map to one exact effective-catalog task.

## Local placement exception

The user-approved Common Security Console placement exception is recorded in
[the local exception reference](references/catalog-placement-exception.md).
It changes no central catalog or auditor rules; automated audits may still
report the placement mismatch.

## Child Skills

| Objective | Skill |
| --- | --- |
| Common manual user-security tasks and approved ESS handoffs | `common.security-console.user-security-common` |
| Security Console role-management planning or Manage Job Roles FSM routing | `common.security-console.manage-security-fsm-skill` |
| Create, update, delete or redesign custom job/abstract roles; export/import role setup | `common.security-console.manage-job-roles` |
| Create, update, delete or redesign custom duties; export/import duty setup | `common.security-console.manage-duties` |
| Create, update, delete or redesign data-security policies; export/import policy setup | `common.security-console.manage-data-security-policies` |
| Create, update, delete or redesign HCM role-provisioning rules | `common.security-console.manage-hcm-role-provisioning-rules` |
| Create, update, delete or redesign HCM LDAP account options | `common.security-console.manage-hcm-ldap-user-account-options` |
| Validated bulk User/UserRole HDL provisioning | `common.security-console.bulk-user-role-provisioning` |

## Template assistance

When users cannot identify or fill a template, accept their requirements and
route to the focused owner using [FSM input preparation](references/fsm-input-preparation.md).
The owner obtains/extracts its supported template and guides or prepares input.
Do not route a supported individual-object change to a manual-only classifier.

## Routing Rules

1. Route a request to exactly one focused child skill unless the selected child
   skill explicitly declares a dependency on another child skill.
2. Preserve each child skill's environment, validation, approval, and
   diagnostic gates. This routing skill grants no approval for a live action.
3. Record ambiguity as a routing diagnostic and request the business object or
   FSM task scope needed to choose the child skill.

## Preflight and Failure Handling

Before routing, confirm the implementation objective, requested operation, and
target environment when the selected child skill requires one. Do not infer an
approval, endpoint, task identity, or scope. If more than one child skill
could apply or a required routing input is absent, stop before delegation and
return a routing diagnostic with the missing input and recommended next action.

Do not persist or expose credentials, tokens, private keys, customer data, or
unredacted payloads in routing diagnostics. The selected child skill owns any
durable artifact, live-operation approval, retry, timeout, and recovery logic.
