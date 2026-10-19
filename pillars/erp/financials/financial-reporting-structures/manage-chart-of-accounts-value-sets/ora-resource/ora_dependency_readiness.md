# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Read-only value-set metadata | For every requested COA segment, confirm the explicit ValueSetCode or SegmentCode_VS candidate and compare its target definition before FSM export |
| 2 | Data security object metadata | When SecurityEnabledFlag is Y, verify that DataSecurityObjectName identifies an existing object with a nonblank object tag |
| 3 | Table-validation metadata | When ValidationType indicates table validation, verify the supplied table and column metadata before preview |
| 4 | Complete same-task FSM export | Run only when the value set is absent or an explicitly approved update needs package data; export populated CSV data and ASM_SETUP_CSV_METADATA.xml |
| 5 | Template-only FSM export | Use only as a supplement when the complete export needs file-shape clarification |
| 6 | Data Loader import path | Submit the immutable FSM package only through core.data-loader after task validation, preview, and explicit approval |
| 7 | Oracle functional and EDM documentation | Resolve only documented defaults |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_object | Existing Value sets | Yes | Before FSM export, create, or import package for every requested COA segment | Verify | GET valueSets using explicit ValueSetCode or derived SegmentCode_VS candidate | find_value_set | Idempotency and segment-to-value-set traceability | If exactly one matching value set has compatible format and MaximumLength, reuse it; if different, request update-or-new direction; if absent, retain the candidate for creation readiness | Existing definition, ValueSetId, ValueSetCode, format, MaximumLength, and flags |
| secured_value_set_object | Data security object | Conditional | SecurityEnabledFlag is Y | Verify | FND_OBJECTS and qualified value-set security metadata | verify_value_set_security_object | A secured value set requires an existing data security object with a nonblank object tag | Provide DataSecurityObjectName or disable value-set security | DataSecurityObjectName, object existence, object tag |
| table_validation_metadata | Table-validation source metadata | Conditional | ValidationType indicates table validation | Verify | Complete same-task export or approved Fusion value-set metadata | verify_table_validated_value_set_metadata | Table validation requires resolvable source and column metadata | Provide the table-validation source and column fields; provide optional enabled, date, where, and order-by fields only when used | FromClause, ValueColumnName, ValueColumnType, ValueColumnLength, IdColumnName, EnabledFlagColumnName, StartDateColumnName, EndDateColumnName, WhereClause, OrderByClause |
| data_loader_import_path | Data Loader authorization | Yes | Before any live import | Ready | Approved immutable FSM ZIP and core.data-loader task-validation result |  | The FSM ZIP is package evidence only; it must not be submitted through a direct FSM import endpoint | Approve the exact package fingerprint and target environment | Approved source path, checksum, preview, and Data Loader handoff |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Reuse | Exactly one existing value set matches the candidate code, required format, and MaximumLength | Lookup only; do not create a package row |
| Create readiness | No matching value set exists for a validated candidate | Continue automatically with the complete same-task export and package-readiness gates; do not ask for a separate value-set creation confirmation |
| Update decision | A matching code has a differing definition | Lookup only; require an update-or-new decision before package generation |
| Ambiguous | More than one candidate match or the lookup response cannot establish a unique compatible definition | Lookup only; stop and resolve the ambiguity |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAVS.READY | step | 3 | resolve_dependency | ready->COAVS.LOOKUP | COAVS.VALIDATE | stop | Always |
