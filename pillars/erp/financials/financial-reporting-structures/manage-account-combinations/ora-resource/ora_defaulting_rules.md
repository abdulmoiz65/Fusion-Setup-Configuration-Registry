# Manage Account Combinations Defaulting Rules

Defaults are applied before final CSV validation and never replace a supplied valid value.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Chart of Accounts Code | Resolved StructureInstanceCode | COA Name or natural-language COA identifier is supplied and exactly one enabled structure instance resolves | No | resolve_chart_of_accounts_from_candidate |
| Import Group Identifier | Local current date and time in yyyyMMddHHmmss format | Position 38 is omitted, including natural-language input; do not ask the user for it | No |  |
| End-of-record indicator | END | Position 62 is omitted while creating a new CSV from natural language | No |  |
| Enabled | Blank | User does not provide position 2 | No |  |
| Allow Posting | Blank | User does not provide position 33 | No |  |
| Segment positions beyond supplied natural-language vector | Blank through position 32 | Fewer than 30 segment values are supplied | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAC-040-APPLY-DEFAULTS | step | 40 | apply_default | defaulted->MAC-050-ENFORCE-DESIGN | MAC-030-RESOLVE-DEPENDENCIES | stop | Dependencies are ready |
