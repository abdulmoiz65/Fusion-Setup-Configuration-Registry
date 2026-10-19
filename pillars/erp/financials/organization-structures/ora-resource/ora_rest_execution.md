# Organization Structures Execution Boundary

No authoritative REST write action, request-body, or describe metadata is supplied here. Direct REST writes remain unavailable. For CSV import, a freshly completed same-task template/spec export from the target environment becomes approved package evidence only after the emitted metadata descriptor and every header have been inspected.

## Runtime Sources

| Task Code | Task Name | Source | Purpose |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | TBD approved Oracle REST describe metadata or machine-readable contract | Required before previewing a direct REST write |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | TBD approved Oracle REST describe metadata or machine-readable contract | Required before previewing a direct REST write |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Fresh same-environment template/spec, inspected metadata, and current CSV headers | Required before previewing a CSV import; a direct REST write remains unavailable |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Fresh same-environment template/spec, inspected metadata, and current CSV headers | Required before previewing a CSV import; a direct REST write remains unavailable |

## Execution Contract

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | A direct REST write is requested, or no fresh same-task template/spec is available for a CSV import | Stop. Do not invent an endpoint or package format. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A direct REST write is requested, or no fresh same-task template/spec is available for a CSV import | Stop. Do not invent an endpoint or package format. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | A direct REST write is requested, or no fresh same-task template/spec metadata is available for CSV import | Stop. Do not invent an endpoint or package format. With the inspected template, prepare only the emitted CSVs and fields. |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | A direct REST write is requested, or no fresh same-task template/spec metadata is available for CSV import | Stop. Do not invent an endpoint or package format. With the inspected template, prepare only the emitted CSVs and fields. |

## Import Completion Evidence

Treat API process completion as incomplete evidence until the downloaded `ProcessLog` is reviewed. Record the process ID, row counts, failures, and warnings. Do not continue from Business Unit creation to function assignment unless the Business Unit detail object completed successfully. Ensure the local output directory exists before submitting the import so the process log can be retrieved.

## Preview Pattern

| Task Code | Task Name | Step | Requirement |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Contract gate | Do not produce a write preview without approved endpoint and field metadata |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Contract gate | Do not produce a write preview without approved endpoint and field metadata |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Contract gate | Do not preview a direct write; preview CSV only from the fresh target template and inspected metadata |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Contract gate | Do not preview a direct write; preview CSV only from the fresh target template and inspected metadata |
  <!-- -->


Full populated data export is prohibited by the parent BU policy and ora_design_enforcement.md for this resource and all delegates. The task template establishes shape; packaged rules and permitted current-state sources supply values. Native reference-set creation remains the separately declared setIdSets prerequisite in ora_reference_lookups.md; this file does not authorize a direct REST mutation of any BU task.


## Operation-Specific Preparation and Resume

For BUSA_FSM_ADD_OVERRIDE_V1 and SPR_FSM_ADD_RELATIONSHIP_V1, evaluate the independent eligibility/field tables in ora_bulk_intake.md before Task Hook. Do not mark a genuine missing lookup as passed: record tested omissions, explicit current-workflow decisions, fresh reads and qualified first-submission assurance with their exact limits. Inside these profiles no missing-field waiver is needed; all normal Data Loader preflight, rule evaluation and immutable archive approval gates remain.

Create local archive/download/log destination folders before retrieval. If a completed template process cannot be saved because a directory is missing, repair local persistence and retrieve that recorded process; do not submit a second export. Refresh OAuth serially before independent read batches. Preserve completed stages on resume, re-resolve time-sensitive facts and reconcile request/fingerprint receipts before any write. After submission apply mandatory log review to both success and failure; processing acceptance, independent saved-value checks and unavailable reads are distinct results.
