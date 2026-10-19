# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| BPA attributes | Existing All Business Units defaults when no specific-BU override exists | BPA is created from external purchase prices | TBD | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPPAD.APPLY_DEFAULTS | step | 3 | apply_default | applied->EPPPAD.ENFORCE_DESIGN;blocked->EPPPAD.HANDLE_ISSUES | EPPPAD.CHECK_DEPENDENCIES | stop | Every validated request |
