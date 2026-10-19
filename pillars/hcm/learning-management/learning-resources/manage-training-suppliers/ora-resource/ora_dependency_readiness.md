# Manage Training Suppliers Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Contact person | Resolve uniquely when supplied; otherwise allow correction or removal |
| 2 | Existing suppliers | Read same-name tenant records and obtain the user's intent when matches exist |
| 3 | Tenant configuration | Resolve required flexfields and an accessible immutable Set when enabled |
| 4 | Execution route | Record the user's REST upload or Data Loader choice before proposal approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| TS.CONTACT | Accessible HCM person | No | Contact is supplied | Lookup or Blocked | User-provided person identifier | resolve_contact_person | Prevents linking the wrong person | Select one match, correct the value, or remove the optional contact | contactPersonId, contactPersonDisplayName |
| TS.EXISTING | Existing training suppliers | Yes | Before every create proposal | Lookup | User-provided supplier name | inspect_existing_training_suppliers | Names are not guaranteed unique | Choose an existing record or explicitly create another same-name supplier | Existing identifiers and statuses |
| TS.CONFIG | Set and configured flexfields | Conditional | Tenant configuration requires them | Lookup or Blocked | Tenant configuration and user values | validate_required_supplier_configuration | Required tenant values must be valid and accessible | Supply the required Set or segment values | Set and flexfield values |
| TS.ROUTE | Creation route | Yes | Before every create proposal | User selection or Blocked | Explicit user choice |  | The approved execution channel must not be inferred or changed silently | Choose REST upload or Data Loader | execution_route_choice |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency is resolved | Yes |
| Selection required | Multiple people or existing same-name suppliers need user intent | Lookup yes; create no |
| Blocked | A required tenant value is missing or invalid | Lookup yes; create no |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->TS.ENFORCE_DESIGN;selection_required->TS.BLOCKED;blocked->TS.BLOCKED;failure->TS.FAILED | TS.RESOLVE_REFERENCES | stop | After applicable reference lookups complete |
