# Manage Job Dependency Readiness

## Purpose

Defines the conditional Job, set, family, subfamily, Grade, benchmark, and Work
Day references used by Manage Job. Dependencies are resolved only when applicable.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Job identity | Resolve the current target or confirm the proposed create identity is available |
| 2 | Delete history | Resolve the retained start and inclusive deletion end against complete Job history for delete-effective-split |
| 3 | Reference-data set | Resolve one exact set when reference-data scope applies |
| 4 | Job Family | Resolve a supplied Job Family in the selected set context |
| 5 | Job Subfamily | Resolve a supplied Job Subfamily after its Job Family context is known |
| 6 | Grade and benchmark Job | Resolve supplied Job Grade and benchmark references |
| 7 | Enterprise Work Day Information | Resolve only omitted working-time values that current metadata marks required or defaultable for create |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| job_identity | Existing Job or create-availability evidence | Conditional | Read, edit, inactivate, delete-effective-split, or create duplicate check | Lookup | Jobs resource | find_manage_job | Prevents an ambiguous target or duplicate create | Provide one exact Job selector | Resolved Job identity and current values |
| job_delete_history | Complete Job history | Conditional | delete-effective-split | Lookup | hcmDateEffectiveObjectHistory | resolve_job_delete_history | Prevents deletion of a logical Job or an unintended history range | Provide the effective start of the last row to retain and the inclusive end date of the last split to remove | Confirmed retained start and deletion end |
| reference_data_set | Reference-data set | Conditional | Create or edit requires reference-data scope | Lookup | Current reference-data set configuration | resolve_job_reference_data_set | Prevents an unsupported or ambiguous set value | Provide one exact set candidate | Confirmed stored set value |
| job_family | Effective Job Family | Conditional | Create or edit supplies a Job Family | Lookup | Job Families resource | resolve_job_family_for_job | Prevents an unresolved or set-incompatible Job Family | Provide one exact Job Family code or name and selected set | JobFamilyId, JobFamilyCode, and confirmed set context |
| job_subfamily | Effective Job Subfamily | Conditional | Create or edit supplies a Job Subfamily | Lookup | Current Job Subfamily LOV | resolve_job_subfamily_for_job | Keeps the Job Subfamily compatible with the resolved Job Family | Provide one exact Job Subfamily code or name and effective date | Stored Job Subfamily value |
| job_grade | Effective Grade | Conditional | A JobGrade row is supplied | Lookup | Grades resource | resolve_job_grade | Prevents an unresolved or set-incompatible Grade | Provide one exact Grade and effective date | GradeCode and confirmed set context |
| benchmark_job | Eligible benchmark Job | Conditional | A benchmark Job is supplied | Lookup | Jobs resource | find_manage_job | Prevents an unresolved or self-referencing benchmark | Provide one exact different Job | Resolved benchmark Job identity |
| workday_defaults | Enterprise Work Day Information | Conditional | Create omits a working-time field that current metadata marks required or defaultable | Lookup | Effective Enterprise EFF context | resolve_job_workday_defaults | Supplies only metadata-confirmed omitted working-time values | Provide a value only when current metadata marks it required and no default resolves | Validated nonblank working-time values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB.DEPENDENCIES | decision | 4 | resolve_dependency | ready->JOB.DEFAULTS;not_required->JOB.DEFAULTS;needs_input->JOB.ERROR;unresolved->JOB.ERROR | JOB.HISTORY | stop | After target and delete-history resolution and before defaulting |
