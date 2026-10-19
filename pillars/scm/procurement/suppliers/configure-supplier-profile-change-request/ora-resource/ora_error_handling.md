# Error Handling

## Data Loader Update Boundary

| Functional Activity | Required Update Route | Required Boundary |
|---|---|---|
| Update profile-change attachment requirements | core.data-loader using the ordered registered business objects | Validate the changed attachment requirement in the prepared Data Loader artifact and obtain explicit approval immediately before import. |
| Update a profile-management entity | core.data-loader using the ordered registered business objects | Validate the selected entity and permitted changed field in the prepared Data Loader artifact and obtain explicit approval immediately before import. |
| Custom action or direct REST update | Not permitted | Do not infer or invoke a custom action, PATCH, PUT, POST, or DELETE operation. |
| No configuration changes are present | No operation | Do not prepare or import a setup-data artifact. |

ADF REST references are read-only lookup guidance only. Use core.data-loader,
the validated Data Loader artifact, and target-specific approval for every update.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Configuration lookup fails | Stop, retain sanitized diagnostic evidence, and resolve the lookup failure before continuing |
| Validation or design enforcement fails | Return the affected scope, entity, and field without applying a configuration change |
| A shared supplierOptions lookup is stale, missing, ambiguous, or conflicts with another task's proposed attribute value | Stop this task, retain the conflict evidence, re-read the singleton after the preceding task completes, and obtain one resolved final value before preparing a new Data Loader artifact |
| A shared supplierEntityConfigurations row is stale, missing, ambiguous, or includes another task's attributes | Stop this task, re-read the entity configuration after the preceding task completes, and prepare a new Data Loader artifact containing only InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode. |
| An approved import reports failure or timeout | Stop before retry, retain the import diagnostics, and require a fresh recovery decision |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Requested scope, entity, or field combination is incomplete or invalid | Correct the input and repeat validation |
| transport or environment | A read-only configuration lookup cannot complete | Resolve environment access before retrying the lookup |
| process failed | An approved import returns failure | Review retained diagnostics and obtain a new recovery decision |
| approval blocker | A live import has no approval bound to its validated artifact and target | Obtain explicit approval before import |
| shared singleton conflict | A shared supplierOptions row is stale, unresolved, or has overlapping task values | Resolve ownership or the final value, then restart the affected task from its read-only lookup |
| shared entity-configuration conflict | A shared supplierEntityConfigurations row is stale, unresolved, or includes attributes owned by Configure Supplier Registration | Re-read the row and restart the affected task with owned attributes only |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import | Target environment, immutable import artifact, intended operation, and approval requirement |
| On failure | Failure class, affected scope, sanitized diagnostics, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup or design validation is incomplete | Do not prepare or apply a configuration update |
| Shared supplierOptions runbook | Do not run this task in parallel with Configure Supplier Registration or Configure Supplier Notifications, do not include another task's unapproved fields in its Data Loader artifact, and do not create, bootstrap, or delete the seeded singleton row |
| Shared supplierEntityConfigurations row | Do not run this task in parallel with Configure Supplier Registration, and do not include RegistrationProspectiveCode or RegistrationSpendAuthorizedCode in its Data Loader artifact. |
| An import outcome is uncertain | Do not retry the import automatically |
| Approval is absent or stale | Do not perform a live import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROFILECHG.COMPLETE | terminal | 50 | terminal | none | PROFILECHG.ENFORCE_SCOPE | stop | The configuration request is compliant |
| RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A lookup, validation, design, or approval issue is encountered |
