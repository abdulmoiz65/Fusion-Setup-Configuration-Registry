# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Registered Salary Range Differential business object | BusinessObject: SalaryRangeDifferential | Stop | Resolve the exact registered business object; do not substitute a similarly named object | Every request | resolve_salary_range_differential_business_object |
| Current Salary Range Differential field contract | One or more supplied fields present in the current SalaryRangeDifferential template and attribute metadata | Stop | Read the current schema and submit only fields whose names and values conform to it | A validation, preview, import, create, or update request supplies configuration values | read_salary_range_differential_schema |
| Parent differential identity | Name for a new SalaryRangeDifferential record; EffectiveStartDate when required by the selected operation | Stop | Provide the missing value in the source data; do not infer identifiers or dates | A new parent Salary Range Differential record is prepared | read_salary_range_differential_schema |
| Differential value | Differential for a new SalaryRangeDifferentialValue record; EffectiveStartDate and parent reference when required by the selected operation | Stop | Provide the missing value and valid parent relationship in the source data | A new Salary Range Differential Value record is prepared | read_salary_range_differential_schema |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The registered business object has not resolved | Blocked | Stop before preview or import preparation | resolve_salary_range_differential_business_object |
| The current schema has not been read | Blocked | Stop before preview or import preparation | read_salary_range_differential_schema |
| A supplied field is absent from the current schema or violates its data type, length, mandatory, lookup, or reference contract | Blocked | Correct the source data and revalidate | read_salary_range_differential_schema |
| Every supplied field conforms to the current schema | Continue | Continue only through the task's established export/import workflow | read_salary_range_differential_schema |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact field identity | Accept only fields returned by the current SalaryRangeDifferential template and attribute metadata | Every supplied value | read_salary_range_differential_schema |
| Field shape | Validate supplied values against current data type, data length, number precision, mandatory status, lookup, and reference metadata | Every supplied value | read_salary_range_differential_schema |
| Parent section fields | Validate RangeDiffId, EffectiveStartDate, EffectiveEndDate, Code, Name, Criteria, LegislativeDataGroupId, LegislativeDataGroupName, Status, AddressType1, AddressType2, AddressType3, ProcessWfhFlag, GeographyTypeId, GeographyTypeName, and RangeDiffType only when supplied | A SalaryRangeDifferential parent row is supplied | read_salary_range_differential_schema |
| Child value section fields | Validate RangeDiffValueId, EffectiveStartDate, EffectiveEndDate, RangeDiffId, RangeDiffCode, LocationId, LocationCode, LocationSetCode, BusinessUnitShortCode, Differential, AnnualizationFactor, Frequency, GeographyId, GeographyName, GeographyZoneType, GradeRateId, GradeRateName, GradeRateMinimumLimit, Criteria, and LegislativeDataGroupName only when supplied | A SalaryRangeDifferentialValue child row is supplied | read_salary_range_differential_schema |
| Lookup-backed parent fields | Validate Criteria against ORA_CMP_RANGE_DIFF_CRITERIA, RangeDiffType against ORA_CMP_RANGE_DIFF_TYPE, AddressType1 through AddressType3 against ADDRESS_TYPE, and Status against ACTIVE_INACTIVE when supplied and current metadata retains those lookup contracts | A supplied parent field has a live lookup contract | read_salary_range_differential_schema |
| Parent-child reference | Validate SalaryRangeDifferentialValue.RangeDiffId against the current SalaryRangeDifferential reference contract | A child value row is supplied | read_salary_range_differential_schema |
| Unavailable live schema | Do not infer Salary Range Differential fields from an older archive, cached output, or a similarly named business object | The schema resolver does not produce matching current metadata | read_salary_range_differential_schema |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SRD.VALIDATE_INPUT | step | 30 | validate_input | valid->SRD.COMPLETE;invalid->SRD.HANDLE_ISSUE | SRD.READ_SCHEMA | stop | After the registered business object and current schema resolve |
