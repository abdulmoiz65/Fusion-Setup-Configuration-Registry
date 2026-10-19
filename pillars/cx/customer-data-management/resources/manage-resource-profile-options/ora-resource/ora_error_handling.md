# Manage Resource Profile Options Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A profile option, level, or scope cannot be resolved | Stop before preview and identify the unresolved target |
| SqlValidation cannot be parsed into one supported lookup type | Stop before preview and report the unresolved validation contract |
| The requested code is missing, disabled, not yet active, or end-dated | Stop before preview and request an enabled effective code |
| A read-only lookup returns authentication or authorization failure | Stop and report the access failure; do not infer a value or retry a write |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required profile-value identity or requested value is missing | Supply the missing target facts |
| Profile resolution | The definition, level, or scope does not resolve exactly | Correct the target profile value |
| Validation contract | SqlValidation does not yield one supported lookup type | Obtain a supported validation contract before import |
| Lookup validation | Requested code is not enabled and effective | Select an enabled effective code |
| Authorization or privilege | Fusion denies a required read-only lookup | Obtain the required access and retry the read only |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview blocked | The affected profile option, requested value, blocking validation, and safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| SqlValidation does not yield one exact supported lookup type | Do not infer a lookup type or submit the import |
| Requested code fails lookup validation | Do not substitute another value or submit the import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.RETURN_ISSUES | terminal | 7 | terminal | none | none | stop | Input, profile, level, lookup, or design validation fails |
| RPO.RETURN_SUCCESS | terminal | 8 | terminal | none | RPO.ENFORCE_VALUE | stop | Every changed profile value passes validation |
