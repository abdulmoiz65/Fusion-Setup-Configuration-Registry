# Areas of Responsibility Templates Dependency Readiness

## Purpose

Defines the conditional template and reference dependencies used by this task.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Template identity | Resolve the target or confirm create availability |
| 2 | Lookup-backed references | Resolve each supplied type, usage, status, attribute, criterion, or category |
| 3 | Criteria and scope values | Resolve each supplied System Person Type, Job Function, Country, Job, Location, and object-backed scope reference into its target source field |
| 4 | Task Hook approval binding | Build the Task Hook preview for the immutable archive, obtain separate approval, verify the archive bytes, and preserve the returned inner `taskValidationEnvelope` for Core Data Loader |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| template_identity | Existing template or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Areas of Responsibility Templates resource | find_areas_of_responsibility_templates | Prevents an ambiguous target or duplicate create | Provide one exact template selector when required | Current template identity and values |
| lookup_reference | Lookup-backed template value | Conditional | A lookup-backed value is supplied | Lookup | Configured lookup | resolve_aor_common_lookup | Prevents an invalid stored value | Provide one exact enabled/effective value; do not infer a sibling-attribute restriction from Lookup Tag | Resolved stored value |
| job_reference | Job criterion | Conditional | A Job criterion is supplied | Lookup | Job resource | resolve_aor_job | Prevents an invalid criterion | Provide one compatible current Job | Resolved Job value |
| location_reference | Location criterion | Conditional | A Location criterion is supplied | Lookup | Location resource | resolve_aor_location | Prevents an invalid criterion | Provide one compatible current Location | Resolved Location value |
| system_person_type_reference | System Person Type criterion | Conditional | A System Person Type criterion is supplied | Lookup | Common lookup `SYSTEM_PERSON_TYPE` | resolve_aor_system_person_type | Prevents an invalid person-type criterion | Provide one enabled/effective exact code or meaning | Resolved SystemPersonType |
| job_function_reference | Job Function criterion | Conditional | A Job Function criterion is supplied | Lookup | Common lookup `JOB_FUNCTION_CODE` | resolve_aor_job_function | Prevents an invalid job-function criterion | Provide one enabled exact code or meaning | Resolved JobFunctionCode |
| country_reference | Country scope or criterion | Conditional | A Country scope or criterion is supplied | Lookup | HCM Countries LOV | resolve_aor_country | Prevents an invalid or obsolete country criterion | Provide one nonobsolete exact country code or name | Resolved TerritoryCode |
| scope_value_reference | Object-backed or hierarchy scope value | Conditional | A populated TemplateScope value other than a literal Last Name range is supplied | Lookup | AOR scope-value resolver matrix | resolve_aor_scope_value | Prevents a display-only or incompatible stored value | Provide one exact effective value and, when applicable, its required set | Exact registered TemplateScope source columns |
| static_blank_scope | Blank static scope | Blocking | A TemplateScope has no static value and DynamicValueFlag is not Y | Temporary AORTemplate contract | No LOV resolution |  | Prevents unsupported blank-child serialization | Stop before source generation: static blank scope serialization is temporarily unsupported pending an attribute-specific loader-proven contract | Preflight blocker |
| representative_reference | Worker assignment | Conditional | A representative is directly assigned | Lookup | Worker assignment resource | resolve_aor_worker_assignment | Prevents an ineligible representative | Provide one eligible worker-assignment pair | Resolved worker and assignment |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact evidence | No |
| Lookup | A declared resolver can resolve the dependency | Run the read-only resolver now; do not pause |
| Not Applicable | The dependency condition is false | No |
| Needs Input | Required business input is missing | No |
| Unresolved | Resolution returns no match, multiple matches, or incompatible evidence | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AORT.DEPENDENCY | decision | 2 | resolve_dependency | ready->AORT.READ;not_required->AORT.READ;needs_input->AORT.ERROR;unresolved->AORT.ERROR | AORT.VALIDATE | stop | After input validation and before task-local reference lookups |
