# Alert Foundation Input Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Request identity | contract_version, consumer_skill_id, project_id, requested_intent, target_environment | Stop before external access | Supply the missing provider request fields | Always | |
| CUSTOM_ALERTS | Alerts | Create identity | AlertCode, Name, AlertType, AlertAccessLevel, EnabledFlag, TestModeFlag | Stop before preview | Supply an exact unique alert code and every explicit create decision | requested_intent is create | |
| CUSTOM_ALERTS | Alerts | Template create identity | TemplateCode, Name, MimeType, DefaultLanguage, EnabledFlag, Subject | Stop before preview | Supply the explicit Template values; inline Body remains optional | a Template create is requested | |
| CUSTOM_ALERTS | Alerts | Template Recipient create identity | RecipientCode, ChannelType, ValueExpression and the included parent Template key | Stop before preview | Supply the exact recipient values and use the reviewed AlertCode and TemplateCode to form its exact URI before approval | a Template Recipient create is requested | |
| CUSTOM_ALERTS | Alerts | Optional inline Template Body | Body is blank/absent or plain text and must not be combined with BodyFilePath or BodyFileSHA256 | Stop before preview | Supply plain text in Body or leave it blank; use no file fields with inline Body | a Template create is requested | |
| CUSTOM_ALERTS | Alerts | Optional file-based Template Body | BodyFilePath and BodyFileSHA256 must be both blank or both supplied | Stop before preview | Leave both blank for the version 0.8.0 executable route; file-based Body remains planning-only | a Template is supplied | |
| CUSTOM_ALERTS | Alerts | Existing item identity | AlertId plus the server-returned canonical key/URI, or an AlertCode that resolves to exactly one item | Stop before preview | Supply an exact alert code and retain AlertId as internal verification identity | requested_intent is update, disable, delete, or copy | find_event_alert_by_code |
| CUSTOM_ALERTS | Alerts | Update body | At least one writable changed field and the expected current value | Stop before preview | Supply only the intended field changes and current-state expectation | requested_intent is update or disable | read_event_alert_by_canonical_key |
| CUSTOM_ALERTS | Alerts | Approval binding | For an eligible hierarchy create: exact environment, source digest, ordered operations, methods, URIs, canonical payloads, per-operation digests, effects, verification plans, execution policy, and aggregate SHA-256; otherwise the exact individual mutation preview | Return approval_blocked | Regenerate the work-unit or individual preview and obtain immediate explicit approval | requested_intent is create, update, disable, delete, or copy | |

## Dependency-Aware Validation

| Task Code | Task Name | Applies When | Result | Next Action | Resolver |
|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Deep mode and AlertType is supplied | Verify the code exists in ORA_HRC_ALERT_TYPE | Resolve the target-environment lookup before preview | resolve_alert_type_code |
| CUSTOM_ALERTS | Alerts | Deep mode and AlertAccessLevel is supplied | Verify the code exists in ORA_HRC_ALERT_ACCESS_LEVEL | Resolve the target-environment lookup before preview | resolve_alert_access_level |
| CUSTOM_ALERTS | Alerts | Existing-item operation uses AlertCode | Require exactly one matching AlertId | Stop on zero or multiple matches | find_event_alert_by_code |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Contract and validation mode are supported | Require 0.11.0; validation_mode defaults to simple and accepts only simple or deep, independently of sequential or batch-create | Always | |
| CUSTOM_ALERTS | Alerts | Simple CREATE validation is local | Require mandatory values, valid hierarchy, supported operations, basic types, unique workbook keys and payload shape; retain cheap known local length checks, but leave business value validity to Fusion | validation_mode is simple and intent is CREATE | |
| CUSTOM_ALERTS | Alerts | Batch-create input is bounded | Require all included rows to be CREATE, exact parent relationships, unique codes within parent scope, TemplateCode and RecipientCode at most 32 characters, and no file-based Body | execution mode is batch-create | |
| CUSTOM_ALERTS | Alerts | Batch approval document is immutable | One entire-workbook unit binds source digest, environment, mode, POST root URI, exact version-4 batch headers, ordered parts, nested payloads and verification policy; any change invalidates approval | execution mode is batch-create | |
| CUSTOM_ALERTS | Alerts | Requested intent is supported | Accept plan, inspect, verify, preview, create, update, disable, delete, or copy; reject upsert and process | Always | |
| CUSTOM_ALERTS | Alerts | Name length is at most 80 characters | Reject an overlength value before preview | Name is supplied | |
| CUSTOM_ALERTS | Alerts | Description length is at most 2000 characters | Reject an overlength value before preview | Description is supplied | |
| CUSTOM_ALERTS | Alerts | Server-managed fields are absent | Reject AlertId on create and reject audit fields in every write body | A mutation body is proposed | |
| CUSTOM_ALERTS | Alerts | Boolean decisions are explicit | Require EnabledFlag and TestModeFlag as true or false; do not inherit endpoint defaults | requested_intent is create | |
| CUSTOM_ALERTS | Alerts | Recipient fields match local shape | Require RecipientCode at most 32 characters, ChannelType at most 30 characters, and ValueExpression at most 2,000 characters | a Template Recipient is supplied | |
| CUSTOM_ALERTS | Alerts | Mutation payload is immutable | Recompute the digest and invalidate approval after any payload, URI, method, or environment change | A preview exists | |
| CUSTOM_ALERTS | Alerts | Work-unit approval document is immutable | Recompute the aggregate digest and invalidate approval after any validation mode/policy, source digest, environment, operation order, method, URI, payload, effect, verification contract, or execution policy change | An Alert hierarchy create work unit exists | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | ALERT.VALIDATE | decision | 1 | validate_input | valid->ALERT.LOOKUP;invalid->ALERT.RETURN_ISSUES | none | stop | Always |
