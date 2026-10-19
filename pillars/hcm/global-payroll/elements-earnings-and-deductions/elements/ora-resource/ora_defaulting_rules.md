# Elements Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SecondaryClassificationName | empty | User omits optional secondary classification. | No; preserve an explicitly supplied valid value. | |

No default is documented for Category, ElementStartDate, ElementName, currency, or any questionnaire response. The example response values in the local catalog are display examples, not defaults.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ELE.APPLY_DEFAULTS | step | 2 | apply_default | applied->ELE.CHECK_DEPENDENCIES;unchanged->ELE.CHECK_DEPENDENCIES | ELE.VALIDATE_INPUT | stop | Normalize omitted optional secondary classification to empty without changing a supplied value. |
