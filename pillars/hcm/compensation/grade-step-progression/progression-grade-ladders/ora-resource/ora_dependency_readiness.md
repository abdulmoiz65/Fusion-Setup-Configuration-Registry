# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered `ProgressionGradeLadder` business object | Resolve the exact registered Data Loader business object. |
| 2 | Current schema | Retrieve root and child-component attribute metadata. |
| 3 | Parent ladder dependencies | Validate lookup and reference-backed parent fields that are supplied. |
| 4 | Grade membership dependencies | Validate the parent ladder and grade references for supplied grade rows. |
| 5 | Step-rate dependencies | Validate the parent ladder and legislative data group references for supplied rate rows. |
| 6 | Step-rate-value dependencies | Validate supplied rate, grade step, and legislative data group references. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| progression_grade_ladder_registered_bo | Registered `ProgressionGradeLadder` business object | Yes | Every request | Lookup | Fusion Data Loader registered-BO metadata | resolve_progression_grade_ladder_business_object | Establishes the exact supported loader object | Do not substitute a similarly named object | BusinessObject: `ProgressionGradeLadder` |
| progression_grade_ladder_schema | Current root and child schema | Yes | A request contains configuration values | Lookup | Fusion Data Loader detail, component, and attribute metadata | read_progression_grade_ladder_schema | Defines valid fields and dependencies | Wait for readable current metadata before processing values | Validated field contract |
| parent_lookup_values | Parent lookup-backed fields | Conditional | The corresponding parent fields are supplied | Verify | `ORA_CMP_GSP_GRADE_LADDER_GRP`, `ORA_CMP_GSP_AUTO_APPROVE`, `ORA_CMP_GSP_PROG_STYLE`, `ORA_CMP_GSP_PROG_DT`, `GRADE_TYPE`, `YES_NO`, `ORA_CMP_GSP_RATE_SYNC_DT`, `ORA_CMP_GSP_SALARY_ADJ_TYPE`, `ORA_CMP_GSP_SAL_CALC_METH`, `ORA_CMP_GSP_SAL_CHG_DT`, and `ACTIVE_INACTIVE` declared by live metadata | read_progression_grade_ladder_schema | Loader metadata declares these fields as lookup-backed | Provide a value valid for the named lookup; do not infer a default | Supplied parent lookup values |
| parent_reference_values | Parent foreign references | Conditional | The corresponding parent fields are supplied | Verify | `Actions`, `ActionReasons`, `Formula`, and `LegislativeDataGroups` declared by live metadata | read_progression_grade_ladder_schema | Loader metadata declares foreign-object references and user keys | Provide the declared associated user-key values | Supplied parent reference values |
| grade_membership_references | Grade membership references | Conditional | A grade membership row is supplied | Verify | `GradeLadder` and `Grade` declared by live metadata | read_progression_grade_ladder_schema | Child rows depend on ladder and grade identity | Provide `GradeLadderName`, `GradeCode`, and `GradeSetCode` where required by the user-key contract | Supplied grade membership reference values |
| step_rate_dependencies | Step-rate lookups and references | Conditional | A step-rate row is supplied | Verify | `CMP_SALARY_BASIS`, `GRADE_PAY_RATE_TYPE`, `ACTIVE_INACTIVE`, `GradeLadder`, and `LegislativeDataGroups` declared by live metadata | read_progression_grade_ladder_schema | Rate rows are metadata-linked to these dependencies | Provide fields valid for the declared lookup and reference contracts | Supplied step-rate dependency values |
| step_rate_value_dependencies | Step-rate-value references | Conditional | A step-rate-value row is supplied | Verify | `Rate`, `GradeStep`, and `LegislativeDataGroups` declared by live metadata | read_progression_grade_ladder_schema | Value rows depend on rate, grade step, and LDG identity | Provide the declared associated user-key values | Supplied step-rate-value dependency values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PGL.CHECK_DEPENDENCIES | decision | 40 | resolve_dependency | ready->PGL.ROUTE;blocked->PGL.HANDLE_ISSUE | PGL.VALIDATE_INPUT | stop | After supplied values pass schema validation |
