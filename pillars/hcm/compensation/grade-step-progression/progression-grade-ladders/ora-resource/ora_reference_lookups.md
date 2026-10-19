# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_progression_grade_ladder_business_object | Before validating a Progression Grade Ladder request | Registered discriminator: `ProgressionGradeLadder` | `/hcmRestApi/resources/latest/dataLoaderBusinessObjects?finder=findDataLoaderBos&onlyData=true&limit=500&offset=<n>` | `BusinessObjectId`, `BusObjTopDiscriminator`, `UIName`, `TemplateFileName`, `UcmContentId` | Follow pagination and require exactly one case-sensitive `BusObjTopDiscriminator` match | BusinessObject: `ProgressionGradeLadder`; UI name: Progression Grade Ladder; template: `ProgressionGradeLadder.dat` | Stop as a registered-business-object validation gap; do not infer an alias |
| read_progression_grade_ladder_schema | Before accepting configuration fields | Resolved business object and component IDs | `/hcmRestApi/resources/latest/dataLoaderBusinessObjects/<BusinessObjectId>`; `/hcmRestApi/resources/latest/dataLoaderBusinessObjects/<BusinessObjectId>/child/childBusinessObjects/<ComponentId>/child/attributes` | Component name, attribute name, type, length, mandatory status, user keys, reference object, lookup name, and description | Require readable metadata for `ProgressionGradeLadder`, `GradesInProgressionLadder`, `ProgressionStepRate`, and `ProgressionStepRateValue` | Current field and dependency contract | Stop as a schema-validation gap; do not infer fields, payload shape, lookup values, or defaults |

## Metadata-Declared Lookup Fields

| Component | Field | Lookup Name |
|---|---|---|
| ProgressionGradeLadder | `GradeLadderGrpCode` | `ORA_CMP_GSP_GRADE_LADDER_GRP` |
| ProgressionGradeLadder | `AutoProgressionCode`, `AutoSalChangeCode` | `ORA_CMP_GSP_AUTO_APPROVE` |
| ProgressionGradeLadder | `ProgressionStyleCode` | `ORA_CMP_GSP_PROG_STYLE` |
| ProgressionGradeLadder | `ProgressionDateCode` | `ORA_CMP_GSP_PROG_DT` |
| ProgressionGradeLadder | `GradeType` | `GRADE_TYPE` |
| ProgressionGradeLadder | `UpdateSalaryFlag` | `YES_NO` |
| ProgressionGradeLadder | `RateChangeDateCode` | `ORA_CMP_GSP_RATE_SYNC_DT` |
| ProgressionGradeLadder | `SalaryAdjustmentTypeCode` | `ORA_CMP_GSP_SALARY_ADJ_TYPE` |
| ProgressionGradeLadder | `SalaryCalculationMethodCode` | `ORA_CMP_GSP_SAL_CALC_METH` |
| ProgressionGradeLadder | `SalaryChangeDateCode` | `ORA_CMP_GSP_SAL_CHG_DT` |
| ProgressionGradeLadder, ProgressionStepRate | `ActiveStatus` | `ACTIVE_INACTIVE` |
| ProgressionStepRate | `RateFrequency` | `CMP_SALARY_BASIS` |
| ProgressionStepRate | `RateType` | `GRADE_PAY_RATE_TYPE` |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PGL.RESOLVE_REGISTERED_BO | step | 10 | reference_lookup | resolved->PGL.READ_SCHEMA;not_found->PGL.HANDLE_ISSUE;lookup_failed->PGL.HANDLE_ISSUE | none | stop | Before handling a Progression Grade Ladder request |
| PGL.READ_SCHEMA | step | 20 | reference_lookup | schema_ready->PGL.VALIDATE_INPUT;schema_unavailable->PGL.HANDLE_ISSUE | PGL.RESOLVE_REGISTERED_BO | stop | Before field validation or import preparation |
