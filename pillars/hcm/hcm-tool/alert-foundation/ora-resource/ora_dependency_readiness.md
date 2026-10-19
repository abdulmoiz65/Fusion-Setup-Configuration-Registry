# Alert Foundation Dependency Readiness

## Required Dependency Order

For simple CREATE, dependencies are evaluated from the locally validated intake,
the fixed supported adapter contract, configured environment and declared
authorization assumption. The live checks in this section apply to deep mode
only, except identity/current-state checks for existing-item mutations and
post-submission read-back. A skipped live check is not a passed live check.

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | 1 | Compatible eventAlerts contract | Resolve the target-environment describe contract for the selected method |
| CUSTOM_ALERTS | Alerts | 2 | Alert type and access level | Resolve exact target-environment lookup codes |
| CUSTOM_ALERTS | Alerts | 3 | Alert identity and current state | Prove uniqueness for create or resolve one exact existing AlertId |
| CUSTOM_ALERTS | Alerts | 4 | Authorized execution route | Select core.fusion-api.rest-api-client through this provider skill |
| CUSTOM_ALERTS | Alerts | 5 | Immediate approval | Bind one explicit approval to the exact immutable Alert hierarchy create work unit, or individual approval to a mutation outside that route |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | batch_create_route | Reviewed single batch POST route | Yes | Explicit batch-create | Satisfied | Locally enforced versioned batch adapter; deep additionally resolves compatible_contract | | Keeps latest root and version 4 scoped to the supported create envelope | Bind validation mode, exact payload and one approval; simple does not need live gate evidence | Mode, source digest, exact headers, complete parts envelope and aggregate fingerprint |
| CUSTOM_ALERTS | Alerts | compatible_contract | Compatible eventAlerts describe | Yes | Deep validation or explicit metadata inspection | Verify | Target Fusion environment | inspect_event_alert_contract | Prevents release-path or metadata drift | Use the exact target environment | Compatible methods, key, finders, fields |
| CUSTOM_ALERTS | Alerts | template_mime_type | Valid Template MIME code | Yes | Deep validation with Templates | Lookup | Target Fusion MIME lookup | resolve_template_mime_type | Detects invalid MIME values before submission | Select one exact returned code | MimeType and meaning |
| CUSTOM_ALERTS | Alerts | template_language | Valid Template language | Yes | Deep validation with Templates | Lookup | Target Fusion active languages | resolve_template_language | Detects invalid language values before submission | Select one exact returned language code | DefaultLanguage and description |
| CUSTOM_ALERTS | Alerts | alert_type | Valid alert type | Yes | Deep mode: create or AlertType change | Lookup | ORA_HRC_ALERT_TYPE | resolve_alert_type_code | Prevents an invalid type code | Select one returned code | AlertType, AlertTypeMeaning |
| CUSTOM_ALERTS | Alerts | access_level | Valid alert access level | Yes | Deep mode: create or AlertAccessLevel change | Lookup | ORA_HRC_ALERT_ACCESS_LEVEL | resolve_alert_access_level | Prevents an invalid access classification | Select one returned code and confirm intended ownership | AlertAccessLevel, AlertAccessLevelMeaning |
| CUSTOM_ALERTS | Alerts | alert_identity | Unique alert identity | Yes | Deep create; existing-item mutations in either mode | Verify | eventAlerts finder and server-returned canonical item context | find_event_alert_by_code | Prevents duplicates and wrong-item mutations | Simple CREATE delegates existing-code conflicts to Fusion; existing-item mutations still require exact fresh identity | AlertId, canonical key/URI, and current-state fields |
| CUSTOM_ALERTS | Alerts | recipient_channel | Valid Template Recipient channel | Yes | Deep mode with Template Recipients | Lookup | ORA_HRC_ALERT_CHANNEL_TYPE | resolve_recipient_channel_type | Prevents invalid recipient transport codes | Select one returned target-environment code | ChannelType and meaning |
| CUSTOM_ALERTS | Alerts | recipient_expression | Live Template Recipient expression validation | No | Deferred capability work only | Deferred | Product decision recorded for provider version 0.8.0 | | Keeps the deferred action outside runtime preflight | Do not call eventAlerts validateExpression; retain required presence and maximum-length validation locally | Deferred status |
| CUSTOM_ALERTS | Alerts | child_parent_keys | Exact supplied and verified parent and Template canonical keys | Yes | Template create, inline Body PATCH, or Template Recipient create | Verify | Reviewed AlertCode and TemplateCode before approval; server-returned create responses and independent read-back during execution | | Prevents child writes against assumed or changed keys | Precompute exact child paths and stop the work unit if a create response does not return the approved key | Alert and Template canonical keys |
| CUSTOM_ALERTS | Alerts | inline_body_execution_route | Reviewed inline Body route for selected mode | Yes | Inline Template Body is supplied | Satisfied | Observed plain-text PATCH and batch Base64 create behavior | | Sequential uses plain-text PATCH; batch-create nests UTF-8 Base64 Body in Template CREATE | Bind the mode-specific representation in the one approved work unit and disclose deferred stored-content verification | Mode, payload digest and verification limitation |
| CUSTOM_ALERTS | Alerts | file_body_execution_route | Reviewed raw Body enclosure route | Yes | BodyFilePath or BodyFileSHA256 is supplied | Blocked | Shared REST client capability | | Version 0.8.0 cannot submit raw attachment bytes | Omit both file-based Body fields or complete the future shared-client enhancement | Raw-byte route and content type |
| CUSTOM_ALERTS | Alerts | mutation_authorization | Product-owner security assumption plus runtime authorization | Yes | Create, update, disable, delete, or copy | Satisfied | User-confirmed role/access assumption; runtime 403 remains authoritative | | Records the declared security basis without treating GET as technical proof | Confirm the executing identity is the intended authorized identity | Authorization assumption |
| CUSTOM_ALERTS | Alerts | exact_approval | Immediate mutation approval | Yes | Create, update, disable, delete, or copy | Blocked | Current conversation approval bound to the aggregate create work unit or individual immutable preview | | FDOS requires exact approval immediately before the declared execution step | For an eligible hierarchy create, approve every shown ordered operation with Confirm Alert Work Unit and its aggregate SHA-256; otherwise approve the individual mutation | Aggregate or individual approval fingerprint |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Satisfied | Required input and authoritative evidence are present | Yes for read-only lookup; mutation still needs approval |
| CUSTOM_ALERTS | Alerts | Lookup | A declared read-only resolver can supply the value | Yes for lookup only |
| CUSTOM_ALERTS | Alerts | Verify | Supplied identity or metadata must be confirmed | Yes for read-only verification only |
| CUSTOM_ALERTS | Alerts | Blocked | Identity, compatibility, route, or approval is unresolved | No |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | ALERT.DEPENDENCY | decision | 3 | resolve_dependency | ready->ALERT.DESIGN;blocked->ALERT.RETURN_ISSUES | ALERT.LOOKUP | stop | Always |
