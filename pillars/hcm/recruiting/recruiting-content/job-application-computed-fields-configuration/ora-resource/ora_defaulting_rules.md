# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| FlexfieldCode | PER_PERSON_EIT_EFF | EFF discovery | No | |
| Category | PER_EIT | EFF discovery | No | |
| Usage | PER_PERSON_EIT_EFF | EFF discovery | No | |
| FormulaBaseFormulaTypeName | IRC_JA_COMPUTED_FIELD | Every CSV mapping row | No | |
| Legislative Data Group filter | Global | Formula listing is requested without a Legislative Data Group | No | resolve_fast_formula_details |
| Formula Text handling | Discard and never display or persist | Every delegated formula response | No | |
| Mapping summary | One row per Context, Segment, Formula, Base formula name | Review and preview | No | |
| New mapping display | Show the proposed mapping without a Create badge | New mapping preview | No | |
| End-to-end implementation | Continue through discovery, validation, fresh export, clean-target handling, immutable ZIP assembly, Task Hook preview, approval, one submission, and verification | Implement, add, or configure mapping request | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JACF.FORMAT_REVIEW | step | 4 | apply_default | complete->JACF.DONE_REVIEW | none | stop | Context, segment, or eligible-formula review is ready |
