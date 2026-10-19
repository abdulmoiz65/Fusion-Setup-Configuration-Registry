---
task_code: "CUSTOM_CONFIGURE_BACKGROUND_PROCESSING"
task_name: "Configure Background Processing"
parent_skill_id: "hcm.learning-management.learning-configurations"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Configurations"
functional_area_code: "ORA_LEARNING_CONFIGURATIONS"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Configure Background Processing

## Purpose and route

Review workload concurrency, immediate-processing choices and execution identity
for Learning. Changing defaults and submitting/scheduling an ESS process are
different operations with different approvals. Use the
[common workflow](references/workflow.md) and [dependencies](references/sources-and-dependencies.md).
Do not run every Learning process as an enablement step.

## Contract Not Resolved

CSV and export/import support are N. Generated REST mode and empty businessObject
are not a registered Data Loader route. The taxonomy marks the BC REST contract
TBD ETA 27B. Current-setting reads, write schema, exact privileges and readback
mapping are TBD; do not use generic REST, Data Loader or browser fallback.
A job display name is not an ESS package/definition/parameter contract.

## Intake and inventory

Ask which workload needs attention, expected volume/latency, present symptoms,
bulk versus UI activity, existing schedules/timezone and intended run-as policy.
Review Assignments, Recommendations and Access separately; then Catalog Items
and Execution Details. Inventory each setting in the canonical resource tables,
not just the settings proposed for change. Unknown live values are Unverified.

Source D7 describes My Client Groups > Learning and Development > Configure
Background Processing. The resource files own its numeric constraints, delivered
defaults, recommendations and toggle dependencies:
[input validation](ora-resource/ora_input_validation.md),
[defaulting](ora-resource/ora_defaulting_rules.md),
[design](ora-resource/ora_design_enforcement.md).
Do not conflate reconciliation UI jobs with expansion UI threads.

## Design and sequencing

1. Inspect attributable current evidence and existing schedules only through
   a declared reader. No reader: record Not validated and continue planning.
2. Compare proposed concurrency with workload and platform capacity. Discuss
   contention with other enterprise processing; record the customer's reason
   for a valid exception. Do not automatically apply a tuning recommendation.
3. Evaluate immediate-processing toggles together with their downstream
   processing requirement. Show the dependency and its owner before approval.
4. For an execution-identity change, confirm the exact eligible account and
   appropriate permissions through a selected workflow. Never create accounts
   or grant roles as an implicit prerequisite.
5. If process scheduling is separately requested, require a supported job
   definition, parameters, timezone, frequency, existing-schedule comparison,
   approval and bounded monitoring in the owning process workflow. Reuse an
   appropriate schedule; do not submit duplicate jobs.
6. Present settings changes and schedule operations separately, with exact
   operation counts only after provider resolution. Neither is executable
   while its contract remains incomplete.

## Acceptance evidence

Re-read each attempted setting through the future approved reader. Observe a
representative separately authorized workload and check its expected processing
path, result and identity. Capture sanitized status/log references. A saved
concurrency value or accepted ESS submission is not evidence that processing
finished. Keep application configuration, job completion and downstream results
as separate acceptance checks. Poll the original request with the provider's
interval and timeout; do not replay an uncertain submission.
