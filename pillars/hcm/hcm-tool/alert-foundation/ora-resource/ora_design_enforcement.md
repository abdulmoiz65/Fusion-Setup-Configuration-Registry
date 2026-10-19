# Alert Foundation Design Enforcement

## Mode Scope

Separate parent/child writes, Body PATCH and per-hierarchy Confirm Alert Work Unit
rules below apply to sequential mode only. Explicit batch-create substitutes one
whole-workbook JSON parts envelope, one Confirm Alert Batch fingerprint and one
POST as defined in the batch-create runbook. Simple CREATE applies local design
and identity/correlation checks and delegates business values and existing-code
conflicts to Fusion. Deep adds live lookup and duplicate checks. Environment,
authorization assumption, file-Body exclusions and exact approval apply in both.
Batch response success cannot establish server atomicity, rollback or
stop-on-first-part-error. Require all returned parts to match and then independent
canonical read-back; stored Body verification remains deferred.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | 1 | Confirm operation boundary | Permit create, update, disable, delete, or copy only; reject upsert and process |
| CUSTOM_ALERTS | Alerts | 2 | Confirm identity and ownership | Check local keys for simple CREATE; prove zero live duplicates for deep CREATE; require exactly one current item for any existing-item operation |
| CUSTOM_ALERTS | Alerts | 3 | Confirm safe payload | Use only described writable fields and require explicit enablement and test-mode decisions |
| CUSTOM_ALERTS | Alerts | 4 | Confirm ordered mutation plan | For one eligible hierarchy CREATE, bind separately submitted parent and child calls into one ordered work unit with verification after each call; otherwise retain one-mutation planning |
| CUSTOM_ALERTS | Alerts | 5 | Confirm immutable preview | Bind exact approval to the aggregate work-unit document and digest, or to the individual mutation preview when the work-unit route does not apply |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Deep mode and requested_intent is create | Blocking | find_event_alert_by_code | AlertCode already resolves to an item | Use a unique reviewed AlertCode and create with explicit EnabledFlag and TestModeFlag | Yes |
| CUSTOM_ALERTS | Alerts | requested_intent is update, disable, delete, or copy | Blocking | read_event_alert_by_canonical_key | The server-returned canonical key/URI and AlertId do not resolve to the expected code and current state | Refresh current state and regenerate the preview | Yes |
| CUSTOM_ALERTS | Alerts | Deep mode and AlertType is created or changed | Blocking | resolve_alert_type_code | Code is not returned by ORA_HRC_ALERT_TYPE | Select a returned target-environment code | Yes |
| CUSTOM_ALERTS | Alerts | Deep mode and AlertAccessLevel is created or changed | Blocking | resolve_alert_access_level | Code is not returned or intended ownership/editability is not confirmed | Select a returned code and include ownership rationale in approval | Yes |
| CUSTOM_ALERTS | Alerts | requested_intent is upsert | Blocking | | Stable upsert identity and duplicate behavior have not been certified | Use explicit create or exact-item update | No |
| CUSTOM_ALERTS | Alerts | requested_intent is process | Blocking | | processAlert may deliver notifications and is outside CRUD scope | Route notification delivery through a separately reviewed capability | No |
| CUSTOM_ALERTS | Alerts | A parent CREATE has child Templates or Recipients | Blocking | | The hierarchy is not represented as one exact parent-first work unit or a child URI contains an unresolved key | Generate exact URIs from reviewed AlertCode, TemplateCode, and RecipientCode values; order Alert POST, Template POST, optional inline Body PATCH, then Recipient POST | Yes |
| CUSTOM_ALERTS | Alerts | An inline Template Body is supplied | Blocking | | The exact Template item PATCH is absent, Body is combined with file fields, or the preview claims independent Body read-back | Include one exact plain-text Body PATCH after Template verification, accept HTTP 200 as the version 0.8.0 result, and disclose deferred read-back | Yes |
| CUSTOM_ALERTS | Alerts | File-based Template Body is supplied | Blocking | | The shared REST client has no reviewed raw-byte request mode in version 0.8.0 | Omit BodyFilePath and BodyFileSHA256 or complete the future shared-client enhancement | No |
| CUSTOM_ALERTS | Alerts | An eligible hierarchy CREATE is proposed | Blocking | | Exact immediate approval is absent or does not match the current aggregate work-unit fingerprint | Present the complete immutable work-unit document and request Confirm Alert Work Unit followed by its SHA-256 | Yes |
| CUSTOM_ALERTS | Alerts | Any other mutation is proposed | Blocking | | Exact immediate approval is absent or does not match the current individual preview fingerprint | Present the complete immutable mutation preview and request approval immediately before one submission | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | find_event_alert_by_code | Deep CREATE duplicate prevention or required existing-item resolution | Match count, AlertId, current business state | ora_reference_lookups.md |
| CUSTOM_ALERTS | Alerts | read_event_alert_by_canonical_key | Existing-item preview or post-mutation verification | Exact canonical key/URI, AlertId, and current or actual business state | ora_reference_lookups.md |
| CUSTOM_ALERTS | Alerts | resolve_alert_type_code | Deep CREATE or deep AlertType change | AlertType and meaning | ora_reference_lookups.md |
| CUSTOM_ALERTS | Alerts | resolve_alert_access_level | Deep CREATE or deep AlertAccessLevel change | AlertAccessLevel and meaning | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | ALERT.DESIGN | decision | 4 | design_enforcement | pass->ALERT.APPROVAL;blocked->ALERT.RETURN_ISSUES | ALERT.DEPENDENCY | stop | Always |
