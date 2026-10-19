# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| DataSecurityObjectCode | WORK_DEFINITION | The user provides an explicit enable or disable instruction | No | |
| DataSecurityEnabledFlag | Y | The user provides an explicit enable instruction | No | |
| DataSecurityEnabledFlag | N | The user provides an explicit disable instruction | No | |
| RestAction | PATCH | Every supported update row | No | |

## Defaulting Rules

| Situation | What Happens |
|---|---|
| The user provides an explicit enable instruction | Set DataSecurityObjectCode to WORK_DEFINITION, DataSecurityEnabledFlag to Y, and RestAction to PATCH in the Data Loader workbook before validation. |
| The user provides an explicit disable instruction | Set DataSecurityObjectCode to WORK_DEFINITION, DataSecurityEnabledFlag to N, and RestAction to PATCH in the Data Loader workbook before validation. |
| DataSecurityObjectCode or DataSecurityEnabledFlag is absent without an explicit enable or disable instruction | Stop in input validation; do not infer a state or object code. |
| DataSecurityObjectName is absent | Preserve the validated workbook layout and stop only when the live schema requires a value; do not synthesize a new column. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEC.DEFAULT | step | 2 | apply_default | ok->SEC.DEPENDENCIES;failure->SEC.FAILED | SEC.VALIDATE | stop | An explicit enable or disable instruction is supplied |
