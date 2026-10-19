# Schedule Generation Profile Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current profile state | For every update, retrieve the latest parent and relevant child resources before constructing the update. |
| 2 | Input validation | Validate required and conditional fields. |
| 3 | LOV resolution | Resolve required supplied references to exact IDs or codes. |
| 4 | Defaults | Apply permitted defaults only after input and lookup checks. |
| 5 | Create duplicate check | For a new-profile create operation, compare the complete resolved and defaulted configuration with all current profiles and populated child collections. Skip this check for an explicit duplicate operation. |
| 6 | Design checks | Validate coverage, conditional fields, and deferred features. |
| 7 | Execution route | Use the setup task's approved workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_profile_state | Latest parent and child state | Yes | Any update is requested | Lookup | Fusion REST current state | resolve_current_schedule_profile | Update payloads must preserve provider-generated parent and child identifiers, surrogate user codes, and unchanged current values. | Supply the profile code and business identity of each child to update. | Current parent fields and ScheduleGenerationProfileId; current relevant child fields, REST IDs, and surrogate user codes. |
| create_duplicate_check | Current configurations and child state | Yes | Any new-profile create operation | Lookup | Fusion REST current state | find_identical_schedule_profile_configuration | An existing configuration that exactly matches the requested parent settings and populated child settings requires an explicit user decision before a second profile is created. An explicit duplicate operation is already the user's decision to create another profile and bypasses this check. | Confirm whether to create a separate profile after an exact match is shown. | Existing matching profile business identity and verified business configuration. |
| profile_references | Schedule profile LOV values | Conditional | A referenced UI value is supplied | Lookup | Fusion REST | | Exact IDs and codes are required | Select an exact candidate when more than one value matches | IDs and codes for the selected references |
| condition_builder | Condition Builder capability | No | Rotation groups or published-open-shift groups are supplied | Not Applicable | Deferred feature | | These fields are ignored until Condition Builder uptake | Do not provide group values in the current profile request | rotationGroups[].ListId; opportunityGroups[].ListId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required values are supplied as valid IDs or codes | No |
| Lookup | A name or display value requires resolution | Yes |
| Not Applicable | A deferred Condition Builder field is supplied | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SGP.DEPENDENCIES | step | 2 | resolve_dependency | ready->SGP.LOOKUP.INCLUDE_EXCLUDE;blocked->SGP.ERROR | SGP.VALIDATE | stop | Always |
