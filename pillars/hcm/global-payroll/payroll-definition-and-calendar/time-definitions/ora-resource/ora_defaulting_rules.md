# Payroll Time Definition Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Local task context | Create artifacts/shared/runbook/current/task-context.json with one exact Time Definitions catalog row and a positive project-unique sequence | The file is absent and the active project, effective catalog task, and nested skill are known and consistent | No | bootstrap_task_context |
| TimeDefinitionId | Omit | Parent create or natural-key parent or child operation | No |  |
| TimeDefinitionUsageId | Omit | Usage assignment or removal | No |  |
| GUID | Omit | Create or usage assignment | No |  |
| Parent delete key fields | Resolved parent ShortName as TimeDefinitionCode and LegislativeDataGroupName only | Parent delete after code or DefinitionName resolution | No | resolve_payroll_time_definition |
| Usage child key fields | Resolved parent ShortName as TimeDefinitionCode, LegislativeDataGroupName, and UsageType only | Usage assignment or removal after parent code or DefinitionName resolution | No | resolve_payroll_time_definition |
| Usage export display-name projection | Retain joined parent ShortName as TimeDefinitionCode and disclose the projection warning | The unqualified usage export TimeDefinitionCode equals the same joined parent DefinitionName | No | resolve_payroll_time_definition |
| Export-lag usage child key fields | Matching TimeDefinitionCode, LegislativeDataGroupName, and UsageType from a qualified successful immutable DAT | A usable fresh export has zero candidates immediately after a create and successful terminal evidence or authenticated exact read-back is verified | No | resolve_recent_successful_payroll_time_definition |
| SourceSystemOwner and SourceSystemId | Omit both | Either source-system field is absent | No |  |
| Date format | YYYY/MM/DD | A validated date is emitted into PayrollTimeDefinition.dat | No |  |
| Parent definition-type attributes | No inferred business value | A type-dependent field is absent or unfamiliar | No |  |
| UsageType | No default and no code substitution | A usage child is requested | No |  |

Defaults never translate a user-supplied business value to an export encoding, existing-row value, documented example, or local allowlist entry. In particular, preserve the trimmed user-supplied UsageType meaning and do not replace it with UsageTypeCode. The local task-context default is reversible preflight state and requires no separate mutation approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TD.BOOTSTRAP_CONTEXT | step | 20 | apply_default | resolved->TD.LOOKUP_LDG;blocked->TD.ERROR_HANDLE | TD.VALIDATE_INPUT | stop | Resolve a matching task context or bootstrap and schema-validate the missing local context before Fusion preflights |
