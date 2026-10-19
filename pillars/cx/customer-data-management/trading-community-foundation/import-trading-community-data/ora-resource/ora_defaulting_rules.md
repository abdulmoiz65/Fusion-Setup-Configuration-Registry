# Defaulting Rules

## Supplied CSV pass-through import

Do not derive or default any value from supplied data columns or rows. Preserve
the CSV exactly as supplied. Select the job-level `ImportMode` only from
explicit user intent or an already reviewed workflow artifact; it is routing
metadata and must not be inferred from CSV content.

| Value | Default | Rule |
|---|---|---|
| Import object | None | Use explicit user context or authoritative mapping metadata; otherwise ask for the exact CX Business Object code. |
| Import mode | None | Require exactly one of `CREATE_ONLY`, `CREATE_RECORD`, or `DELETE_RECORD`; never rely on Oracle's implicit `CREATE_RECORD` default. |
| UCM account | Exact current object-metadata value | Resolve it from the selected target; reject caller overrides. |
| Activate | `YES` in the reviewed initiation payload | This transport setting does not grant execution approval or validate CSV data. |
| Schedule | `ONE_TIME_IMMEDIATE` | Change only through a newly reviewed preview. |
| Execution | Preview only | Upload/initiate only after exact-group approval. |

For CSV generation or explicit data validation, map the selected operation to
the same explicit job-level mode: `create` to `CREATE_ONLY`,
`update` or `create-or-update` to `CREATE_RECORD`, and `delete` to
`DELETE_RECORD`. The
selected object profile may default volume, parent, or semantic destructive
handling before the generated artifact is frozen.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCA.DEFAULTS | step | 2 | apply_default | applied->TCA.DEPENDENCIES;failure->TCA.RETURN_ISSUES | TCA.VALIDATE | stop | Apply transport defaults only for supplied CSVs; apply profile defaults only for generation or explicit validation. |
