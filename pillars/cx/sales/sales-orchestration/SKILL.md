---
skill_id: "cx.sales.sales-orchestration"
name: "Sales Orchestration Question Routing and Implementation Guidance"
description: "Answers and routes source-backed questions about the CX Sales Orchestration functional area and its Sales Motions, Sales Plays and Content, Data Capture Rules, and Pre-requisites tasks. Use for functional-area concepts, first-time readiness validation, task comparisons, setup sequencing, dependencies, security, object metadata, lifecycle, API capabilities, troubleshooting, import/export or mutation support, help sources, and implementation planning; classify task-level requests before routing them to a nested skill and never use the parent to bypass a child skill's execution boundary."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Orchestration"
functional_area_code: "CUSTOM_SALES_ORCHESTRATION"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.5.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "sales_orchestration_scope"
  - "sales_orchestration_requirements"
  - "sales_orchestration_question"
  - "requested_answer_mode"
outputs:
  - "question_classification"
  - "sourced_answer"
  - "operation_support_status"
  - "source_gap"
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-orchestration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-orchestration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-orchestration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_SALES_MOTIONS"
  - "CUSTOM_SALES_PLAYS_AND_CONTENT"
  - "CUSTOM_DATA_CAPTURE_RULES"
  - "CUSTOM_PRE_REQUISITES"
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

# Sales Orchestration Question Routing and Implementation Guidance

## Purpose

Answer and route source-backed questions about the CX Sales Orchestration
functional area, and provide functional-area implementation guidance without
bypassing the nested task skills' execution boundaries.

## When to Use

Use this functional-area skill for a Sales Orchestration overview, a comparison
or dependency spanning tasks, task selection, setup sequencing, support-boundary
questions, or functional-area implementation planning. Route a question owned
by one task to that task's nested skill.

## General Question Router

Read `references/sales-orchestration-question-routing.md` before answering a
general, ambiguous, cross-task, support, or help-source question.

1. Classify the request by subject and question class before loading API or
   authentication resources.
2. For a functional-area definition, business-value, capability, or trust and
   security question, read `references/sales-orchestration-overview.md`.
   For a question such as "What is Sales Orchestration?", give the complete
   agentic seller-experience definition and its seller outcomes and capabilities;
   do not reduce the answer to Sales Motions, Sales Plays, and Data Capture.
3. Select `EXPLAIN`, `READ`, `CLARIFY`, `ROUTE`, `GAP`, or `REFUSE` as the
   answer mode.
4. Route single-task questions to the owning nested skill.
5. For a multi-task question, obtain a source-backed result from each relevant
   task skill and synthesize only the supported facts.
6. Return `SOURCE_GAP` for behavior that the approved task sources do not
   establish. Identify the exact missing Oracle source or SME decision; do not
   invent a product rule.
7. Do not authenticate, call Fusion, refresh OAuth, or create a project artifact
   for an explanation-only question.

## Task Routing

| Subject | Nested skill |
|---|---|
| Sales Motion, objective, or high-value activity | `cx.sales.sales-orchestration.sales-motions` |
| Sales Play, content bundle or packet, content artifact, or Sales Play Content Intelligence | `cx.sales.sales-orchestration.sales-plays-and-content` |
| Data Capture Rule or rule attribute | `cx.sales.sales-orchestration.data-capture-rules` |
| Explicit Sales Orchestration Pre-requisites setup task | `cx.sales.sales-orchestration.pre-requisites` |

Ask one short clarification when a term such as "content" or "data" could map
to more than one task and that choice changes the answer.

## Cross-Task and Support Questions

- Use the parent skill to explain the catalog hierarchy, task ownership,
  sequence, dependencies, and differences between tasks.
- Use the selected child skill for concepts, metadata, lifecycle, setup,
  security, endpoints, live reads, troubleshooting, and help sources specific
  to one task.
- Preserve each child's read-only execution boundary. The parent must not
  generate a mutation blueprint, call a direct BOSS endpoint, select a browser,
  or substitute another loader for an unsupported task operation.
- Data Loader does not currently support the applicable BOSS REST endpoints.
  Create, Update, and Delete may be added only after that support and the
  repository's write contracts are reviewed.

## Execution Safety

### Preflight

Before producing a durable plan, configuration blueprint, or validation result,
confirm the requested answer mode, question classification, owning task skill,
and project workspace path. For any child-skill live-read request, the selected
child workflow must additionally confirm the target environment, acting-user
context, required privileges, and bounded read inputs before authentication or
an external call. This parent skill has no direct Fusion, browser, OAuth, or
configuration-mutation path.

### Failure Handling

Classify an unclear question or missing supported source as `SOURCE_GAP` and
state the exact Oracle source or SME decision required. Stop on an ambiguous
task classification until it is clarified. For a selected child workflow,
preserve that child's failure classification, retry limits, and sanitized
diagnostics; do not retry, broaden a query, substitute an endpoint, or bypass
an unsupported operation. When a durable artifact is in scope, record only the
safe status, failure class, recommended action, target environment identifier,
and artifact reference under the selected project workspace.

### Redaction

Never request, display, log, or persist passwords, OAuth tokens, client
secrets, private keys, token-cache contents, full authorization headers, or
sensitive customer data. Configuration guidance may identify a setting or
whether a value is present, but must not copy secret values into an answer,
diagnostic, or project artifact.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Sales` (`ORA_MIDSIZE_SALES`)
- Functional area / Setup Object: `Sales Orchestration` (`CUSTOM_SALES_ORCHESTRATION`)

## Setup Tasks

1. [Sales Motions](sales-motions/SKILL.md) (`CUSTOM_SALES_MOTIONS`)
2. [Sales Plays and Content](sales-plays-and-content/SKILL.md) (`CUSTOM_SALES_PLAYS_AND_CONTENT`)
3. [Data Capture Rules](data-capture-rules/SKILL.md) (`CUSTOM_DATA_CAPTURE_RULES`)
4. [Pre-requisites](pre-requisites/SKILL.md) (`CUSTOM_PRE_REQUISITES`): baseline
   readiness plus first-time validation of signals, Microsoft Outlook and email
   integration, and Dispatcher routing.

## Inputs

- `implementation_objective`
- `project_context`
- `sales_orchestration_scope`
- `sales_orchestration_requirements`
- `sales_orchestration_question`
- `requested_answer_mode`: EXPLAIN, READ, CLARIFY, ROUTE, GAP, or REFUSE

## Outputs

- `question_classification`
- `sourced_answer`
- `operation_support_status`
- `source_gap`
- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level questions, planning,
sequencing, setup-data routing, and validation. Track token usage for any
generated project artifact or skill-run record using the manifest policy. Do
not persist an answer-only response unless the active project workflow requires
a durable artifact.

## Help Source

- Functional-area definition, business value, capabilities, and trust model:
  `references/sales-orchestration-overview.md`
- Cross-task question classification and response contract:
  `references/sales-orchestration-question-routing.md`
- First-time environment readiness validation:
  `pre-requisites/references/sales-orchestration-prerequisites.md`
