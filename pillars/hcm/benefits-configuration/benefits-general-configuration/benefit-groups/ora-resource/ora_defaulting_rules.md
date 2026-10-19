# Benefit Groups Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Operation | Create | The user asks to generate a new Benefit Groups HDL sample and supplies no operation | No | |
| RestAction | POST | The operation is Create and RestAction is unset in a generated HDL artifact | No | |
| Read behavior | Read/verify only | The user asks to inspect metadata or load status without requesting a mutation | No | |
| Business object | benefitGroups | Every request | No; Benefit Groups is the task display name | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_GRP.APPLY_DEFAULTS | step | 20 | apply_default | applied->BEN_GRP.CHECK_READINESS | BEN_GRP.VALIDATE_REQUEST | stop | Apply only the documented operation and business-object defaults |
