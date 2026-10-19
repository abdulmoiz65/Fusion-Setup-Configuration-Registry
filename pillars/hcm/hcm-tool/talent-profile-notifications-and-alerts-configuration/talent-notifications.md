---
task_code: "HRT_MANAGE_TALENT_NOTIFICATIONS"
task_name: "Talent Notifications"
parent_skill_id: "hcm.hcm-tool.talent-profile-notifications-and-alerts-configuration"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Talent Profile Notifications and Alerts Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_NOTIFICATIONS_AND_ALERTS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Talent Notifications

## Setup Task Metadata

- Task name: `Talent Notifications`
- Task code: `HRT_MANAGE_TALENT_NOTIFICATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Request Routing

Classify the request before any project, authentication, REST, FSM export, or
Data Loader step:

- guidance-only requests return local guidance with no target-environment
  claims;
- blank-template requests return
  `assets/talent-profile-notifications-requirements.xlsx` unchanged;
- draft-questionnaire requests retain only user-supplied values, permit missing
  fields as open questions, carry an explicit unvalidated label, and do not
  generate XLSX automatically;
- only an explicit configure, enable, disable, turn-on, turn-off, stop, start,
  apply, submit, or other implementation request enters the workflow below.

None of the first three modes requires Fusion authentication, complete
notification rows, an FSM export, or persistence approval. A supplied row or
file without explicit change intent remains a draft and never authorizes
implementation.

## CSV Export, Import, and Validation Workflow

For explicit implementation only, before any FSM export, resolve `environment`
and `restBaseUrl` from the active
`core.auth.fusion-oauth-authentication` context. Do not request a quarterly
release. Through `core.fusion-api.rest-api-client`, issue one 60-second bounded
GET to
`/hcmRestApi/resources/11.13.18.05/talentNotifications?onlyData=true&limit=1`.
Treat `11.13.18.05` as an API resource version only. A valid HTTP 200 JSON
collection, including an empty `items` array, establishes read capability; it
does not supply runtime notification data.

Stop before FSM processing on any capability failure. Preserve distinct reason
codes for final 401 (`rest_capability_unauthenticated`), final 403
(`rest_capability_forbidden`), 404 (`rest_capability_unavailable`), timeout
(`rest_capability_timeout`), transport (`rest_capability_transport_failure`),
other HTTP (`rest_capability_http_failure`), and malformed response
(`rest_capability_malformed_response`).

Record a quarterly release only when an explicit value is already present in
trusted authenticated-context or validated same-environment FSM metadata.
Retain its source and timestamp, omit it when absent, and block conflicting
trusted values without asking the user. Never infer a release from the REST
version, hostname, documentation, date, catalog path, or conversation.

`CSVExportImportSupportedFlag` is `Y`. Route task setup data through:

1. `shared.setup-export.task-level-export` for template, current-state, and
   post-import exports.
2. `shared.validation.setup-data-validator` for exported or prepared setup
   data.
3. `core.data-loader` for the one approved import.

The parent skill accepts an exact delivered identifier or label, or business
intent that the user confirms against candidates from a fresh current-data
export. Partition that export before resolution. Only rows whose exact exported
`ProductCode` is `HRT` are eligible; other nonblank product codes are out of
scope, and blank or ambiguous scope evidence fails closed. This rule is dynamic
and must not be replaced by a fixed name or row-count allowlist.

The eligible export rows supply authoritative `NotifId`, `NotifName`,
`NotifLabel`, current `NotifEnabled`, candidate context, and every technical
value. Copy each confirmed eligible row in this exact order:

```text
NotifName, ViewInstanceName, GroupingKey, Description, NotifEnabled,
NotifLabel, ProductCode, NotifId
```

Use unique nonblank `NotifId` as the provider key when available; otherwise use
unique nonblank `NotifName` provisionally and fail closed if its uniqueness or
value changes. `Description`, `GroupingKey`, `ViewInstanceName`, and
`ProductCode` may assist candidate discovery only after exact `HRT` eligibility
has been established and never selects a row without confirmation. Do not infer
scope from a notification-code prefix, label, description, business intent, or
user-supplied tab.

If an exact identity exists only under another exported product code, return
`validation_failed` with `reason=out_of_scope_notification`. If no current FSM
row establishes the identity, use
`reason=unsupported_by_current_fsm_provider`. Fail the complete set before
preview when any requested row is unsupported, out of scope, or has invalid
scope evidence.

Change only `NotifEnabled` to `Y` or `N`; preserve the other seven serialized
values, including blanks and quoting. Build a minimal FSM upsert package that
retains unchanged metadata and every required CSV member, preserves native
encoding and line endings, and includes only approved changed rows. Keep an
unused required CSV header-only. Rows omitted from the package remain
unchanged and are not deleted. Export again after import and verify the same
provider keys, exact `ProductCode=HRT` scope, and enabled values. Do not
substitute REST, HDL, browser automation, or a task-local adapter. The declared
bounded REST GET is preflight capability evidence only and is never a runtime
notification-discovery, persistence, current-state, or readback route.

Use this task context internally when invoking the shared skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Talent Profile Notifications and Alerts Configuration`
- Setup task name: `Talent Notifications`
- Setup task code: `HRT_MANAGE_TALENT_NOTIFICATIONS`

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or
validating setup data for `Talent Notifications` under `Talent Profile
Notifications and Alerts`.

For notification configuration, invoke the parent
`hcm.hcm-tool.talent-profile-notifications-and-alerts-configuration` skill. This metadata file
does not own intake, mapping or candidate confirmation, approval, submission,
readback, or Alerts Composer execution.
