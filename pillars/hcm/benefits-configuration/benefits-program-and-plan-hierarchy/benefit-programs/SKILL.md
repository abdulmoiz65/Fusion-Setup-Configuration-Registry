---
skill_id: "hcm.benefits-configuration.benefits-program-and-plan-hierarchy.benefit-programs"
name: "Benefit Programs"
description: "Creates or imports an Oracle Fusion Benefits plan from a bundled 401k or commuter template, or an end-user custom native Plan Copy ZIP, under the catalog's Benefit Programs task. For generic plan requests, offer both templates and a custom ZIP upload or local path; program creation is unsupported."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Program and Plan Hierarchy"
functional_area_code: "ORA_BENEFITS_PROGRAM_AND_PLAN_HIERARCHY"
task_code: "BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS"
task_name: "Benefit Programs"
parent_skill_id: "hcm.benefits-configuration.benefits-program-and-plan-hierarchy"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "benefitPlanCopyParameters"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM benefits configuration pillar team"
version: "1.8.9"
inputs:
  - "plan_copy_plan_archive"
  - "fusion_environment_context"
  - "task_context"
  - "plan_copy_import_approval"
outputs:
  - "plan_copy_import_preview"
  - "plan_copy_import_result"
  - "plan_copy_object_report"
  - "validation_checkpoints"
depends_on:
  - "core.runbook"
  - "hcm.benefits-configuration.benefits-eligibility.eligibility-profiles"
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.ess-job-submitter"
persists_project_state: true
state_updates:
  - "setup_task_sequence"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-program-and-plan-hierarchy/benefit-programs/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-program-and-plan-hierarchy/benefit-programs/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
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
side_effects:
  - "When required for a requested plan, merges the catalog-resolved Benefit Programs task into the selected active Run Book and refreshes project planning artifacts."
  - "Preview writes an immutable local JSON artifact and performs no Fusion mutation."
  - "After exact approval, creates a Plan Copy import, uploads the ZIP, submits generateMappings, and monitors the import."
  - "After import, writes a parsed import-log object-count report beside the approved preview without retaining raw RequestLogs in the project."
required_privileges:
  - "OAuth write access to /hcmRestApi/resources/latest/benefitPlanCopyParameters"
  - "OAuth write access to the PackageContent enclosure and generateMappings action"
  - "GET access to Plan Copy mappings, RequestLogs enclosure, child logs, parent status, and ESS request status"
  - "Privileges to view and merge tasks into the selected active Run Book when Benefit Programs is missing"
---

# Benefit Programs

## Purpose

Import an existing native Benefits plan ZIP through Plan Copy REST. Do not
extract, regenerate, or modify the package as part of this workflow.
The Fusion catalog calls the setup task **Benefit Programs**, and its task code
remains `BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS`. This implementation supports
plan packages only (`ComponentObjType=PLN`). It does not create or import
Benefits programs; stop a program request as unsupported rather than
substituting a plan package.

## Plan Source Intake and Workflow

Treat `create a 401k plan` and `create a commuter plan` as direct triggers for
the corresponding template unless the user explicitly supplies a custom ZIP
for that request. For a generic request such as `create a plan` or `create
benefits plans`, offer all three sources: **401(k) template**, **Commuter
Benefits template**, or **custom Plan Copy ZIP**. For example, ask: "Which
plan should I prepare: a 401(k) template, a Commuter Benefits template, or your
custom Plan Copy ZIP? For custom, upload the ZIP or provide its full local path."
Do not present a template-only choice in the GUI or conversational intake.

If an uploaded ZIP or explicit accessible ZIP path is already supplied for the
current request, use it without asking for a template. If the user selects
custom without supplying the file, ask them to upload their native Benefits
plan ZIP or provide its full local path, and stop package preparation until
it is available. If several supplied ZIPs could match, ask which one to use;
do not silently select a ZIP from Downloads, a previous run, or the bundled
assets. Reuse an earlier package only when the user explicitly requests it.

Pass the exact selected custom path as `--zip "<end-user-plan.zip>"`, without
`--template`, to both preview and the later approved submission. Keep the ZIP
unchanged and apply the same native package validation, target/task binding,
immutable preview, and approval checks as for a template. Uploading a ZIP is
not import approval. Multiple plans require separate previews and approvals.
Use the selected ZIP and current target-environment task context.
Do not search for another implementation, rebuild the package, or inspect
unrelated skills.

The Benefits-owned adapter is
`pillars/hcm/benefits-configuration/benefits-common/scripts/benefits_plan_copy.py plan`, which delegates to
the Benefits Plan Copy REST wrapper `scripts/import_plan_configuration.py`,
to create the immutable preview. After a
later exact `approve`, rerun that adapter against the same ZIP and preview,
enter the wrapper's exact interactive approval, and monitor through final
status `12`. Use repository
`core/auth/fusionEnv.properties` and `.fusionaim_token.json` by default; honor
`FUSION_PROPERTIES`, `FUSION_OAUTH_PROPERTIES`, and `FUSION_TOKEN_CACHE` when present. If the
authentication inputs are unavailable or expired, report that single blocker
directly instead of searching the workspace for alternate workflows. A matching
Benefit Programs task must exist in the selected project's active Run Book
task context. If it is absent, follow **Ensure the Benefit Programs task** below
and continue the same plan request; do not stop merely because the current
context contains only Eligibility Profiles. Do not fabricate a task context
or substitute the Eligibility Profiles task.

### Ensure the Benefit Programs task

A request to prepare or create a supported Benefits plan includes the necessary
Benefit Programs task in that request's scope. Use the selected project's
existing active Run Book and configured target. Do not ask the user to provide
a hand-written context or separately request the prerequisite merge.

The prerequisite merge is a Benefits-owned orchestration rule declared here;
it requires no changes to core skills, scripts, policies, or configuration.
For this workflow only, the plan request authorizes the narrow task merge
described below instead of requiring a separately worded merge request under
the generic Run Book guidance. Reuse the unchanged core Run Book services
and retain their target, privilege, payload, execution-permission, and
indeterminate-write checks. This rule applies only to adding
`BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS` to the already selected active Run Book.

1. Read the current project binding and planning artifacts. Resolve
   `Benefit Programs` / `BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS` against the
   maintained setup-task catalog and this skill. Use its Benefits offering and
   Benefits Program and Plan Hierarchy functional area, not the existing
   Eligibility Profiles task's functional area.
2. If the canonical context already contains this task, reuse its sequence.
   If the context lacks it, use `core.runbook` to inspect the active Run Book
   before merging. If the task already exists remotely, refresh the local
   planning artifacts from that verified task instead of adding it again.
3. Otherwise, prepare a delta planning envelope containing only the resolved
   Benefit Programs task and its task notes. Preserve all existing tasks and
   choose a sequence consistent with the active Run Book. Invoke the declared
   `core/runbook/scripts/runbook_rest.py merge-runbook --input-stdin` workflow
   for that active Run Book with the selected environment's authentication.
   This skill explicitly selects that prerequisite operation for the plan
   request; it does not select a new Run Book or authorize unrelated tasks.
4. Require confirmed merge success and return the refreshed dashboard. Only
   then incorporate the task into the project's persisted task mapping,
   preserving existing entries. Regenerate `setup-task-plan.json`,
   `task-context.json`, and `runbook-plan.json` through the maintained
   `core/project-mgmt/project-workspace-initializer/scripts/create_project_runbook.py`
   generator with `--project-root` and `--refresh-artifacts`. Preserve the
   active Run Book binding; do not reset it or synthesize a context JSON.
   Use the verified task sequence and catalog-resolved skill path.
5. Verify the regenerated context selects this task and the same active target
   and Run Book. Record the merge and refreshed artifact references in the
   project run record, then resume the already selected plan's immutable
   preview with that context and sequence. Reuse its locally validated ZIP;
   do not ask which plan again or restart package preparation.
6. A missing Benefit Programs context is recoverable through this workflow,
   not a terminal import-routing blocker. Stop only for an actual unresolved
   project/target selection, catalog ambiguity, permission failure, merge
   failure, or artifact-persistence failure, and report that specific cause.
   If a merge may have succeeded, inspect the same Run Book read-only; never
   retry the merge POST automatically or fabricate success.

This prerequisite merge does not create a plan. Retain the separate immutable
plan preview and existing exact import-approval checks before Plan Copy writes.

For Benefits plan requests, always use this Benefits-owned importer. This is
the explicitly authorized, standing exception to the generic Data Loader
entry-point requirement for this skill; do not ask for routing permission
again, require a native route declaration in core, or edit core files to enable
it. Continue reusing the existing core authentication, transport, Task Hook
and Run Book validation services without changing them. This exception applies
only to the import entry point, not to package validation, task/target binding,
or submission approval. Prepare a fresh immutable preview and require the
later standalone exact `approve` before any import write. Do not treat route
authorization as auto-approval of an import or retry.

## Bundled Templates

Use `--template 401k` for `assets/plan-copy/Greenfield 401k Plan.zip`, or
`--template commuter` for `assets/plan-copy/Greenfield Commuter Benefits Plan.zip`.
The Benefits adapter requires an explicit selection. `--template` and a custom
`--zip` are mutually exclusive.
Do not import both templates without separate previews and approvals.

## REST Contract

Use `references/plan-copy.openapi.json` and the maintained
`scripts/import_plan_configuration.py` adapter. The adapter reuses the existing,
tested eligibility Plan Copy REST engine while selecting
`ComponentObjType=PLN`, task `Benefit Programs`, and import
prefix `BENEFITS_PLAN_`.

The live sequence is:

1. Create `benefitPlanCopyParameters` metadata with `RequestSource=FDOS`.
2. Upload the unchanged ZIP to `enclosure/PackageContent`.
3. Call `generateMappings`; do not call `submitImport`.
4. Poll the returned ESS request.
5. Require zero unresolved mappings and final parent status
   `ImportPlDesign=12`. Treat code `10` as failure.
6. Download `enclosure/RequestLogs`, which exposes the consolidated import log
   stored in `BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB2`. Report failure when the
   log contains an error, even if ESS and the parent report success. Confirm
   success only when the log is non-empty and contains no recognized errors.

Read `references/plan-copy-import.md` for the detailed contract and recovery
rules.

## Validate the ZIP

Validation is local and makes no Fusion request:

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-program-and-plan-hierarchy/benefit-programs/scripts/import_plan_configuration.py validate \
  --zip "pillars/hcm/benefits-configuration/benefits-program-and-plan-hierarchy/benefit-programs/assets/plan-copy/Greenfield 401k Plan.zip"
```

## Create the Immutable Preview

The generated Run Book task-context JSON must point to this skill. Run
**Ensure the Benefit Programs task** first if the current context lacks it;
do not ask the user to supply another context. The OAuth
properties identify the selected target environment through `restBaseUrl`; the
OpenAPI contract remains host-neutral.

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-common/scripts/benefits_plan_copy.py plan \
  --template "<401k-or-commuter>" \
  --sequence "<Benefit Programs task sequence>" \
  --preview-output "<project-artifact-directory>/<selected-plan>.preview.json" \
  --properties "core/auth/fusionEnv.properties" \
  --token-cache auto \
  --task-context "<task-context.json>"
```

For a custom package, replace `--template "<401k-or-commuter>"` in this
command with `--zip "<end-user-plan.zip>"`; retain the remaining target,
task-context, sequence, and preview arguments. Do not pass both source options.

The wrapper derives the effective date and setup-object inventory from the
selected ZIP's embedded Plan Copy export log (401(k): `1951-01-01`; commuter:
`1951-01-01`). It creates a package-specific preview at the caller-selected
`--preview-output` path (or the current directory by default) and stops without
a Fusion POST or PUT. Reuse the exact emitted
`previewPath` and selected template or exact custom ZIP path after approval. In the
user-facing object-count preview, show only Plan, Plan Type, Option, Year
Period, Eligibility Profile, Benefit Group, and Age Factor, and omit any object
whose count is zero. Apply this to both CLI and conversational previews; do not
render zero-count rows or bullets. Keep the complete
log inventory in the immutable artifact for validation, but do not display its
other object types or the Plan Copy mapping count. Ask the user to reply in a
later standalone message exactly `approve`.

## Execute After Approval

Only after validation and that later exact approval, rerun the same Benefits `plan` adapter and
source, target, task, date, and preview inputs with:

```text
--approve-upload --approval-preview "<preview.json>" \
  --object-report-output "<project-artifact-directory>/<selected-plan>.object-report.md"
```

The importer revalidates the OpenAPI and ZIP hashes before the first write and
also requires exact interactive approval. Never retry a POST, PUT, or action
automatically after an uncertain outcome. Preserve the returned Plan Copy ID
and ESS request ID internally for read-only diagnosis or resume. In
user-facing progress and completion output, show the approved Plan Copy name,
never the Plan Copy ID or ESS request ID/status. Show only the `SUCCESS` or
`ERROR` status derived from `MappingRequestStatus`; on error, include sanitized
details from `RequestLogs`. Keep the approved metadata `Name`, IDs, paths and
machine events unchanged internally for approval binding and recovery.
Use the verified Fusion hostname when presenting the target for approval.

## Import Log Object Report

After the import reaches terminal status, download the completed Plan Copy
request's `RequestLogs` enclosure. This is the REST view of the consolidated
import log in `BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB2`; the parent REST JSON
does not contain an inline log. Parse only its `Plan Copy Report` object table.
Do not use warning sections such as `Objects with leading/trailing spaces`
as imported-object evidence.

Write a Markdown report and machine-readable JSON under the project workspace.
The user-facing report contains only setup object names and counts actually
reported by the import log. Exclude Plan Copy mapping and integration-key mapping
rows. Keep existing source inventories and comparison fields in machine artifacts
for compatibility, but do not display them in CLI, Markdown, or conversation.

## Required User-Facing After-Import Summary

After each import finishes, identify the business plan name, approved target
hostname, effective date, and import process status (`SUCCESS` or `ERROR`).
For an error, include sanitized RequestLogs error details without claiming success.
Present the counts directly in a two-column table: `Object` and `Count`, followed
by the total of the reported setup-object counts. Include every setup object type
listed in the import log, including translation types and explicitly reported
zeros; do not add source-only objects, missing-type placeholders, or inferred zeros.

Do not show ZIP counts, before/after columns, count differences, matching-count
summaries, or comparison/verification statuses. If no per-object counts are
reported, state: "The import log did not report object counts." Do not substitute
the initial ZIP inventory. Import process status remains independent of whether
counts were reported, and success still requires the existing status and log-error
checks.

Use the saved result and parsed RequestLogs evidence; never repeat an import to
produce its summary. A report link is supporting evidence, not a replacement for
the inline table. If saving the report fails, disclose that persistence failure
and use only the parsed import-log evidence already available. Keep metadata IDs,
ESS IDs/status, secrets, and raw logs out of the user-facing summary.

For an already completed import, first retrieve its `RequestLogs` through the
read-only recovery route below. Then regenerate the report without another
import:

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-program-and-plan-hierarchy/benefit-programs/scripts/import_plan_configuration.py report \
  --zip "<approved-plan.zip>" \
  --import-log "<downloaded-RequestLogs>" \
  --report-output "<project-artifact-directory>/<selected-plan>.object-report.md" \
  --import-status "<confirmed-process-status>"
```

Persist only the parsed object inventory and a hash of `RequestLogs` under the
project; keep the raw import log in temporary local storage because it may
contain unrelated target object names.

## Failure Rules

- Reject an unreadable, encrypted, path-unsafe, malformed, or structurally
  inconsistent nested ZIP before preview.
- Require the ZIP's embedded export-log inventory to match its nested XML
  package before preview.
- Reject a ZIP containing Benefits program setup rows, even when it also
  contains a Plan row.
- Do not map with guessed IDs or IDs copied from another pod.
- Do not expose credentials, tokens, raw ZIP bytes, or sensitive response
  bodies in output.
- Report success only after ESS success, Plan Copy status code `12`, and a
  non-empty, error-free `RequestLogs` enclosure.
- Treat `RequestLogs` as the consolidated import result. Use `child/logs` only
  for supplemental processing messages when a failure occurs.
- After an import error with a retained Plan Copy ID, retrieve the same
  `enclosure/RequestLogs` REST log used after success before reporting the
  failure. Include seeded `JBO-BEN:::BEN_*` messages and their text; an empty
  `child/logs` response does not mean this enclosure is unavailable. See
  `references/plan-copy-import.md#logs-after-an-import-error`.

## Read-only Report Recovery

For an already completed import whose Plan Copy ID was not retained, use the
declared `core.fusion-api.rest-api-client` to look up
`benefitPlanCopyParameters` by the exact approved metadata `Name` from its
immutable preview. Request only `PlCopyId`, `Name`, `FileName`,
`ComponentObjType`, and `ImportPlDesign`; require exactly one match, the
approved ZIP name, `PLN`, and status `12` before using the existing
`RequestLogs` enclosure GET. This lookup and log download are read-only.
Fail closed on no match, duplicate names, unexpected metadata, or an
unavailable log. Never submit another import to recover a report.
The Plan Copy parent advertises blob-backed enclosure links. Read its
same-origin `RequestLogs` enclosure after import for the BLOB2 log, even when
the parent JSON has no inline `Log` field. Use its `Plan Copy Report` rows for
the object-count summary. If the table is empty, state that the import log did
not report object counts, even when the process status is `SUCCESS`.

## Preflight and Redaction

Preflight completes all local ZIP, policy, OpenAPI, target, metadata, task-rule,
and approval checks before the first Fusion write. On failure, output must
redact authorization headers, passwords, client secrets, access tokens, and
token-cache contents; never print raw package bytes or unbounded REST bodies.
