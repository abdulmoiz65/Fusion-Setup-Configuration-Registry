# Manage Procurement Agents Client-Side Defaulting Rules

## Source Basis

- Oracle Fusion Cloud Procurement 26C Procurement Agents documentation
- Procurement-agent Redwood and UI acceptance-criteria exports supplied by the developer

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Status | Active | A new client-side form has no status value | No | |
| StatusCode | Y | A new client-side form uses Status and has no explicit code | No | |
| Access-level codes | None | The applicable client-side access level is not specified | No | |
| Manage capability flags | false | A new client-side form omits a documented capability flag | No | |
| DFF | No item | The DFF is not enabled or no DFF value is supplied | No | |

## Defaulting Guidance

Apply defaults only to empty create-form values and record the resulting values in the client-side preview. Never replace an explicit user value, silently broaden an access level, infer DFF attributes, or make a network request while applying defaults.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PAG.APPLY_DEFAULTS | step | 20 | apply_default | defaulted->PAG.ENFORCE_CREATE;unchanged->PAG.ENFORCE_CREATE | PAG.VALIDATE_INPUT | stop | A client-side create form has passed required-field validation and any available duplicate check |
