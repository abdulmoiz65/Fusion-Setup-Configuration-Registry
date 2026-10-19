# Defaulting Rules

## Source

| Source | Location | Used For |
|---|---|---|
| Developer-provided CONSIGNED valuation structure mode rule | Valuation Structure Type Code CONSIGNED requires Valuation Structure Mode Code AUTO; default AUTO when no mode is specified | Conditional mode-code default and enforcement context |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Valuation Structure Mode Code | AUTO | The resolved Valuation Structure Type Code is CONSIGNED and the user did not specify a Valuation Structure Mode | No | |

## Defaulting Rules

| Situation | What Happens | Applies When | Resolver |
|---|---|---|---|
| A mode is supplied | Preserve the resolved user-supplied Valuation Structure Mode Code for subsequent design enforcement | A Valuation Structure Mode was supplied | |
| No mode is supplied for CONSIGNED | Set Valuation Structure Mode Code to AUTO | The resolved Valuation Structure Type Code is CONSIGNED | |
| No mode is supplied for a non-CONSIGNED type | Block the workflow; no default is defined | The resolved Valuation Structure Type Code is not CONSIGNED | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VS.DEFAULT_CONSIGNED_MODE | decision | 6 | apply_default | defaulted->VS.CHECK_DEPENDENCIES;supplied->VS.CHECK_DEPENDENCIES;blocked->VS.HANDLE_ISSUE | VS.RESOLVE_VALUATION_STRUCTURE_SET | stop | A Valuation Structure Type and optional Mode have been resolved |
