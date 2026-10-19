# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Expense pool type | For Create, DELETE with a supplied ExpensePoolTypeCode, or a PATCH that supplies ExpensePoolTypeCode, retrieve the fixed expense-pool lookup type and resolve one exact normalized Meaning to its returned LookupCode. |
| 2 | Reference data set | For Create or DELETE with a supplied SetName, use the verified case-insensitive SetName candidate query and resolve its returned SetId after local normalized verification. The set is immutable after Create and must not be supplied for PATCH. |
| 3 | Existing delete target | For DELETE, resolve exactly one current Expense Pool from ExpensePoolCode and any resolved optional qualifiers in the approved task-export baseline. |
| 4 | Payload readiness | For Create, construct the final payload only after both dependency resolutions succeed. For DELETE, use only the verified ExpensePoolCode and generated RestAction=DELETE. For PATCH, include only supplied, validated, or resolved fields. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| expense_pool_type | Expense pool type lookup | Yes | Create; PATCH when ExpensePoolTypeCode is supplied | Lookup | User-supplied ExpensePoolTypeCode meaning | resolve_expense_pool_type | The Create payload must store the LookupCode returned for the exact normalized Meaning; PATCH resolves it only when supplied. | Provide one valid expense pool type meaning when creating or changing the type. | ExpensePoolTypeCode from LookupCode |
| reference_data_set | Reference data set | Yes for Create; optional for DELETE | Create; DELETE when SetName is supplied | Lookup | User-supplied SetName | resolve_reference_set | The Create payload must contain the SetId returned for SetName; DELETE resolves it only when supplied as a target qualifier. Never accept user-supplied SetId or SetCode. | Provide one valid set name when creating or disambiguating a delete. The set is immutable after Create. | SetId from SetId |
| delete_target | Existing Expense Pool | Yes | DELETE | Verify | ExpensePoolCode and optional resolved SetId and LookupCode qualifiers | resolve_delete_target | Delete requires exactly one existing target. Optional qualifiers constrain identity only; Fusion remains authoritative for referential-integrity rejection. | Provide a supported qualifier when the code does not identify one target. | Verified ExpensePoolCode for the delete source |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Both resolvers return exactly one eligible value | Continue to payload-readiness enforcement; do not create through this resource. |
| Lookup | A supplied type or set selector requires resolution | Read-only lookup only. |
| Blocked | A resolver has no exact match, more than one match, an invalid response, or unavailable access | No. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OEP.RESOLVE_DEPENDENCIES | step | 2 | resolve_dependency | ready->OEP.RESOLVE_EXPENSE_POOL_TYPE;blocked->OEP.HANDLE_ISSUE | OEP.VALIDATE_INPUT | stop | Input validation, including explicit InactiveFlag validation when required, passed; DELETE resolves supplied qualifiers before target identity |
