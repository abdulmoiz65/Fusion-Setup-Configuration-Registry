# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| FSM import package | An import package containing the task CSV files | Block import | Provide the FSM import package to validate | Before importing Manage Planning Source Systems setup data |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An FSM import package is supplied | Validate the package before evaluating source-system CSV changes | Continue to retained-baseline resolution |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Import package is present | Block when no FSM import package is available for validation | Before importing task setup data |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSCPS.VALIDATE_PACKAGE | step | 1 | validate_input | valid->MSCPS.DEPENDENCIES;invalid->MSCPS.BLOCKED;failure->MSCPS.FAILED | none | stop | Before importing Manage Planning Source Systems setup data |
