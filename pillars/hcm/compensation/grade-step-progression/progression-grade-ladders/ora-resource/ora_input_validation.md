# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Registered Progression Grade Ladder business object | `ProgressionGradeLadder` | Stop | Resolve exactly one registered Data Loader business object with that discriminator | Every request | resolve_progression_grade_ladder_business_object |
| Current Progression Grade Ladder schema | One or more supplied fields present in the current object, component, and attribute metadata | Stop | Read the current metadata before accepting configuration values | Every create, update, import, or validation request | read_progression_grade_ladder_schema |
| Parent ladder identity | `GradeLadderName` and `EffectiveStartDate`; `GradeSetId`, `GradeType`, and `ActiveStatus` for new records | Stop | Provide values conforming to the parent-component metadata | New parent record | read_progression_grade_ladder_schema |
| Grade membership | `GradeId`, `GradesInLadderSequence`, and `EffectiveStartDate` for new child records | Stop | Provide values conforming to the Grades in Progression Ladder component metadata | A grade is added to the ladder | read_progression_grade_ladder_schema |
| Progression step rate | `RateName`, `CurrencyCode`, `RateFrequency`, `LegislativeDataGroupId`, `RateType`, `ActiveStatus`, and `EffectiveStartDate` for new child records | Stop | Provide values conforming to the Progression Step Rate component metadata | A progression step rate is supplied | read_progression_grade_ladder_schema |
| Progression step rate value | `RateObjectId` and `EffectiveStartDate` for new child records | Stop | Provide values conforming to the Progression Step Rate Value component metadata | A step rate value is supplied | read_progression_grade_ladder_schema |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact field identity | Accept only fields returned by current metadata for `ProgressionGradeLadder`, `GradesInProgressionLadder`, `ProgressionStepRate`, or `ProgressionStepRateValue` | Every supplied value | read_progression_grade_ladder_schema |
| Field shape | Validate data type, length, mandatory status, user-key contract, and foreign-key contract from current metadata | Every supplied value | read_progression_grade_ladder_schema |
| Lookup-backed field | Require a value compatible with the lookup name declared in current metadata; do not infer a code or meaning | A supplied field has a `LookupName` | read_progression_grade_ladder_schema |
| Reference-backed field | Require the declared user-key values when a dependent record is identified by a foreign key | A supplied field has `ReferenceIntObjName` | read_progression_grade_ladder_schema |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PGL.VALIDATE_INPUT | step | 30 | validate_input | valid->PGL.CHECK_DEPENDENCIES;invalid->PGL.HANDLE_ISSUE | PGL.READ_SCHEMA | stop | After registered-BO and schema metadata resolve |
