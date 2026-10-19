# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| jobDefinitionId | JobDefinition://oracle/apps/ess/projects/foundation/setup/system/OrgDenormJob | Every request | No; reject conflicting value | |
| application | FscmEss | Every request | No; reject conflicting value | |
| product | PJF | Every request | No; reject conflicting value | |
| requestParameters | Omitted | Every request | No; reject any supplied value | |
| operation | resume | requestId supplied and operation omitted | No; never submit with an existing ID | |
| operation | submit | No requestId and operation omitted | No automatic execution; require approval | |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.APPLY_DEFAULTS | step | 2 | apply_default | applied->MPO.TRACK_EXISTING_REQUEST;failure->MPO.RETURN_ISSUES | MPO.VALIDATE_INPUT | stop | Valid task input |
