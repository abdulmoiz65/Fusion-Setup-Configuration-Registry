# Defaulting Rules

## Default Rules

| Business Value | Default Value | Applies When | Can User Override? | Why This Default Is Safe |
|---|---|---|---|---|
| InactiveFlag | N | The user does not supply a status | Yes | New overhead cost element groups are active unless the user explicitly requests inactive or disabled status |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OCEG.DEFAULT_INACTIVE_FLAG | step | 50 | apply_default | defaulted->OCEG.ENFORCE_CREATE_DESIGN;unchanged->OCEG.ENFORCE_CREATE_DESIGN | OCEG.RESOLVE_COST_ELEMENTS_FOR_CREATE | stop | Create |
