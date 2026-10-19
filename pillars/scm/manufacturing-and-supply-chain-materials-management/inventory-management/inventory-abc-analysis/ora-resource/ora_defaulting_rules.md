# Inventory ABC Analysis Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| Redwood ABC Classes CollectionToolbarSpPrimaryActionChain | On opening a new ABC Class drawer, sets EnableDate to the current ISO date |
| User approval | Author the ABC Class EnableDate behavior as a local default |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| abcClasses.EnableDate | Current ISO date in YYYY-MM-DD format | Creating an ABC Class and EnableDate is blank | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABC.APPLY_DEFAULT | step | 20 | apply_default | applied->ABC.CHECK_READINESS;skipped->ABC.CHECK_READINESS | ABC.VALIDATE_INPUT | stop | Before Data Loader preparation, when creating abcClasses with blank EnableDate |
