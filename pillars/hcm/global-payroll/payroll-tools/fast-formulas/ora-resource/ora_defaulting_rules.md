# Fast Formulas Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveEndDate | End of time | EffectiveEndDate is blank | No; preserve any explicitly supplied valid end date | |
| FormulaCode | Exact FormulaName value, preserving case, spacing, punctuation, and all other supplied characters | FormulaCode is absent during FastFormula DAT preparation; if explicitly supplied, validate that it equals FormulaName | No; reject a supplied FormulaCode that differs from FormulaName | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FF.APPLY_DEFAULTS | decision | 4 | apply_default | applied->FF.ENFORCE_DESIGN;skipped->FF.ENFORCE_DESIGN;invalid->FF.HANDLE_ERROR | FF.RESOLVE_REFERENCES | stop | EffectiveEndDate is blank or explicitly supplied |

## Sources

- Developer-provided /scratch/share/FastFormulasExport.xls, accessed 2026-08-17.
- Developer-provided Fast Formula name-to-code derivation instructions, received 2026-08-17.
