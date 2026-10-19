# Input Validation

## Supplied CSV pass-through import

When a CSV is supplied for import, its data content is opaque. Do not open or
parse a data CSV, inspect its header or rows, compare it with a sample/template,
or apply field, lookup, identity, parent, operation, duplicate, or volume rules.
Do not add, drop, rename, reorder, normalize, or rewrite columns or values.

The CSV may have any number of columns in any order. It may have more columns
than the bundled sample, fewer columns, different columns, or no sample match.
Missing or unfamiliar columns are not local validation failures. Never require
`PartyUsageCode` and never request a waiver for it. Fusion Import Management is
responsible for evaluating the data after submission.

The only allowed local checks for a supplied direct-CX group are:

- every source path exists and is a regular, nonempty `.csv` file;
- filenames are transport-safe and basenames are unique case-insensitively;
- there is at most one authoritative CX mapping CSV and at least one data CSV;
- an exact CX Import Management object code is supplied or derived from the mapping CSV;
- an exact job-level `ImportMode` is supplied separately as `CREATE_ONLY`, `CREATE_RECORD`, or `DELETE_RECORD`; it must not be inferred from CSV content;
- the target supports that exact object code, its UCM account is resolved, and the exact ordered filenames and bytes produce the approved group SHA-256;
- the current approval and Task Hook envelope cover that exact group, object, mode, environment, UCM account, activity name, and mode-aware execution adapter.

Mapping-file signature and `IMPORT OBJECT` checks apply only to the optional
mapping CSV; they do not authorize inspection of data CSV columns or rows.

For an explicit supplied `Hierarchy` or `HierarchyNode` delete, apply the same
opaque pass-through contract. Do not inspect PartyId, PartyNumber, parent
identity, AsOfDate, identifier-only shape, or pre-delete matches. Fusion Import
Management evaluates the unchanged row data after submission.

## Generation or explicit data validation

Only when the user asks to generate a CSV or explicitly asks to validate its
data, apply `references/object-profiles.json`, `references/column-contracts.json`,
`references/field-contracts.json`, and `scripts/prepare_tca_import_csv.py`.
Those contracts must never block pass-through import of a supplied CSV.
For a generated or explicitly validated Linked Party file, resolve a
`fusion-runtime` LinkType contract and pass it through `--target-values-json`.

For Hierarchy and Hierarchy Member, accept `create`, `update` (normalized to
`create-or-update`), and `delete`. Require high-volume mode. Delete accepts only
one complete exact identity set and is always destructive. A live delete also
requires exact pre-delete target resolution and current target-specific
`DELETE_RECORD` capability evidence.

For Additional Identifier generation or explicit validation, accept `delete`
only when every row contains one nonblank `PartyIdentifierId` and no other
populated fields. Treat the operation as destructive and require the exact
selected party parent for pre-delete and post-delete verification.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCA.VALIDATE | step | 1 | validate_input | valid->TCA.DEFAULTS;invalid->TCA.RETURN_ISSUES |  | stop | Validate transport/routing only for supplied CSVs; validate data only for generation or an explicit validation request. |
