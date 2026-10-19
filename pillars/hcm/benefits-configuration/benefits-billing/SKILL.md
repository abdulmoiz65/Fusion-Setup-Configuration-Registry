---
skill_id: "hcm.benefits-configuration.benefits-billing"
name: "Benefits Billing Implementation Guidance"
description: "Prepares and validates Benefit Bill Calendars samples and routes approved benefitBillCalendars HDL loads through core.data-loader, including bill-period linkage and failure recovery."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Billing"
functional_area_code: "ORA_BENEFITS_BILLING"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
version: "0.2.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "benefits_billing_scope"
  - "benefits_billing_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
uses_core:
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-billing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-billing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-billing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "BEN_MANAGE_PROGRAMS_PLAN_YEARS"
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

# Benefits Billing

## Scope and Authority

Implement Benefit Bill Calendars under the catalog task
`BEN_MANAGE_PROGRAMS_PLAN_YEARS` (Year Periods and Billing Calendars).
The requested import mode is `HDL` and the exact configured object is
`benefitBillCalendars`. Separate year-period setup, bill generation, payments,
and other Benefits Billing tasks are outside this skill's implementation scope.

The developer supplied the HDL object identity. Live registration, its DAT
template, child discriminators, keys, and supported operations have not yet
been verified for this skill. This is an execution prerequisite, not permission
to infer HDL support from a REST resource with the same name. Stop if the exact
object is absent, ambiguous, or incompatible with the requested mode; report
the actual metadata and ask for a corrected mapping. Do not silently switch to
REST, FSM, a BOSS object, another pod, or another business-object name.

Read [task metadata](year-periods-and-billing-calendars.md) for catalog identity
and [calendar contract guidance](references/calendar-contract.md) for field
semantics and validation boundaries. REST documentation is supporting evidence,
not an HDL template or permission to call a write endpoint.

## Input and Validation Workflow

### No-file calendar intake and period generation

When no file is supplied for calendar creation, ask for missing Calendar Name,
Payment Due Day, and Days Overdue. Default Period Type to Calendar and Billing
Frequency to Monthly, and display these defaults in the preview. Reuse explicit
values already supplied instead of asking again. For bill-period creation, also
ask for missing Start Year and End Year. Include both endpoint years.

Generate January through December for each year: 12 × (End Year − Start Year + 1)
periods. Use full English month names, independent of system locale.

| Field | Approved generation rule |
|---|---|
| Billing Period | <Calendar Name>_<Year>_<Month Name>, for example BenefitsBilling_2026_January |
| Year | Corresponding year |
| Period Start Date | First calendar day of the corresponding month |
| Period End Date | Last calendar day of the corresponding month |
| Payment Due Date | Payment Due Day in the corresponding month and year |
| Payment Overdue Date | Payment Due Date plus Days Overdue calendar days |

Each generated period spans its corresponding calendar month, including leap-year
February. Overdue dates can roll into the next
month or year. Reject reversed year ranges, noninteger day/year inputs, negative
Days Overdue, and impossible dates. If a due day is unavailable in any month,
ask for a valid day or explicit alternative handling; do not clamp, skip, or
roll the due date. Preserve zero Days Overdue.

Use [the local preview helper](scripts/preview_bill_periods.py) after intake:

```bash
python3 scripts/preview_bill_periods.py --calendar-name BenefitsBilling --payment-due-day 15 --days-overdue 10 --start-year 2026 --end-year 2027
```

Run from this skill folder. Its JSON is internal preview data, not a REST
payload, DAT template, or upload artifact. Present a readable preview and total
record count. Preserve the helper's `YYYY-MM-DD` date strings when preparing
bill-period DAT rows; do not reformat them to slash-separated HDL dates.
Map the approved business values and Calendar/Monthly labels to
the exact live loader attributes and lookup codes through core; do not assume
display labels are transport codes. If explicitly supplied settings differ from
these defaults, preserve them and clarify the generation rules rather than
running the monthly helper with conflicting settings.

For supplied .dat, .xlsx, .xls, CSV, ZIP, or other files, retain the file-based
workflow and do not regenerate or overwrite its rows using these defaults.
An unsupported format is not an absent file: ask for a core-supported format
(for example .xlsx instead of legacy .xls), without silently converting it.
Missing values within a supplied file follow normal validation/correction.
This skill-edit approval is not approval for any future Fusion submission.

### Shared validation and loader handoff

1. Establish sample, validation, create, update, delete, or status intent; retain
   the user's source path, target environment, calendar identity, period scope,
   and requested operation. An unspecified create request generates a sample,
   not a live load. Ask only for missing inputs that affect the operation.
2. Route through [core.data-loader](../../../../core/data-loader/SKILL.md),
   preserving the active Run Book and task context. Let core resolve exact
   `benefitBillCalendars` registration, live template, writable attributes,
   mandatory-for-create flags, alternate keys, child linkage, and privileges.
   Do not inspect only always-mandatory fields: requirements for new records
   and conditional dependencies must also be reviewed. Application-generated
   IDs marked mandatory for updates are not invented for new records.
3. Validate nonempty readable input, supported file type, safe archive paths,
   exact headers and discriminators, duplicate mappings, field types, supported
   operation, and operation-specific required values using core. For confirmed
   DAT registration the filename is `benefitBillCalendars.dat`; derive child
   sections from its live template rather than guessing from REST names.
4. For new calendars, check the calendar name, frequency, payment due day, and
   overdue interval against the confirmed target contract. For periods, check
   their identity, calendar linkage, year, and date fields. Reject malformed
   dates and flag reversed start/end dates for correction. Preserve explicit
   zero values. Apply only the no-file defaults explicitly approved above;
   otherwise do not invent lookup codes, date defaults, or numeric ranges.
   Enforce additional overlap, frequency, and due-date policies only when
   documented by target metadata or confirmed business requirements.
5. For updates or child-only requests, require an unambiguous existing target
   or a supported source/user key. Do not generate surrogate IDs, assume names
   are unique, or copy IDs from another environment. Do not populate unrelated
   parent or child records to make a sample loadable. Renaming a MERGE record
   or removing its ID does not guarantee insertion: alternate keys may match.
6. Samples use core's XLSX default; generate DAT only when requested. Preserve
   its attribute-details companion and supported parent/child structure. Never
   substitute placeholders for database/export-derived values or embed DB
   connectivity in this skill. Samples and validation do not upload anything.

### Bill-period date format gate

For `benefitBillPeriods`, serialize `PeriodStartDate`, `PeriodEndDate`,
`PaymentDueDate`, and `PaymentOverdueDate` as zero-padded `YYYY-MM-DD` calendar
dates. Apply this billing-specific rule when preparing DAT rows even when a
generic loader sample uses `YYYY/MM/DD`. See the
[date-format evidence](references/calendar-contract.md#bill-period-date-format).

Before immutable archive preparation, inspect all populated values in these four
columns. Normalize unambiguous, valid `YYYY/MM/DD` dates in a reviewed working
copy, preserving the original file and date values; reject impossible dates,
ambiguous locale dates, and timestamps rather than guessing or truncating.
Check the final converted DAT as well as the preview. If core conversion changes
the dates back to slash format, stop and correct the prepared source before
validation and approval. A template/header validation pass alone does not prove
that the backend accepts field values. Do not change generic date rules for
other objects or modify an already-approved archive. Corrections require fresh
validation and upload approval.

## Approval and Submission

Let core.data-loader own conversion, live schema validation, immutable archive
preparation, Task Hook validation, approval, UCM upload, and load initiation.
Use the selected catalog task for Task Hook. A missing task-rule registry
follows core's explicit not-applicable policy; do not claim that these prose
checks are a compiled or automatically executed business-rule registry.

Render approval feedback only after all applicable checks pass. Follow core's
standalone approval or same-request auto-approval policy without adding a
second approval. On approval, submit the integrity-checked saved artifact, not
a rebuilt source. Changed execution context or artifact requires fresh
validation and approval. Never call UCM, native HDL, or calendar REST mutations
directly. Never turn an import into a delete-and-recreate operation.

Return core's Markdown result verbatim. Accepted initiation is not completion.
Query status only when requested; retain its request ID and report final
loaded/failed counts and applicable diagnostics. For requested monitoring,
follow core's polling/timeout contract and never resubmit a pending load.

## Error Handling and Recovery

| Failure class | Required response |
|---|---|
| Input validation | Identify the source, section, row, and field when available; request corrected data before preparing approval. |
| Catalog or metadata mismatch | Report the exact unresolved task, object, component, key, or operation. Stop; no fallback route or fabricated schema. |
| Authentication or authorization | Use core authentication's permitted refresh once; stop after repeated rejection. Never substitute credentials or environments. UCM insufficient-access responses require administrator action, not upload retries. |
| Transport or timeout before submission | Report the failed stage and core's permitted next action; do not claim acceptance. |
| Upload or initiation uncertainty | Preserve returned IDs and approved artifact; reconcile before any retry. Do not replay a potentially accepted mutation. |
| Import or load failure | Retrieve diagnostics through core on request; report resolved field errors where available and preserve successful rows. Corrected data requires a fresh validation and approval cycle. |
| Monitoring timeout | Report request ID, target, last status, elapsed wait, and next-check action; do not label the job completed or automatically reload it. |
| Artifact persistence or approval failure | Stop before submission and report the missing, changed, or unwritable artifact or approval context. |

Do not automatically roll back or delete successful calendars/periods. Follow
core's output and diagnostic-file policy; redact credentials and tokens. Keep
customer data and local test files out of tracked skill files. The pillar owns
durable scope/design decisions through its declared project services; core
owns loader outputs and approval artifacts without duplicate pillar logs.

## Verification

Run the offline contract tests and review the synthetic
[workflow scenarios](tests/golden-scenarios.md). These do not prove live import
success. Before merging, run the repository's skill merge audit on committed
HEAD and obtain HCM Benefits SME/Pillar Lead and FSCR core review.

## Setup Tasks

1. [Year Periods and Billing Calendars](year-periods-and-billing-calendars.md) (`BEN_MANAGE_PROGRAMS_PLAN_YEARS`)
