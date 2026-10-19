# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Compensation History business object | Resolve the exact compensationHistoryElements Data Loader business object. |
| 2 | Current Compensation History schema | Read the matching current template and attribute metadata before validating supplied fields. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| compensation_history_business_object | Registered Compensation History business object | Yes | Every request | Lookup | Fusion Data Loader registered-business-object metadata | resolve_compensation_history_business_object | The task's metadata source identifies compensationHistoryElements as the only matching registered object | Do not substitute a similarly named business object | BusinessObject: compensationHistoryElements |
| compensation_history_schema | Current Compensation History element schema | Yes | A request includes data to validate, preview, import, create, or update | Lookup | Fusion Data Loader template and attribute metadata | read_compensation_history_elements_schema | The live schema is the authority for current fields, types, lengths, mandatory flags, and dependencies | Correct source data to match the current schema | Validated section and field contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Exactly one registered business object and matching current schema are available | Lookup only |
| Blocked | The object is absent, ambiguous, unreadable, or schema validation fails | No |

