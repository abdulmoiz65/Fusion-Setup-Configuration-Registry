# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Salary Range Differential business object | Resolve the exact SalaryRangeDifferential Data Loader business object. |
| 2 | Current Salary Range Differential schema | Read the matching current template and attribute metadata before validating supplied fields. |
| 3 | Parent-child reference | Validate a supplied SalaryRangeDifferentialValue.RangeDiffId against the current SalaryRangeDifferential reference contract. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| salary_range_differential_business_object | Registered Salary Range Differential business object | Yes | Every request | Lookup | Fusion Data Loader registered-business-object metadata | resolve_salary_range_differential_business_object | Live registry metadata identifies SalaryRangeDifferential as the exact object | Do not substitute a similarly named business object | BusinessObject: SalaryRangeDifferential |
| salary_range_differential_schema | Current Salary Range Differential schema | Yes | A request includes data to validate, preview, import, create, or update | Lookup | Fusion Data Loader template and attribute metadata | read_salary_range_differential_schema | The live schema is the authority for current fields, types, lengths, mandatory flags, and dependencies | Correct source data to match the current schema | Validated section and field contract |
| salary_range_differential_parent | Parent SalaryRangeDifferential record | Conditional | A SalaryRangeDifferentialValue child record is supplied | Verify | Current SalaryRangeDifferential schema reference metadata | read_salary_range_differential_schema | The child RangeDiffId field references SalaryRangeDifferential | Supply a valid parent relationship in the source data | Validated RangeDiffId reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Exactly one registered business object and matching current schema are available | Lookup only |
| Blocked | The object is absent, ambiguous, unreadable, or schema validation fails | No |
