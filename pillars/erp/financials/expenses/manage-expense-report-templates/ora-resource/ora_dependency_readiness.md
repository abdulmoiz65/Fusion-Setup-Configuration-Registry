# Manage Expense Report Templates Dependency Readiness

## Required Dependency Order

1. Require the current operation-free workbook and parse parent and row identities.
2. Report missing/invalid values, offer updated workbook or chat corrections,
   and validate one chat answer or complete workbook version at a time.
3. Resolve local input and route support. Prepare preservation/execution
   contracts as internal evidence without separate confirmation gates.
4. At the declared preparation step, preflight target, catalog, privileges,
   paths, and output ownership, then obtain the fresh task export.
5. Resolve live identities, target-derived create/update operations, codes, and task headers; build the exact candidate.
   Persist and verify Data Loader preflight before Task Hook validation; bind
   the review files and retained preview to that same final immutable artifact.
6. Obtain one current approval for the final candidate before submission.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| EXMERT.INTAKE | Complete intended changes and preserved values | Yes | Every request | Satisfied | Current workbook supplemented by updated workbook or one-at-a-time chat | | Avoids repeated collection or unselected defaults | Correct only unresolved issues | Scope; identities; base values; medium; issues |
| EXMERT.TABLE_CONSTRAINTS | Storage constraints and user-facing values | Yes | Every request | Satisfied | Current documented storage rules and ora_input_validation.md | | Prevents malformed values | Supply business values, not internal IDs | Validated types, lengths, dates, numbers |
| EXMERT.TASK_ROUTE | Supported candidate builder and task CSV schema | Yes | Preparation | Satisfied | build_import_candidate.py and later fresh task export | | Workbook fields do not imply importer support | Resolve unsupported requested fields before packaging | Exact supported columns and references |
| EXMERT.VALUE_PROVIDERS | Every required value has a provider | Yes | Preparation | Satisfied | Implementor for business values; baseline for preserved edits; Fusion/importer for IDs and WHO data | | Prevents fabricated internal values | Provide only missing functional values | Provider per required field |
| EXMERT.BASELINE | Fresh same-environment preservation source | Yes | Before candidate build | Satisfied | Shared task-level export at the declared preparation step | export_preservation_baseline | Protects unrelated rows and verifies identities | Correct duplicate create or ambiguous edit identities | ProcessId; checksum; inventory; match evidence |
| EXMERT.IMPORT | Validated exact artifact and approval | Yes | Before submission | Satisfied | Core Data Loader persisted preflight and Task Hook | | Prevents approval of a different package | Review CSV files and approve the displayed change | Preflight; preview; checksum; task envelope; approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMERT.RESOLVE_DEPENDENCIES | step | 7 | resolve_dependency | ready->EXMERT.EXPORT_BASELINE;missing->EXMERT.NEEDS_CORRECTION | EXMERT.COMPLETE_INPUT | stop | Local intake is complete; establish providers, route support, and preparation preflight |
