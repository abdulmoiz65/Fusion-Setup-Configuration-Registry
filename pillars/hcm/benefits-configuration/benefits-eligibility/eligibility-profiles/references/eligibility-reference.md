# Eligibility Reference

Runtime workbook, mapping, lookup, import, and evaluation reference.
Use the contents to locate the section required by `../SKILL.md`.
Machine-readable runtime contracts are stored in `eligibility-contracts.json`.

XML sample paths identify members in `../assets/plan-copy/templates.zip`
when no loose override exists. Commands use repository-root paths.

## Contents

All runtime contracts are consolidated in `eligibility-contracts.json`, version 1:

- `lookup_mappings`: criterion lookup declarations.
- `map_rules`: Plan Copy mapping rules.
- `mapping_catalog`: criterion mappings, resolver links, lookup inventory, and resolvers.
- `openapi`: the reviewed Plan Copy API contract.

Legacy filenames and mapping-directory paths below are logical aliases supported
by the shared reader, not additional files. `mapping-reference.json:section_name`
denotes an array inside `mapping_catalog`. Historical CSV references identify
the same preserved fields and rows. Loose custom files take precedence.

- [Eligibility best practices and evaluation](#eligibility-best-practices)
- [Eligibility Workbook to Plan Copy XML](#eligibility-profiles)
- [Postal Code Ranges and Service Areas Workbook to Plan Copy XML](#postal-ranges-and-service-areas)
- [Derived Factors Workbook to Plan Copy XML](#derived-factors)
- [Eligibility Workbook to Plan Copy Map XML](#plan-copy-map)
- [Eligibility Plan Copy REST Import](#import-and-recovery)
- [HCM Lookups Used by Eligibility Profile Criteria](#hcm-lookup-criteria)
- [REST API Resolvers for Eligibility-Profile Mappings](#rest-api-resolvers)

<a id="eligibility-profiles"></a>

## Eligibility Workbook to Plan Copy XML

Use `scripts/eligibility.py convert-profiles` to convert the human-readable eligibility-profile workbook into `BEN_ELIGY_PRFL.xml`.

### Required Inputs

- An end-user copy of the included `Fusion_Elpro_Setup.xlsx` sample workbook, with example rows replaced by their own data. Any filename is accepted. Unused tabs may be removed or left blank, including header-only tabs; they contribute no setup objects. At least one setup row must remain across the workbook.
- When creating profiles, one visible worksheet named `Participant Eligibility`. It may be omitted when creating only supporting setup objects. Populated tabs retain the sample's names and headers; dependencies referenced by populated rows must still exist.
- A header row containing the profile columns `Name`, `Description`, `Status`, `Profile Type`, `Profile Usage`, and `Assignment to Use` before `Eligibility - Criteria`.
- The criterion columns `Eligibility - Criteria`, `Sequence`, `Name`, and `Exclude`.
- The bundled Oracle-exported sample at `assets/plan-copy/BEN_ELIGY_PRFL.xml`. It contains a real `EligibilityProfileVORow`; a staging-only placeholder is not a conversion template.
- The selected target environment's OAuth properties and token cache. Lookup values are resolved from the HTTPS origin in `restBaseUrl` before the output file is written.

Continuation rows may leave the profile columns blank and add another criterion to the preceding profile.
Sequence is required and must be positive for every supported criterion except Marital Status, whose Plan Copy row has no sequence element.

### Supported Values

| Workbook field | Supported workbook value | XML value |
| --- | --- | --- |
| Status | Active / Inactive | A / I |
| Profile Type | Participant | PRTP |
| Profile Usage | Enabled `BEN_BNFT_CAGR_PRTN` product name or code; see below | Corresponding product code, preserved without substituting BNFT |
| Assignment to Use | Any assignment - enterprise | ANE |
| Criteria | Assignment Status, Bargaining Unit, Business Unit, Hourly or Salaried, Job Function, Labor Union Member, Legal Employer, Marital Status, Manager, Religion, Union | Corresponding sample `*CriteriaVO` structure |
| Criteria | Tobacco Use, Gender, Disabled, Termination Reason, Assignment Category, Salary Basis, Quartile in Grade, Formula, Department | Corresponding sample `*CriteriaVO` structure |
| Criteria | Job Family, Collective Agreement, Person Type | Corresponding V2 sample `*CriteriaV2VO` structure |
| Criteria | Age, Compensation, Benefit Groups | `AgeCriteriaVO`, `CompensationCriteriaVO`, or `BenefitsGroupCriteriaVO` |
| Criteria | Length of Service, Age and Service, Hours Worked, Full-Time Equivalent | Corresponding package-local derived-factor `*CriteriaVO` structure |
| Criteria | Postal Code Range, Service Area | `PostalZipRangeCriteriaVO` or `ServiceAreaCriteriaVO` |
| Exclude | blank, N/No, Y/Yes | N or Y |
| Person Type value | Exact active `UserPersonType` whose `SystemPersonType` is `EMP`, such as Employee | `UserPersonType` from the matched lookup row and `SystemPersonType` fixed by that row to EMP |
| Tobacco Use value | Exact active `TOBACCO_USER` meaning, such as Cigar | Returned `LookupCode`, such as CIGAR |

#### Supported Profile Usage products

Accept these display names or their codes, case-insensitively. This list comes
from the enabled `BEN_BNFT_CAGR_PRTN` seeds in ADE, not from the skill's
Benefits offering identity. Different profiles in one workbook may use
different supported products.

| Profile Usage | Plan Copy `BnftCagrPrtnCd` |
| --- | --- |
| Benefits | BNFT |
| Checklist | CHKLIST |
| Compensation | CMP |
| Employee Wellness | EHW |
| Field services | FFS |
| Global | GLOBAL |
| Goals Management | GOAL |
| Personal Brand | HWR |
| Performance | PERFORMANCE |
| Employee Communications | ORA_EMP_COMMUNICATION |
| Opportunity Marketplace | ORA_OPP_MARKET_PLACE |

`CAGR` (Collective agreements) and `MUSE` (Multiuse) are seeded with
`EnabledFlag=N`, so they are not supported for new workbook profiles.
Unknown or disabled usages remain validation errors; do not silently default
them to Benefits. Product support does not add unsupported criterion types,
change assignment options, or waive target validation and import approval.

Source: ADE view label `FUSIONAPPS_PT.V2MIBHCMBRONZE_LINUX.X64_261007.1000.S`.
The ADF `LOV_BnftCagrPrtnCd` uses `BEN_BNFT_CAGR_PRTN` in
`fusionapps/hcm/components/hcmBenefits/eligibility/protectedUiModel/src/oracle/apps/hcm/eligibility/protectedUiModel/view/EligibilityProfileVO.xml`.
Codes, meanings, and enabled flags are maintained in
`fusionapps/hcm/ben/db/data/HcmPlanDesignTop/CommonLookupTypeSD.xml`;
English labels are corroborated by `US/CommonLookupTypeSD.xlf` in that directory.
The migration VO preserves `BnftCagrPrtnCd` in
`fusionapps/hcm/components/hcmBenefits/HcmEligibilityMigration/src/oracle/apps/hcm/eligibility/migrationService/view/EligibilityProfileVO.xml`.

The converter covers all listed criteria and reconciles lookup-backed values with the maintained `mapping-reference.json:criteria_mapping`, `mapping-reference.json:criteria_resolver_links`, `mapping-reference.json:hcm_lookup_criteria`, and `mapping-reference.json:rest_api_resolvers` reference contracts. Common-lookup criteria accept either an exact `Meaning` or `LookupCode`. Object LOVs validate direct-name values and return paired fields where XML needs a code in addition to the label: `ActionName`/`ActionCode`, `JobFamilyName`/`JobFamilyCode`, `CollectiveAgreementName`/`IdentificationCode`, and `UserPersonType`/`SystemPersonType`. Formula, department, legal-employer, business-unit, union, salary-basis, assignment-status, and pre-existing Benefit Group names are preflighted against their mapped target-pod resources. Missing target rows block output. Ambiguous rows also block output except for Department, whose maintained first-match policy selects the first exact active row in Fusion response order and emits a warning.

In the eligibility package workflow, every derived-factor criterion name must exactly match a factor defined in its corresponding workbook tab. `Postal Code Range` and `Service Area` names must exactly match the package's corresponding tabs; singular and plural criterion labels are accepted. `Benefit Groups` names are pre-existing target-pod dependencies and must resolve exactly through read-only `/hcmRestApi/resources/11.13.18.05/benefitGroupsLOV`; a missing group blocks generation. The generated criteria retain null factor/helper IDs so Plan Copy links package-local eligibility objects by batch order and natural name.

`UserPersonType` and `SystemPersonType` are a paired lookup result. The maintained declaration maps Person Type to the read-only `/hcmRestApi/resources/11.13.18.05/personTypesLOV` resource. The converter requests active rows, restricts candidates to `SystemPersonType=EMP`, exact-matches the workbook value against `UserPersonType`, and writes both fields from that one row into `PersonTypeCriteriaV2VORow`. Its grouping key is `<profile>,<UserPersonType>,<SystemPersonType>`. For example, `Employee` resolves to `Employee,EMP`. If the same user-person-type name occurs in more than one active EMP row, resolution fails as ambiguous; `DefaultFlag` is not used.

`UsesTbcoFlag` is lookup-backed; it is not Boolean-only. The maintained declaration in `criterion-lookup-mappings.json` maps the XML field to lookup type `TOBACCO_USER` and the read-only `/fscmRestApi/resources/11.13.18.05/commonLookupsLOV` resource. The converter calls `LookupTypeFinder` for rows active on the current date, exact-matches the workbook value against `Meaning`, and stores `LookupCode`. For example, `Cigar` resolves to `CIGAR`, while the meanings `Any` and `None` resolve to `Y` and `N` respectively.

Lookup responses are paginated and must contain exactly one matching active row unless the maintained mapping explicitly declares `multiple_match_policy: first`. Only Department declares that policy. Repeated collection results are cached for the current conversion. Missing, malformed, inaccessible, unavailable, or otherwise ambiguous lookup data fails closed before output is written. Do not add command-line value overrides; update the reviewed criterion lookup declaration only when the field-to-lookup contract itself changes.

Department resolution uses the date-effective `departments` collection with
`q=Name='<workbook value>'`, followed by exact client-side name matching. Do
not use `departmentsLovV2`: its contextual `findByWord` finder can return no
row for departments that are visible through the canonical collection.

### Command

Run with Python 3.11 because the shared XLSX reader requires a modern Python runtime:

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py convert-profiles \
  --input "<work-directory>/Fusion_Elpro_Setup.xlsx" \
  --sample "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/assets/plan-copy/BEN_ELIGY_PRFL.xml" \
  --output "<BEN_ELIGY_PRFL.xml>"
```

Use `--force` only after approving replacement of an existing output.

There is no `--map-value` option. The converter uses the configured Fusion environment and shared `.fusionaim_token.json` OAuth cache internally. If the cache is missing or expired, the shared authentication flow opens the configured OAuth login and refreshes it without printing token contents.

Use the selected environment's maintained OAuth configuration and its gitignored token cache:

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py convert-profiles \
  --input "<work-directory>/Fusion_Elpro_Setup.xlsx" \
  --sample "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/assets/plan-copy/BEN_ELIGY_PRFL.xml" \
  --output "<BEN_ELIGY_PRFL.xml>" \
  --properties "core/auth/fusionEnv.properties" \
  --token-cache auto
```

The properties `restBaseUrl` must resolve to the selected target environment's HTTPS origin. This skill
uses the shared OAuth client for all Fusion REST requests.

The converter writes XML and makes read-only lookup GET requests. It does not create the nested Plan Copy ZIP, generate or validate `checksum.txt`, or call a mutating Fusion REST operation.

<a id="postal-ranges-and-service-areas"></a>

## Postal Code Ranges and Service Areas Workbook to Plan Copy XML

The combined generator converts the two visible worksheets in
`Fusion_Elpro_Setup.xlsx` into package-local Benefits setup objects. It uses
the Oracle-exported samples only for structure:

- `assets/plan-copy/BEN_PSTL_ZIP_RNG.xml`
- `assets/plan-copy/BEN_SVC_AREA.xml`

### Postal Code Ranges

If supplied, use one visible `Postal Code Ranges` worksheet with this header.
An omitted, blank, or header-only tab creates zero postal ranges; it is not an error
unless populated criteria or Service Areas reference a missing range.

| Workbook column | Required | Plan Copy field |
| --- | --- | --- |
| `From Value` | Yes | `FromValue` |
| `To Value` | Yes | `ToValue` |
| `Start Date` | Yes; `YYYY-MM-DD` or `YYYY/MM/DD` | `StartDate` |
| `End Date` | No; not before Start Date | `EndDate` |

The natural key is `<From Value>-<To Value>`. It is written to `GroupingKey`,
`ZipRange`, and `PostalZipRange`; duplicate ranges block the package. The
converter keeps `PstlZipRngId` null so Plan Copy creates the target row.

### Service Areas

If supplied, use one visible `Service Areas` worksheet with this ordered header.
An omitted, blank, or header-only tab creates zero service areas.

| Workbook column | Required | Plan Copy field |
| --- | --- | --- |
| `Name` | Yes | `GroupingKey`, `Name`, `ServiceAreaName` |
| `Service Type` | Yes | Resolve active `BEN_PRDCT` HCM lookup; write `OrgUnitPrdct` |
| first `Start Date` / `End Date` | Start required; end optional | Service Area effective dates |
| `From Value` / `To Value` | Yes | Child `PostalZipRange` natural key |
| second `Start Date` / `End Date` | Start required; end optional | Child link effective dates |

Rows with the same Service Area Name form one Service Area and its child
`PostalZipRangesInServiceAreaVO` rows. Repeated Service Area rows must have
the same type and parent effective dates. A referenced child range must exist
in the package's `Postal Code Ranges` tab, and child dates must be inside both
the parent Service Area and referenced postal range dates. Duplicate range links
within one Service Area block the package.

Service Type resolution is read-only and uses
`/fscmRestApi/resources/11.13.18.05/genericLookups`, finder
`LookupTypeFinder;LookupType=BEN_PRDCT,ViewApplicationId=3`, nested
`lookupCodes`, and active HCM lookup dates. The resolved `LookupCode` is
written to `OrgUnitPrdct`; no database lookup or manually supplied code is
accepted.

The generator keeps `SvcAreaId`, `SvcAreaPstlZipRngId`, and child
`PstlZipRngId` null. Participant Eligibility `Postal Code Range` and `Service
Area` criteria must reference these same package-local natural names. The batch
order is `PostalCodeRange`, then `ServiceArea`, before `EligibilityProfile`.
Neither object emits a `BEN_PL_COPY_MAP` row.

<a id="derived-factors"></a>

## Derived Factors Workbook to Plan Copy XML

Use the maintained derived-factor converters to convert the six derived-factor
worksheets in `Fusion_Elpro_Setup.xlsx` into their Plan Copy XML batches.

### Worksheet names

The preferred worksheet names are `Derived Factors - Age`, `Derived Factors -
Comp`, `Derived Factors - LOS`, `Derived Factors - Age and LOS`, `Derived
Factors - Hours Worked`, and `Derived Factors - FTE`. Compatibility aliases are
accepted by the converter. Each supplied section has one visible worksheet from
its name set. Omitted, blank, or header-only sections create zero factors.
References to missing factors still fail validation.

### Age contract

| Workbook column | Required | Plan Copy field |
| --- | --- | --- |
| `Derived factor Name` | Yes; unique ignoring case | `GroupingKey`, `Name`, `AgeFactorName` |
| `Age to use` | Yes | Resolve `BEN_AGE_TO_USE_CD`; write `AgeToUseCd` |
| `Units` | Yes | Resolve `BEN_TM_UOM`; write `AgeUom` |
| `Calcualtion Formula` or `Calculation Formula` | No | Validate exact `fastFormulas` dependency; write `AgeCalculationFormulaName` |
| `Greater than or equal to Age` | No; nonnegative number | `MnAgeNum` |
| `Less than Age` | No; greater than minimum when both are supplied | `MxAgeNum` |
| `Determination Rule` | Yes | Resolve `BEN_AGE_DET`; write `AgeDetCd` |
| `Determination Formula` | Required only for Formula rule | Validate exact formula dependency; write `AgeDeterminationDateFormulaName` |
| `Rounding Rule` | No | Resolve `BEN_RNDG`; write `RndgCd` |
| `Rounding Formula` | Required only for Formula rounding | Validate exact formula dependency; write `RoundingFormulaName` |

The converter preserves the exported contract values
`NoMnAgeFlag=Y` and `NoMxAgeFlag=Y`, and keeps `AgeFctrId` null for object
creation.

### Compensation contract

| Workbook column | Required | Plan Copy field |
| --- | --- | --- |
| `Name` | Yes; unique ignoring case | `GroupingKey`, `Name`, `CompensationLevelFactorName` |
| `Unit of Measure` | Yes | Resolve exact currency name/code through `currenciesLOV`; write `CompLvlUom` |
| `Source` | Yes | Resolve the secured `HCM_LOOKUPS` type `BEN_COMP_SRC` through `genericLookups`; this sample supports `Formula` and `Benefits balance type` |
| `Stated Salary/Calc Formula/BenBalType` | Yes | Exact formula or Benefit Balance dependency name |
| `Greater than or equal to compensation` | No; nonnegative number | `MnCompVal` |
| `Less than Compensation` | No; greater than minimum when both are supplied | `MxCompVal` |
| `Determination Rule` | Yes | Resolve `BEN_COMP_LVL_DET`; write `CompLvlDetCd` |
| `Determination Formula` | Required only for Formula rule | Validate exact formula dependency; write `CompensationDeterminationDateFormulaName` |
| `Rounding Rule` | No | Resolve `BEN_RNDG`; write `RndgCd` |
| `Rounding Formula` | Required only for Formula rounding | Validate exact formula dependency; write `RoundingFormulaName` |

For source `Formula`, validate the exact target `fastFormulas` row, write
`CompensationCalculationFormulaName`, and keep `CompCalcRl` null for the Plan
Copy key helper. For source `Benefits balance type`, validate the exact target
`benefitBalancesLOV` row. The balance must already exist on the target pod.
Write `BenefitBalanceName` and keep `BnftsBalId` null. Missing or
ambiguous external dependencies block package generation before any Fusion
write.

The converter preserves `NoMnCompFlag=N` and `NoMxCompFlag=N` from the
Oracle-exported sample and keeps `CompLvlFctrId` null for object creation.

### Length of Service contract

`Derived Factors - LOS` requires a unique Name, Unit of Measure, Determination
Rule, and Period Start Date Rule. Minimum and maximum values are nonnegative and
the minimum must be less than the maximum when both are supplied. Resolve Unit
of Measure from `BEN_TM_UOM`, Determination Rule from `BEN_LOS_DET`, Period
Start Date Rule from `BEN_LOS_DT_TO_USE`, and Rounding Rule from `BEN_RNDG`
through REST. `BEN_TM_UOM` and `BEN_RNDG` use active `commonLookupsLOV` rows;
the HCM-owned `BEN_LOS_DET` and `BEN_LOS_DT_TO_USE` types use active
`genericLookups` `HCM_LOOKUPS` rows. Validate optional determination and
rounding formulas through `fastFormulas`. Write `BEN_LOS_FCTR.xml`, keep
`LosFctrId` null, and keep unused formula and seniority-date key helpers at
literal `#null`.

### Age and Service contract

`Derived Factors - Age and LOS` requires a unique Name, an Age Factor, a Length
of Service Factor, and the lower and upper combined range. Both referenced
factor names must exist in the same workbook's Age and Length of Service tabs.
Write `BEN_CMBN_AGE_LOS_FCTR.xml` with null `AgeFctrId`, `LosFctrId`, and
`CmbnAgeLosFctrId` helpers so Plan Copy resolves the package-local objects by
natural name and batch order.

### Hours Worked contract

`Derived Factors - Hours Worked` requires a unique Name, Source, Benefit
Balance, Payroll Frequency, and Determination Rule. Resolve Source from
`BEN_HRS_WKD_SRC`, Payroll Frequency from `BEN_FREQ`, Determination Rule from
`BEN_HRS_WKD_DET`, and Rounding Rule from `BEN_RNDG` through REST. The
HCM-owned source, payroll-frequency, and determination types use active
`genericLookups` `HCM_LOOKUPS` rows; rounding uses active `commonLookupsLOV`
rows. The maintained worksheet/sample contract supports the `BNFTBALTYP`
Benefits balance source. Validate every balance through `benefitBalancesLOV`;
the balance must already exist on the target pod. Validate optional
formulas through `fastFormulas`. Write
`BEN_HRS_WKD_IN_PERD_FCTR.xml`, retaining the natural Benefit Balance name and
null key-helper IDs.

### Full-Time Equivalent contract

`Derived Factors - FTE` requires a unique Name and Assignment to Use. Accept
only `Primary Assignment` or `Sum of all assignments`; write the corresponding
`UsePrmryAsntOnlyFlag` and `UseSumOfAllAsntsFlag` pair. Validate the optional
rounding rule through `BEN_RNDG` and its optional formula through
`fastFormulas`. Write `BEN_PCT_FL_TM_FCTR.xml` and keep `PctFlTmFctrId` null.

### Samples and package order

Use the Oracle-exported structural samples:

- `assets/plan-copy/BEN_AGE_FCTR.xml`
- `assets/plan-copy/BEN_COMP_LVL_FCTR.xml`
- `assets/plan-copy/BEN_LOS_FCTR.xml`
- `assets/plan-copy/BEN_CMBN_AGE_LOS_FCTR.xml`
- `assets/plan-copy/BEN_HRS_WKD_IN_PERD_FCTR.xml`
- `assets/plan-copy/BEN_PCT_FL_TM_FCTR.xml`

The complete batch sequence is PlanCopyMap, BenefitsGroup, BenefitBalance,
PostalCodeRange, ServiceArea, AgeFactor, LengthOfServiceFactor, CombinedAgeLosFactor,
CompensationLevelFactor, HoursWorkedFactor, FullTimeEquivalentFactor, then
EligibilityProfile. See `eligibility-reference.md#postal-ranges-and-service-areas` for the two
setup-object batch contracts.
Participant Eligibility derived-factor criteria must exactly match a factor
name in the corresponding worksheet. Missing package-local references stop
generation before any XML or ZIP output is written; no database or external ID
lookup is used for these Benefits-owned dependencies.
All lookup and dependency validation uses the same selected target environment OAuth
target as the eventual Plan Copy import.

<a id="plan-copy-map"></a>

## Eligibility Workbook to Plan Copy Map XML

Use `scripts/eligibility.py convert-map` to generate the `BEN_PL_COPY_MAP.xml` companion artifact from the eligibility-profile workbook.

### Mapping rows

The eligibility generator emits one deduplicated row for each populated eligibility value whose maintained classification is `REQUIRED`. Required mappings are Legal Employer, Assignment Status, Salary Basis, Person Type, Business Unit, Job Family, Termination Reason, Department, Collective Agreement, and Union. Lookup-code criteria and other Benefits-owned dependencies do not produce Plan Copy map rows. Participant Eligibility `Age`, `Compensation`, `Postal Code Range`, and `Service Area` references are linked by package order and natural name. Benefit Group and Benefit Balance references resolve against objects that already exist on the target pod; this workflow does not create or map those objects.

| XML field | Source |
|---|---|
| `SrcName` | Exact display name returned by the selected pod |
| `SrcTableName` | `target_reference` from `mapping-reference.json:criteria_mapping` |
| `ColumnName` | `source_column` from `mapping-reference.json:criteria_mapping`; Union uses the package-declared `CRIT_CHAR1` |
| `SrcId` | Exact resolver ID returned by the selected pod |
| `TrgId` | Same validated resolver ID, pre-resolved to avoid manual mapping |
| `TrgName` | Same exact returned display name |
| `TableName` | `criterion_table` from `mapping-reference.json:criteria_mapping` |
| `CompObjId` | Maintained static default `300100655047592`, unless explicitly overridden |
| `CompObjType` | Static `ELIG` |

The generator joins `mapping-reference.json:criteria_mapping` to `mapping-reference.json:criteria_resolver_links` and `mapping-reference.json:rest_api_resolvers`, then checks that the resolver endpoint agrees with `criterion-lookup-mappings.json`. Any missing row, non-`REQUIRED` classification, endpoint mismatch, unresolved name, missing ID, or ambiguous match blocks output, except that duplicate exact Department names inherit the maintained first-match policy and use the first ID in Fusion response order with a warning. A source referenced by more than one setup object is emitted once using `SrcTableName`, `SrcId`, `SrcName`, and mapping attributes as its logical key. This prevents the duplicate-target validation error while retaining pre-resolved target IDs and names, so no manual mapping step is required.

`MapAttribute1` carries `SystemPersonType` for Person Type, `JobFamilyCode` for Job Family, and `IdentificationCode` for Collective Agreement. Person Type also uses the system-person-type display literal `Employee` in `MapAttribute2` because the maintained rule restricts `SystemPersonType` to `EMP`.

### Command

Use the selected target environment's OAuth properties and token cache:

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py convert-map \
  --input "/path/to/Fusion_Elpro_Setup.xlsx" \
  --sample "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/assets/plan-copy/BEN_PL_COPY_MAP.xml" \
  --mapping-reference-dir "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/references/eligibility-profile-mapping-reference" \
  --output "/path/to/BEN_PL_COPY_MAP-converted.xml" \
  --properties "core/auth/fusionEnv.properties" \
  --token-cache auto
```

The sample is structural input and must not be overwritten. The generator creates neither a ZIP nor a checksum.

<a id="import-and-recovery"></a>

## Eligibility Plan Copy REST Import

Use `scripts/eligibility.py import` only after `benefits_eligibility.zip` passes the
eligibility package generator. The task-local `ora-resource` package supplies the
machine-readable validation, dependency, read-only lookup, design, approval,
and error rules. `plan-copy.openapi.json` is the OpenAPI 3.1.2, host-neutral API
contract for the fixed endpoint and payload lifecycle. It contains no scripts,
credentials, environment URL, runtime date, or local file path, and it defines
no mapping PATCH operation.

The importer evaluates its built-in preflight against the compiled resource
plan and writes the ordered results into the immutable Task Hook preview. A
caller may supply a reviewed `--rule-results` file when an external evaluator
is required. If a new planned resource has no built-in evaluator, preview fails
closed instead of silently passing the new rule.

### Enforced sequence

1. Validate the OpenAPI document, nested ZIP shape, target identity, task context,
   metadata, and explicit effective date. When the caller omits the date, use
   the current date.
2. Create an immutable preview containing the target, exact metadata,
   OpenAPI SHA-256, archive SHA-256, and object inventory. No Fusion request
   is sent in preview mode.
3. Stop until the user sends a later standalone message exactly `approve`.
4. Re-read the OpenAPI document and ZIP and require their hashes and approved
   metadata to remain unchanged.
5. Show the exact target, archive details, import name, effective date,
   eligibility profiles, Postal Code Ranges, Service Areas, Age
   factors, Compensation factors, criterion counts, mapping-row count, and
   action. The
   interactive caller must type exactly `approve` before the first write.
6. Create the `benefitPlanCopyParameters` metadata row and upload the approved
   ZIP to its `PackageContent` enclosure.
7. Create metadata with `RequestSource: "FDOS"`, then submit
   `generateMappings` and poll its ESS request. This single request performs
   both mapping generation and import; do not call `submitImport`.
8. Retrieve every mapping page and require zero source rows with a null target
   ID. This is the post-request integrity check; package generation must resolve
   all target IDs before the mutating action.
9. Refresh the Plan Copy parent through REST until `ImportPlDesign` reaches
   `12` (success) or `10` (error).
10. Download `enclosure/RequestLogs` as `application/octet-stream`. This is the
    consolidated import log stored in `BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB2`.
    Any recognized error in the log overrides ESS or parent success. Report
    success only when the parent is code `12` and this log is non-empty and
    error-free. Retrieve REST child processing-log rows as supplemental failure
    detail.

Every Fusion request sends `REST-Framework-Version: 9`. Metadata creation uses
`application/vnd.oracle.adf.resourceitem+json`, action requests use
`application/vnd.oracle.adf.action+json`, and enclosure upload uses
`application/zip`.

### Authentication and target identity

Live Plan Copy writes use OAuth through
`core.auth.fusion-oauth-authentication`. The OAuth `restBaseUrl` supplies the
selected target environment's HTTPS origin. Do not put a
password, bearer token, client secret, or token-cache content in the REST
contract, command, preview, project workspace, or ZIP.

The package must use lookup IDs and validated dependency names from that same
target pod. A target change requires regenerating all ten XML files and the ZIP
and creating a new preview.

### Eligibility preview command

The work directory must contain:

- `Fusion_Elpro_Setup.xlsx`;
- an existing Run Book task-context JSON.

The launcher reads every convention-named Oracle-exported XML sample from
`assets/plan-copy/`, the API contract from
`references/plan-copy.openapi.json`, and the maintained mapping catalogs
from `references/eligibility-profile-mapping-reference/` by default.

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py \
  --input "<work-directory>/Fusion_Elpro_Setup.xlsx" \
  --effective-date "<YYYY-MM-DD; defaults to the current date>" \
  --work-dir "<work-directory>" \
  --properties "core/auth/fusionEnv.properties" \
  --token-cache auto \
  --task-context "<task-context.json>"
```

This generates the ten converted XML files and `benefits_eligibility.zip`, creates
`benefits_eligibility.zip.plan-copy-import-preview.json`, and stops without a Fusion
POST or PUT.

### Approved execution

Only after a later standalone `approve`, rerun the identical command with:

```text
--approve-upload --force
```

`--force` authorizes deterministic replacement of the local generated XML and
ZIP. It does not authorize a Fusion write by itself. The importer separately
verifies the immutable preview and requires exact interactive approval.

Do not rerun an approved command after a partial live failure. Preserve the
Plan Copy ID, combined mapping/import request ID, stage, and raw statuses in
internal recovery state. User-facing output shows the approved Plan Copy name,
a `SUCCESS` or `ERROR` status derived from `MappingRequestStatus`, and, on
failure, sanitized error details from `RequestLogs`; it does not display the
internal IDs or ESS status. Resume or retry only through the purpose-built path
and with the required approval.

### Environment handling

The launcher uses the existing process proxy configuration and normal CA
validation. All lookup and import requests use the HTTPS origin supplied by
the OAuth properties `restBaseUrl`; an explicit target override must match it.

### Failure behavior

- Input, archive, OpenAPI, target, effective-date, and stale-preview errors
  fail before a Fusion write.
- A mapping/import ESS timeout retains the request ID, last status, and elapsed
  wait internally; it does not display them or submit a replacement request.
- An unsuccessful combined request or any unresolved mapping is a failed import;
  there is no second `submitImport` action.
- A successful mapping/import ESS request does not override the Plan Copy parent.
  `ImportPlDesign=10` is a failed import; only `ImportPlDesign=12` is reported
  as success. A nonterminal or missing value is polled until the existing
  timeout and then fails closed.
- A parent success does not override the consolidated `RequestLogs` enclosure.
  Any recognized error or an empty consolidated log fails closed. On failure,
  include recognized consolidated-log errors and use the REST child log
  collection as supplemental detail.
- Missing or non-exact approval is an `approval_blocker`.
- Live POST and PUT calls are never retried automatically. A read-only GET may
  refresh one rejected cached OAuth token once.
- Authorization, password, client-secret, access-token, and full archive values
  are redacted from diagnostics.

### Diagnostic-only database boundary

The normal workflow uses REST for lookups, mappings, parent status, and logs.
Database access must never be invoked by the importer. When a reported REST
status or log is insufficient for root-cause analysis, use the separately
configured read-only database diagnostic connector only after entering a debugging task.
It must expose read-only queries and no write operation. For Plan Copy diagnostics,
`BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB1` contains the uploaded ZIP package;
the consolidated import log is in `PARAM_ATTRIBUTE_BLOB2`.

Exit code `0` means preview creation or live completion succeeded. Code `1`
means preflight, authorization, transport, Fusion API, approval, or persistence
failure. Code `2` means a REST-resource or mapping contract mismatch. Code `3`
means ESS polling timed out. Code `4` means an ESS or parent process reached an
unsuccessful terminal status.

<a id="hcm-lookup-criteria"></a>

## HCM Lookups Used by Eligibility Profile Criteria

### Scope

This inventory documents fixed and dynamic HCM lookups used by
eligibility-profile criterion models.

It distinguishes an active LOV binding from a lookup accessor that is merely
declared in a model. It also identifies lookup-backed fields in supporting
Benefits setup objects used by a criterion. The machine-readable inventory is
in `eligibility-profile-mapping-reference/mapping-reference.json:hcm_lookup_criteria`.

The result is 41 active bindings across 31 criteria and 25 fixed lookup types,
plus four dynamic user-defined value bindings, six declared-only accessors,
and two supporting-setup bindings.

Active criterion bindings consistently store `LookupCode` and display
`Meaning`. These codes are literals, not target-pod object IDs, but they must
still be validated against the target pod for the relevant effective date,
enabled state, legislation, and reference-data context.

### Criterion values

These lookup codes are the main selectable value of the criterion.

| Criterion | Criterion code | HCM lookup type | Stored attribute |
|---|---:|---|---|
| Bargaining Unit | — | `BARGAINING_UNIT_CODE` | `BrgngUnitCd` |
| Disabled | — | `REGISTERED_DISABLED` | `DsbldCd` |
| Full Time / Part Time | — | `EMP_CAT` | `FlTmPtTmCd` |
| Gender | — | `SEX` | `Sex` |
| Hourly / Salaried | — | `HOURLY_SALARIED_CODE` | `HrlySlrdCd` |
| Job Function | `JBF` | `JOB_FUNCTION_CODE` | `CritChar1` |
| Labor Union Member | — | `BEN_PDW_ELPRO_LBR_MMBR` | `LbrMmbrFlag` |
| Marital Status | — | `MAR_STATUS` | `MaritalStatus` |
| Manager | `MNG` | `BEN_YES_NO` | `CritChar1` |
| Military Status | — | `YES_NO` | `MltryStatCd` |
| Opted for Medicare | — | `YES_NO` | `OptdMdcrFlag` |
| Other Coverage | — | `YES_NO` | `CoordBenNoCvgFlag` |
| Quartile in Grade | — | `CMP_QUAR_IN_GRD` | `QuarInGradeCd` |
| Religion | `REL` | `PER_RELIGION` | `CritChar1` |
| Student Status | — | `BEN_STUDENT_STATUS` | `StdntStatCd` |
| Tobacco Use | — | `TOBACCO_USER` | `UsesTbcoFlag` |
| Designator Enrolled Coverage | — | `YES_NO` | `DsgntrCrntlyEnrldFlag` |
| Dependent Coverage Required Relationship | — | `CONTACT` | `PerRelshpTypCd` |

The relationship criterion uses the plan-design `HcmLookupVO`; the other
fixed entries use the common `HcmLookupPVO` directly or the eligibility
component's `HcmLookupValuesVVO` wrapper.

### Lookup-backed fields within criteria

Some criteria have a non-lookup primary value but use HCM lookups for their
controls, units, or date rules.

| Criterion | Field or role | HCM lookup type | Stored attribute | State |
|---|---|---|---|---|
| Geography | Address type | `ADDRESS_TYPE` | `CritChar4` | Active |
| Geography | Primary-address flag | `YES_NO` | `CritChar5` | Active |
| Hire Date | Date basis | `BEN_ELIG_LOS_DT` | `CritChar1` | Active |
| Hire Date | Month | `CMP_MONTH` | `CritChar2` | Active |
| Hire Date | Day | `CMP_DATE` | `CritChar3` | Active |
| Hire Date | Units | `CHECKLIST_QUALIFYING_UNITS` | `CritChar4` | Active |
| Hire Date | Operator | `BEN_ELIG_OPERATOR` | `Operator11` | Active |
| Hire Date | Alternate service-date source | `BEN_SVC_DT_TO_USE` | — | Declared only |
| Hire Date | Alternate equality-date control | `CMP_XPROPR_EQLTYDATE` | — | Declared only |
| Probation Period | Operator | `BEN_ELIG_OPERATOR` | `Operator11` | Active |
| Probation Period | Month | `CMP_MONTH` | `CritChar2` | Active |
| Probation Period | Day | `CMP_DATE` | `CritChar3` | Active |
| Probation Period | Units | `CHECKLIST_QUALIFYING_UNITS` | `CritChar4` | Active |
| Probation Period | Alternate equality-date control | `CMP_XPROPR_EQLTYDATE` | — | Declared only |
| Scheduled Hours | Frequency | `FREQUENCY` | `FreqCd` | Active |
| Scheduled Hours | Determination rule | `BEN_LOS_DET` | `DeterminationCd` | Active |
| Scheduled Hours | Rounding rule | `BEN_RNDG` | `RoundingCd` | Active |

`Declared only` means the `HcmLookupPVO` accessor exists in the model, but no
`ListBinding` in that model consumes it. It should not be treated as an active
workbook field without separate runtime evidence.

### Coverage and enrollment determination criteria

All of the following use `BEN_CVG_DET_DT` for their determination-date field:

| Criterion | Stored attribute |
|---|---|
| Covered by Another Plan | `CvgDetDtCd` |
| Covered by Another Plan in Program | `EnrlDetDtCd` |
| Covered by Another Plan Type | `EnrlDetDtCd` |
| Covered by Another Program | `EnrlDetDtCd` |
| Enrolled in Another Option | `EnrlDetDtCd` |
| Enrolled in Another Plan | `EnrlDetDtCd` |
| Enrolled in Another Plan in Program | `EnrlDetDtCd` |
| Enrolled in Another Plan Type | `EnrlDetDtCd` |
| Enrolled in Another Program | `EnrlDetDtCd` |

### User-defined criteria

User-defined criteria do not have a fixed lookup type. The definition stores
two selected lookup types:

- `COL1_LOOKUP_TYPE` supplies `CharValue1` and `CharValue2`.
- `COL2_LOOKUP_TYPE` supplies `CharValue3` and `CharValue4`.

The selectable lookup-type catalog comes from `FND_LOOKUP_TYPES_VL`, restricted
to `VIEW_APPLICATION_ID = 3`, through `HcmLookupTypeVVO`. The value LOVs then
bind the selected type dynamically and return `LookupCode` and `Meaning`.

### Supporting setup lookups

These are not stored directly on an eligibility-profile criterion row. They
belong to Benefits-owned objects that the criteria reference:

| Criterion dependency | HCM lookup type | Stored attribute |
|---|---|---|
| Service Area | `BEN_PRDCT` | `OrgUnitPrdct` |
| Postal Code Range | `BEN_PRDCT` | `ServiceTypr` |

### Declared accessors that are not active criterion LOVs

The following declarations were found in criterion models, but the same model
has no `ListBinding` that consumes them:

| Criterion | Declared lookup type | Active criterion value |
|---|---|---|
| Business Unit (`EBU`) | `BEN_YES_NO` | Business Unit object ID/name LOV |
| Job Family (`JFM`) | `BEN_YES_NO` | Job Family object ID/name LOV |
| Performance Rating | `BEN_ELIG_PERF_SOURCE` | Template, period, rating model, and rating level object LOVs |

These declarations are retained in the CSV for completeness and marked
`DECLARED_ONLY`.

### Deliberate exclusions

The scan also found HCM lookups in eligibility component models that are not
eligibility-profile criteria, so they are excluded from the criterion list:

- Profile header/search: `BEN_ASMT_TO_USE`, `BEN_BNFT_CAGR_PRTN`, `BEN_STAT`,
  and `BEN_ELIG_PRFL_PERS_TYPE`.
- Continuing Participation configuration: `BEN_TM_UOM`.
- Organization/union setup status: `ACTIVE_INACTIVE`.
- REST evaluation options: `BEN_TM_UOM`.
- HSA calculator plan type: `ORA_BEN_HSA_PLAN_TYPE`.

Country, state, city, business-unit, job-family, performance, and similar
object LOVs are not HCM lookup types. They resolve from territory, geography,
or product object views and are documented separately in the mapping
reference. The dependent relationship criterion is an exception: its
relationship code comes from HCM lookup type `CONTACT`.

### Validation rule for lookup-backed criteria

For every populated lookup-backed field, the workflow should:

1. Resolve the exact lookup type shown in this document.
2. Match the workbook value to `LookupCode`, not translated `Meaning`.
3. Confirm the code is enabled and effective on the criterion effective date.
4. Apply legislation and reference-data filters exposed by the target pod.
5. Fail on zero or ambiguous matches and report the workbook cell.
6. Send the validated `LookupCode`; never replace it with a numeric object ID.

<a id="rest-api-resolvers"></a>

## REST API Resolvers for Eligibility-Profile Mappings

### Outcome

Use the resolver resources below for target-pod ID resolution. They are
read-only dependencies of the Benefits load; the resulting IDs are then placed in
the Benefits eligibility-profile creation payload.

All populated mapping fields have an exact-ID resolver. Four mappings use
internal read-only contracts:

- `talentPerformanceTemplates` returns `TemplateDefnId` and exposes child
  `periods` with `TmplPeriodId`.
- `payrollGenericLOV`, with the seeded data source
  `BalanceGroupUI_DefinedBalanceSearchVO`, returns `DefinedBalanceId`.
- `absenceTypesLovV2` returns context-free setup rows with `AbsenceTypeId`;
  unlike the public worker LOV, its `findByWord` finder does not require a
  `PersonId`.
- `fastFormulaTypesLOV` resolves `FormulaTypeId`, which is then passed to
  `fastFormulas` to resolve the exact `FormulaId`.

These resources are marked `Visibility="unlisted"` in Fusion source or use a
secured internal generic data source. Treat them as release-sensitive internal
contracts: centralize their configuration, use GET only, and run the capability
and privilege preflight before any POST. A 403, 404, missing field, schema drift,
zero matches, or multiple matches is a hard stop. Never submit a source-pod ID.

### Verification status

- `LOCAL_AND_OFFICIAL`: already used by the current loader and also documented
  by Oracle.
- `OFFICIAL_EXACT_ID`: Oracle documents the collection, natural-key fields, and
  exact target ID returned.
- `OFFICIAL_EXACT_ID_CONTEXT`: the exact ID is returned, but another resolved
  ID or effective context is required.
- `INTERNAL_SOURCE_EXACT_ID`: Fusion source registers an unlisted/internal
  GET contract and exposes the exact target ID. It still requires a target-pod
  capability and privilege preflight because it is not a public compatibility
  contract.
- `INTERNAL_SOURCE_EXACT_ID_CONTEXT`: the same source-exact internal contract,
  with another resolved ID or enterprise/effective context required for an
  unambiguous match.
- `OFFICIAL_VALIDATION_ONLY`: the official resource validates a literal code;
  it does not resolve a foreign-key ID.

The same catalog is available for programmatic use in
`eligibility-profile-mapping-reference/mapping-reference.json:rest_api_resolvers`. Join it to criterion fields through
`eligibility-profile-mapping-reference/mapping-reference.json:criteria_resolver_links`; do not parse the human-readable `criteria`
column in the resolver catalog.

### Resolver catalog

All paths use the compatibility version `11.13.18.05`. Keep the version in
configuration; do not scatter it across loader code.

| Mapping | Status | GET collection | Exact match and disambiguation | Returned ID |
|---|---|---|---|---|
| Legal Employer, including nested Benefits Balance/Group references | `LOCAL_AND_OFFICIAL` | [`legalEmployersLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-legalemployerslov-get.html) | `Name` + `LegislationCode` + effective date | `OrganizationId` |
| Assignment Status | `OFFICIAL_EXACT_ID` | [`assignmentStatusTypesLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-assignmentstatustypeslov-get.html) | Prefer `AssignmentStatusCode`; validate `UserStatus`, `HRStatus`, and effective date | `AssignmentStatusTypeId` |
| Salary Basis | `OFFICIAL_EXACT_ID_CONTEXT` | [`salaryBasisLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-salarybasislov-get.html) | `finder=findByBasisCode;Code={code},EffectiveDate={date}`; validate `LegislativeDataGroupId` | `SalaryBasisId` |
| Person Type | `OFFICIAL_EXACT_ID` | [`personTypesLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-persontypeslov-get.html) | `UserPersonType` + `SystemPersonType`; active/default flags are validation fields | `PersonTypeId` |
| Business Unit | `OFFICIAL_EXACT_ID_CONTEXT` | [`hcmBusinessUnitsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-hcmbusinessunitslov-get.html) | Exact `Name`, active `Status`; pass `LegalEmployerId` to `findByWord` when supplied | `BusinessUnitId` |
| Job Family | `OFFICIAL_EXACT_ID` | [`jobFamiliesLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-jobfamilieslov-get.html) | `JobFamilyCode` + effective date; validate `JobFamilyName` and `ActiveStatus` | `JobFamilyId` |
| Payroll | `OFFICIAL_EXACT_ID_CONTEXT` | [`payrollDefinitionsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-payrolldefinitionslov-get.html) | `PayrollName` + `LegislativeDataGroupId` + effective date; use `PeriodType` if still ambiguous | `PayrollId` |
| Position | `OFFICIAL_EXACT_ID_CONTEXT` | [`positionsLovV2`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-positionslovv2-get.html) | `PositionCode` + `BusinessUnitId` + effective date; validate `PositionName` | `PositionId` |
| Work Location | `OFFICIAL_EXACT_ID_CONTEXT` | [`locationsLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-locationslov-get.html) | `LocationCode` + `SetId` + effective date; validate `LocationName` | `LocationId` |
| Job | `OFFICIAL_EXACT_ID_CONTEXT` | [`jobsLovV2`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-jobslovv2-get.html) | `JobCode` + `SetId` + effective date; validate `JobName` and, if supplied, `JobFamilyId` | `JobId` |
| Grade | `OFFICIAL_EXACT_ID_CONTEXT` | [`gradesLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-gradeslov-get.html) | `GradeCode` + `SetId` + effective date; validate `Name` and `ActiveStatus` | `GradeId` |
| Leaving / Termination Reason | `OFFICIAL_EXACT_ID` | [`actionsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-actionslov-get.html) | `ActionCode`; validate `ActionName`, `ActionTypeCode`, date, and termination context | `ActionId` |
| Organization Unit / Department | `OFFICIAL_EXACT_ID` | [`departments`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-departments-get.html) | Exact `Name` on the current date-effective collection row; avoid the contextual `departmentsLovV2` finder | `OrganizationId` |
| Collective Agreement | `OFFICIAL_EXACT_ID_CONTEXT` | [`collectiveAgreementsLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-collectiveagreementslov-get.html) | `IdentificationCode` + `LegalEntityId` or `LegislationCode` + effective date; validate name/union/bargaining unit | `CollectiveAgreementId` |
| Union | `OFFICIAL_EXACT_ID_CONTEXT` | [`unionsLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-unionslov-get.html) | Exact `UnionName` + `LegislationCode` + effective date; validate active `Status` | `OrganizationId` |
| Competency | `OFFICIAL_EXACT_ID_CONTEXT` | [`contentItemsLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-contentitemslov-get.html) | `finder=findActiveContentItemByDate` with competency `ContentTypeId`, active dates, and exact `Name`; catalog ID/code can disambiguate | `ContentItemId` |
| Qualification Type | `OFFICIAL_EXACT_ID` | [`contentTypesLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-contenttypeslov-get.html) | Exact `ContentTypeName`; validate `ContextName` | `ContentTypeId` |
| Qualification | `OFFICIAL_EXACT_ID_CONTEXT` | [`contentItemsLov`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-contentitemslov-get.html) | `finder=findActiveContentItemByDate` with qualification `ContentTypeId`, active dates, and exact `Name`; catalog ID/code can disambiguate | `ContentItemId` |
| Competency or Performance Rating Model | `OFFICIAL_EXACT_ID` | [`ratingModelsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-ratingmodelslov-get.html) | Prefer `finder=findByRatingModelCode`; validate `RatingName` | `RatingModelId` |
| Competency or Performance Rating Level | `OFFICIAL_EXACT_ID_CONTEXT` | [`ratingLevelsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-ratinglevelslov-get.html) | Exact `RatingLevelCode` within resolved `RatingModelId`; validate description/short description | `RatingLevelId` |
| Performance Template | `INTERNAL_SOURCE_EXACT_ID_CONTEXT` | Internal `talentPerformanceTemplates` | `finder=findByWord` for candidates; exact `Name` + document type + template type + active/effective dates | `TemplateDefnId` |
| Performance Template Period | `INTERNAL_SOURCE_EXACT_ID_CONTEXT` | Child `periods` of internal `talentPerformanceTemplates` | Resolve the parent first, then exact `CustomaryName` + `ShortName` + nominal dates; use `ReviewPeriodId` when supplied | `TmplPeriodId` |
| Hours Worked / Compensation Level Defined Balance | `INTERNAL_SOURCE_EXACT_ID_CONTEXT` | [`payrollGenericLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-payrollgenericlov-get.html) with internal `PayRestName=BalanceGroupUI_DefinedBalanceSearchVO` | Exact `BalanceName` + `DimensionName` + legislation or resolved LDG ID; map each `ResultKeyN` to its `ResultValueN` | `DefinedBalanceId` |
| Leave of Absence Type | `INTERNAL_SOURCE_EXACT_ID_CONTEXT` | Internal `absenceTypesLovV2` | `finder=findByWord` on `Name`; exact name + legislation/LDG + `Status` + effective range. No worker `PersonId` is required. | `AbsenceTypeId` |
| Leave of Absence Reason | `OFFICIAL_EXACT_ID_CONTEXT` | [`absenceTypeReasonsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-absencetypereasonslov-get.html) | `finder=findByAbsenceTypeId;AbsenceTypeId={id},StatusCd=A`; exact-match `Name` at the effective date | `AbsenceTypeReasonId` |
| Fast Formula type dependency | `INTERNAL_SOURCE_EXACT_ID` | Internal `fastFormulaTypesLOV` | `finder=FindByFormulaTypeName`; require one exact `FormulaTypeName` or `BaseFormulaTypeName` | `FormulaTypeId` |
| Fast Formula dependency | `INTERNAL_SOURCE_EXACT_ID_CONTEXT` | Internal `fastFormulas` | `finder=findByFilterCriteria` with exact formula name, resolved formula type, effective date, and LDG/legislation partition | `FormulaId` |
| Lookup-code validation for criteria classified `NOT_REQUIRED` | `OFFICIAL_VALIDATION_ONLY` | [`commonLookupsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-commonlookupslov-get.html) | `finder=LookupTypeFinder;LookupType={type}`, then exact lookup code; validate legislation/access. This validates a literal code and does not produce a mapping ID. | `LookupCode` |

### Internal resolver request recipes

The examples below show query templates, not values to concatenate directly.
Construct query parameters with an HTTP URL encoder. Escape all workbook data,
and preserve `||` as the generic Payroll multi-value delimiter (normally encoded
as `%7C%7C`).

#### Performance template and period

Find template candidates:

```text
GET /hcmRestApi/resources/11.13.18.05/talentPerformanceTemplates
    ?finder=findByWord;SearchTerms={templateName}
    &fields=TemplateDefnId,Name,DocumentTypeId,DocumentTypeName,DateFrom,DateTo,Status,TemplateTypeCode
    &onlyData=true
```

`findByWord` is candidate discovery only. Compare the returned `Name` exactly,
then require matching document type, template type, `Status='A'`, and a
`DateFrom`/`DateTo` range containing the workbook effective date.

After resolving `TemplateDefnId`, expand only that template's periods:

```text
GET /hcmRestApi/resources/11.13.18.05/talentPerformanceTemplates
    ?q=TemplateDefnId={templateDefnId}
    &expand=periods
    &fields=periods:TmplPeriodId,CustomaryName,ShortName,ReviewPeriodId,NominalFromDate,NominalToDate,AvailableToUseFlag
    &onlyData=true
```

Require one period whose `CustomaryName`, `ShortName`, nominal dates, and
optional `ReviewPeriodId` match. `AvailableToUseFlag` must be true. The GET
permission is supplied by `HRA_VIEW_PERFORMANCE_TEMPLATE_PRIV`; do not grant
the broader manage privilege merely to run this resolver.

#### Defined balance

Resolve the workbook LDG name to its target `LegislativeDataGroupId` first.
Then call the generic facade with its source-seeded VO:

```text
GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV
    ?finder=findByWord;PayRestName=BalanceGroupUI_DefinedBalanceSearchVO,AdditionalViewCriteria=SearchByLegCodeAndLdg,ParameterKeys=pLegislationCode%7C%7CpLegislativeDataGroupId,ParameterValues={legislationCode}%7C%7C{legislativeDataGroupId},SearchTerms={balanceName},FilterAttributes=BalanceName,DisplayAttributes=DefinedBalanceId%7C%7CBalanceName%7C%7CDimensionName%7C%7CLegislationCode%7C%7CLegislativeDataGroupId
    &onlyData=true
```

Pass the legislation and/or LDG value appropriate to the balance partition.
Build a dictionary from every returned `ResultKeyN`/`ResultValueN` pair; never
hard-code the numeric position of `DefinedBalanceId`. Require exact
`BalanceName`, `DimensionName`, and legislation/LDG context. The seeded source
requires the VBCS permission
`/vbcs/hcm/payroll-balance-groups/flows/manage-balance-group`.

#### Absence type

Use the setup LOV, not the public worker-context `absenceTypesLOV`:

```text
GET /hcmRestApi/resources/11.13.18.05/absenceTypesLovV2
    ?finder=findByWord;SearchTerms={absenceTypeName},FilterAttributes=Name
    &fields=AbsenceTypeId,Name,LegislationCode,LegislativeDataGroupId,Status,EffectiveStartDate,EffectiveEndDate
    &onlyData=true
```

Match `Name` exactly and require the correct legislation or LDG, active status,
and an effective range containing the workbook date. The internal finder has
only `SearchTerms` and `FilterAttributes`; it has no `PersonId` dependency.
Resolve the reason afterward with the documented `absenceTypeReasonsLOV` and
the resolved `AbsenceTypeId`.

#### Fast Formula

Resolve the formula type first:

```text
GET /hcmRestApi/resources/11.13.18.05/fastFormulaTypesLOV
    ?finder=FindByFormulaTypeName;FormulaTypeName={formulaTypeName}
    &fields=FormulaTypeId,FormulaTypeName,BaseFormulaTypeName
    &onlyData=true
```

The finder is prefix-based, so exact-match the returned formula type name. Then
pass its ID to the formula resolver:

```text
GET /hcmRestApi/resources/11.13.18.05/fastFormulas
    ?finder=findByFilterCriteria;FormulaName={formulaName},FormulaTypeId={formulaTypeId},EffectiveAsOfDate={effectiveDate},LegislativeDataGroupId={legislativeDataGroupId}
    &fields=FormulaId,FormulaName,FormulaTypeId,FormulaTypeName,LegislativeDataGroupId,LegislativeDataGroupName,LegislationCode,EffectiveStartDate,EffectiveEndDate,CompileStatus
    &onlyData=true
```

For a legislative formula, use `LegislationCode` instead of LDG; for a global
formula, omit both only when that is valid for its formula type. The formula
name finder also searches description, so exact-match every returned field and
require one effective row. `PAY_MANAGE_HCM_BUSINESS_RULE_PRIV` grants the source
REST permissions. If the workflow creates the formula in the same run, retaining the
creation response's `FormulaId` remains preferable to re-resolution.

### Important non-equivalences

- `ReviewPeriodId` from
  [`reviewPeriodsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-reviewperiodslov-get.html)
  is not `TMPL_PERIOD_ID` and cannot replace `TmplPeriodId`.
- `BalanceTypeId` from
  [`payrollBalanceDefinitionsLOV`](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-payrollbalancedefinitionslov-get.html)
  is not `DEFINED_BALANCE_ID`.
- `EligibilityObjectId` from `performanceTemplateDocumentNamesLOV` is not
  `TemplateDefnId`.
- Union uses the REST-returned `OrganizationId`; it does not resolve the package's separate
  `CRIT_NUMBER1`/`CRIT_CHAR1` inconsistency.

### Lookup resolution contract

#### Workbook keys

Names alone are not a reliable cross-pod key. Add the following columns to the
relevant Excel sheets when the object is used:

- `EffectiveDate` for every effective-dated reference.
- `LegislationCode`, `LegalEmployerName` or key, and
  `LegislativeDataGroupName` or key where applicable.
- `SetCode` for job, grade, location, and department references.
- Stable object codes: salary-basis code, job-family code, position code, job
  code, grade code, action code, collective-agreement identification code,
  rating-model code, and rating-level code.
- `ContentTypeName` plus content-item catalog code for competency and
  qualification references.
- Performance template name, document type, template type, and effective date;
  plus period customary name, short name, and nominal dates.
- Balance name, dimension name, legislation, and LDG for defined balances.
- Absence type name, legislation or LDG, and effective date.
- Formula name, formula type name, effective date, and LDG or legislation.

#### Resolution algorithm

1. Run a target-pod capability preflight for every distinct resolver used by
   the workbook. For internal resources, call `/describe` where permitted and
   a harmless GET. Confirm HTTP 200, the expected fields/finders, and the
   service account's required privilege.
2. Resolve parent/context IDs first: legal employer, LDG, set, content type,
   rating model, absence type, then child IDs.
3. Search with the stable code/finder when available. Apply an exact equality
   check locally to the returned rows; search text is only candidate discovery.
4. Include `fields` and `onlyData=true`. Candidate finders are often
   prefix/contains searches, so follow pagination until `hasMore=false`; an
   optimization may stop after finding two exact matches because ambiguity is
   already proved. A resolver succeeds only when exactly one active row across
   all searched pages matches every natural-key and effective-date field.
5. Zero matches, more than one match, inactive rows, a missing result field,
   or any internal resolver that fails capability/privilege preflight are hard
   validation failures. Report sheet, row, column, supplied key, endpoint, and
   candidates.
6. Cache only successful resolutions. Include pod, resolver key, normalized
   natural key, context IDs, and effective date in the cache key.
7. Send only the returned target ID to the create API. Never fall back to a
   source ID or silently select the first match.

#### Generic payroll result handling

`payrollGenericLOV` returns either `Code`/`Meaning` or generic
`ResultKeyN`/`ResultValueN` pairs. The workflow must build a name-to-value map from
those pairs; it must not assume, for example, that `ResultValue1` is always the
ID. Fusion implementation source preserves the requested `DisplayAttributes`
order when generating these pairs, but key-based parsing remains mandatory and
the preflight must confirm that `DefinedBalanceId` is present and numeric.

For this resolver, the target query and exact-match key is:

`BalanceName + DimensionName + (LegislationCode or LegislativeDataGroupId)`

The workbook can store the LDG name, but the workflow must resolve it to the target LDG
ID before querying. This is stronger than the old display string
`Balance Name - Dimension Name` and should be required in the workbook.

### Recommended implementation order

1. Add a centralized resolver registry populated from `eligibility-profile-mapping-reference/mapping-reference.json:rest_api_resolvers`
   and join criterion fields through `eligibility-profile-mapping-reference/mapping-reference.json:criteria_resolver_links`.
2. Implement the official exact-ID resolvers, then the four internal resolver
   flows above behind the same registry interface.
3. Add one preflight stage that batches distinct natural keys and rejects all
   unresolved or ambiguous values before any POST occurs.
4. Preflight all internal resources on the authenticated target pod and record
   observed availability, fields, finders, and privileges as pod-and-release
   capability data, not global assumptions.
5. Keep public alternatives only as validation/fallback candidates. They must
   not replace `TemplateDefnId`, `DefinedBalanceId`, or the context-free setup
   resolution contracts documented above.

<a id="eligibility-best-practices"></a>

## Eligibility profile best practices

Use the 30 runtime review practices below. Internal numbering BP-01 through
BP-30 identifies each check in import evaluation output.

### How to evaluate an import

Review the exact workbook used for the preview and
the supplied business requirements. Use the governed package inventory to
cross-check scope. Do not infer business intent solely from a profile name.

| Review area | Practices | Evidence and checks |
| --- | --- | --- |
| Population, usage, naming | BP-01–04 | Business purpose and target population; participant/dependent type; usage; consistent reusable names. |
| Assignment scope | BP-05 | Flag broad Any Assignment–Enterprise for explicit justification; request multiple-assignment test evidence. Do not replace it with an option unsupported by this converter. |
| Profile logic and attachment | BP-06–10 | Explain same-type OR and cross-type AND; check alternative paths and required/optional associations only when consumer configuration is available. |
| Criteria and dependencies | BP-11–15 | Prefer seeded criteria and derived factors; verify prerequisites, user-defined data contracts, and formula justification. Multiple formulas are a review recommendation, not an automatic import failure. |
| Inclusion, exclusions, row count | BP-16–20 | Flag mixed include/exclude values of the same type, repeated rows, unclear null behavior, and sequences. Recommend smaller equivalent sets only with population evidence. |
| Reuse and downstream impact | BP-21–24 | Identify candidate equivalent profiles and shared criteria in the workbook; require existing-profile and consumer evidence before claiming safe reuse or replacement. |
| Test and effective-date evidence | BP-25–29 | Expected versus actual person/assignment/date outcomes, boundaries, lifecycle, exclusions, nulls, and independent formula tests. Package validation and API success do not prove eligibility outcomes. |
| Ownership and design record | BP-30 | Owner, intent, consumers, assumptions, effective dates, dependencies, test cases, and change history. |

Record each finding with profile name, worksheet/row(s), practice number,
observed evidence, impact, recommendation, and disposition. Use **Pass** only
when evidence supports it, **Recommendation** for a design improvement,
**Needs evidence** for unverified intent/consumer/test information, and
**Not applicable** with a reason. Keep actual converter validation errors
separate. Do not invent severity scores or treat missing evidence as a pass.

BP-29 requires tested and approved expected/actual outcomes before activation
or migration. If that evidence is missing, say readiness is
unverified and ask for it before claiming best-practice readiness. Do not label
a successful import as proof that this requirement has been met.

Present the approval preview and every review finding in the user-facing
response before asking for import approval; links to saved artifacts are
supplemental, not a substitute for showing their contents. Identify the exact
target, operation, effective date, archive, profile inventory, setup-object
counts, finding disposition, evidence, impact, and recommended action. State
when source provenance or expected-versus-actual eligibility test evidence is
missing. Do not ask for approval when preview validation has failed.
Do not silently edit, rename, merge, exclude, or change assignment options in
the workbook. Proposed configuration changes need user direction and a new
preview. Evaluation does not authorize new live queries, UI tests, or imports:
use only supplied evidence and operations already selected by the workflow.
If a check requires unavailable consumer, target-profile, or person-test data,
record that gap and recommend the appropriate follow-up.

### Runtime practices

Eligibility Profiles provide a flexible way to define who qualifies for programs, plans, and processes, but thoughtful design is essential to keeping eligibility rules clear, reusable, and easy to maintain. This reference guide brings together practical best practices for designing, configuring, testing, and managing Eligibility Profiles It covers how to define target populations, select the appropriate profile usage and assignment, structure criteria and profile logic, and make effective use of seeded criteria, derived factors, user-defined criteria, and Fast Formulas. It also highlights important considerations for effective dating, profile reuse, validation, and ongoing maintenance. Whether you are creating a new eligibility rule or refining an existing configuration, these practices can help you build eligibility profiles that are easier to understand, validate, and manage over time.

| Design principle: Define the business population and rule first, then select the simplest configuration that represents it clearly. |
| --- |

#### Quick Reference

| Best practice | What it means |
| --- | --- |
| Purpose | Define and reuse consistent rules that identify people or dependents who qualify for a business process or offering. |
| Profile logic | Within one profile, multiple values of the same criterion type are OR; different criterion types are AND. |
| Profile reuse | Reuse a common profile when the same business rule applies. Avoid duplicating equivalent criteria across profiles. |
| Criteria selection | Use seeded criteria and derived factors first. Use user-defined criteria or Fast Formulas only when the requirement cannot be represented by standard functionality. |
| Assignment | Choose the assignment to evaluate based on the consuming business process, especially for workers with multiple assignments. |
| Validation | Test representative populations, boundaries, effective dates, and exception cases before activation or migration. |

### 1. Start with the Business Rule

<a id="bp-01"></a>

1. Define the purpose and target population.  Clearly define the eligibility profile's business purpose, target population, profile usage, and expected outcome before adding criteria.

<a id="bp-02"></a>

2. Choose the correct profile usage.  Set the profile usage to the business process where it will be used, such as Benefits, Compensation, Performance, Goals, or Checklist. Use Global only when the same profile is intentionally shared across multiple business processes.

<a id="bp-03"></a>

3. Separate participant and dependent profiles.  Use participant profiles for employees or workers. Use dependent profiles only when evaluating spouses, children, or other eligible dependents for Benefits plans or plan types.

<a id="bp-04"></a>

4. Use reusable, criteria-based names.  Name the profile for the eligibility rule rather than the object that uses it, for example, Age 20-25 and Non-Tobacco User rather than Supplemental Life Plan Eligibility. Apply a consistent naming standard that identifies the population or rule, profile usage, participant or dependent type, and, were useful, the country, legislative group, or effective period. Avoid naming a reusable profile solely after one plan or program.

<a id="bp-05"></a>

5. Choose the correct assignment to evaluate.  Carefully select Assignment to Use based on the business process consuming the eligibility profile, particularly for workers with multiple assignments. For active employee Benefits programs, generally use the employee's primary assignment or the applicable Benefits relationship assignment. For profiles used outside Benefits, select the specific assignment option required by the consuming product. Avoid broad options such as Any Assignment - Enterprise unless the business requirement explicitly requires evaluation across all assignments. Evaluating unnecessary assignments can increase processing time and may produce unexpected eligibility results. Validate the selected assignment option using workers with primary, secondary, inactive, suspended, and Benefits-related assignments. Do not assume that the default assignment selection is appropriate for every use case.

#### Example: A clear reusable rule

Example business rule: Employees in Florida who are salaried and active as of the effective date qualify for a defined Benefits offering.

The profile should express that rule through the appropriate participant criteria and effective-dated setup, rather than being named only for the plan that happens to consume it.

### 2. Structure Profile Logic Carefully

<a id="bp-06"></a>

6. Use one profile when the criteria form one rule.  Use a single profile when the conditions form one eligibility rule.

<a id="bp-07"></a>

7. Use multiple profiles for alternative qualification paths.  Attach separate profiles when the object needs alternative paths, such as Executive employees OR employees in a specific bargaining unit. Separate profiles are also appropriate when rules need to be reused independently or when some profiles must be required and others optional.

<a id="bp-08"></a>

8. Understand AND OR behavior.  Within one profile, multiple values of the same criterion type are evaluated as OR; different criterion types are evaluated as AND. Example: (Toronto OR Ottawa) AND Full-time employee belongs naturally in one profile.

<a id="bp-09"></a>

9. Use Required and Optional deliberately.  When multiple profiles are attached, mark a profile as Required when every eligible participant must satisfy it. Participants must satisfy all required profiles. Optional profiles represent alternative qualification paths. When required and optional profiles are attached, the participant must satisfy all required profiles and at least one optional profile. When all attached profiles are optional, the participant must satisfy at least one. When only one profile is attached, the participant must satisfy that profile regardless of whether Required is selected.

<a id="bp-10"></a>

10. Confirm the consuming object's profile limit.  Before deciding between one or multiple profiles, confirm whether the target object supports multiple eligibility profiles. Some objects, including checklist tasks, variable rate and coverage profiles, total compensation statements, and absence types, accept only one profile; Benefits offerings, compensation plans, performance documents, goal plans, and absence plans can accept multiple profiles.

#### Multiple-profile behavior

| Configuration | Result |
| --- | --- |
| Required profiles | The participant must satisfy all required profiles. |
| Required + optional | The participant must satisfy all required profiles and at least one optional profile. |
| All optional | The participant must satisfy at least one optional profile. |
| Single attached profile | The participant must satisfy the profile whether or not Required is selected. |

### 3. Select Criteria at the Right Level

<a id="bp-11"></a>

11. Create prerequisites first.  Create and validate any derived factors, user-defined criteria, and Fast Formulas before building the eligibility profile that references them.

<a id="bp-12"></a>

12. Use seeded criteria first.  Use seeded criteria first for worker type, assignment status, legal employer, location, job, grade, hours, age, service, and dependent relationship.

<a id="bp-13"></a>

13. Use derived factors for supported calculations.  Use derived factors for age, length of service, compensation, hours worked, full-time equivalent, or age-and-service combinations rather than reproducing these calculations in formulas.

<a id="bp-14"></a>

14. Use user-defined criteria for organization-specific attributes.  Use user-defined criteria for reusable organization-specific attributes that seeded criteria and derived factors cannot represent. Document the source, data type, value set, null handling, ownership, and effective-dating behavior of the underlying data.

<a id="bp-15"></a>

15. Use Fast Formula only when necessary.  Use seeded eligibility criteria and derived factors before using a Fast Formula. Use a Fast Formula only when the required calculation, derived value, or business rule cannot be supported by standard eligibility functionality. Where practical, use no more than one eligibility Fast Formula in a profile. Consolidate closely related logic into one clearly documented formula with explicit return paths. Using multiple formulas in the same profile can make the combined outcome difficult to understand and may complicate testing, troubleshooting, and maintenance. When a formula is required, explicitly control every return path; document input values, defaults, null handling, and expected results; test the formula independently using the Fast Formula testing capability; test positive, negative, boundary, null-data, and effective-dated scenarios; and validate the final result through the eligibility profile evaluation UI and diagnostics.

| Rule of thumb  Prefer the most standard representation that expresses the business rule clearly: seeded criterion, then derived factor, then user-defined criterion, and finally Fast Formula when required. |
| --- |

### 4. Keep Criteria Clear and Maintainable

<a id="bp-16"></a>

16. Choose inclusion or exclusion deliberately.  For each criterion type, use either included values or excluded values whenever possible. Avoid mixing included and excluded values for the same criterion type because the resulting population can be difficult to interpret, validate, and maintain. For example, if 100 jobs exist and 80 should be eligible, either include the 80 eligible jobs or exclude the 20 ineligible jobs. Choose the approach that uses fewer rows and produces the clearest rule. When values are included, values not listed are normally treated as ineligible. When values are excluded, the remaining values are normally treated as eligible. Clearly document the intended treatment of blank, null, inactive, and unmapped values.

<a id="bp-17"></a>

17. Use the simpler row set.  When inclusion and exclusion approaches produce the same population, choose the approach that requires fewer rows and is easier to understand. Do not reduce the number of rows at the expense of clarity or correctness.

<a id="bp-18"></a>

18. Document blank, null, inactive, and unmapped values.  Clearly define the intended treatment of missing or unmapped data so the profile behaves predictably as workforce data changes.

<a id="bp-19"></a>

19. Assign criterion sequence deliberately.  Assign criterion sequence numbers deliberately and consistently. The system uses sequence numbers to determine the evaluation order of criteria of the same type, which can also make logs and troubleshooting easier to interpret. Do not rely on sequence to replace correctly designed AND/OR logic.

<a id="bp-20"></a>

20. Minimize unnecessary criteria rows.  Design eligibility profiles using the smallest practical number of criteria rows. When inclusion and exclusion approaches produce the same population, use the approach that requires fewer rows and is easier to understand. Do not reduce the number of rows at the expense of clarity or correctness. The selected approach must remain understandable to administrators and produce deterministic results. Large or unnecessarily repetitive criteria sets can increase configuration effort, complicate diagnostic output, and add processing overhead during eligibility evaluation and event processing.

### 5. Reuse, Placement, and Impact

<a id="bp-21"></a>

21. Search for an existing reusable profile before creating a new one.  Before creating a new profile, search for an existing reusable profile that represents the required population. Reuse common profiles for common rules such as active employment, legal employer, assignment status, location, job population, or service requirements.

<a id="bp-22"></a>

22. Avoid duplicating equivalent criteria.  Do not duplicate the same eligibility criteria across multiple profiles. Create reusable profiles for common rules such as active employment, legal employer, assignment status, location, job population, or service requirements and associate those profiles with the appropriate consuming objects rather than recreating the criteria. Duplication increases configuration and evaluation overhead, creates inconsistent results when one copy is changed and another is not, makes testing and troubleshooting more difficult, and increases the risk that different profiles represent what should be the same business rule. When reuse is not appropriate, document why a separate profile is required.

<a id="bp-23"></a>

23. Perform impact analysis before changing a shared profile.  Before changing, copying, or replacing an eligibility profile, identify all objects that currently consume it. Determine whether the proposed change applies to every consuming object. When only one consumer requires different behavior, create a separate profile rather than modifying the shared profile. Do not duplicate an existing profile solely to associate the same criteria with another object. Reuse common profiles whenever the same eligibility rule applies. Maintain a record of the profile's consuming objects and review downstream impact before promoting any change.

<a id="bp-24"></a>

24. Attach profiles at the highest appropriate reusable level.  Attach an eligibility profile at the highest appropriate reusable level after confirming inheritance, scope, and downstream impact. Do not repeat identical criteria in profiles attached at multiple levels. Define common population rules in separate reusable profiles and associate them with the applicable programs, plans, options, rates, tasks, or processes. For example, maintain a common active-employee profile separately rather than recreating the same active-assignment criteria in multiple plan-specific profiles. Before placing a shared profile, confirm whether the consuming object supports multiple profiles, whether the profile is required or optional, whether inherited eligibility applies, which effective date the consumer uses, and whether all consumers require the same rule.

#### Before reusing or changing a profile, confirm

All current consuming objects

Whether the consuming object supports multiple profiles

Whether each profile is Required or Optional

Whether inherited eligibility applies

Which effective date the consumer uses

Whether all consumers require the same rule

### 6. Test Before Activation or Migration

<a id="bp-25"></a>

25. Test by person, assignment, and effective date.  Test representative workers against the eligibility profile using the available Eligibility Evaluation UI and diagnostic tools. Validate the profile and criteria evaluated, the assignment selected for evaluation, the result of each criterion, inclusion and exclusion outcomes, blank, null, and unmapped-value behavior, derived-factor results, Fast Formula results, and the final eligibility determination. Use the generated eligibility logs and diagnostics to determine whether an unexpected result is caused by profile logic, assignment selection, source data, effective dating, derived factors, or formula behavior. Test each Fast Formula independently before validating it through the eligibility profile.

<a id="bp-26"></a>

26. Test boundary and lifecycle conditions.  Test null or missing data, exact age and service boundaries, hires, rehires, transfers, terminations, future-dated changes, multiple assignments, and dependents aging out, not only straightforward eligible and ineligible cases.

<a id="bp-27"></a>

27. Validate effective-dated behavior.  Confirm the effective date used by the consuming process before testing or changing a profile. Test the profile before, on, and after the effective date of relevant worker, assignment, organizational, or dependent changes. Avoid overwriting an existing rule when a future-dated rule or separate profile is required.

<a id="bp-28"></a>

28. Test formulas independently when used.  When a formula is required, explicitly control every return path; document input values, defaults, null handling, and expected results; test the formula independently using the Fast Formula testing capability; test positive, negative, boundary, null-data, and effective-dated scenarios; and validate the final result through the eligibility profile evaluation UI and diagnostics.

<a id="bp-29"></a>

29. Record expected and actual results.  Do not activate or migrate an eligibility profile until expected results have been documented, tested, and approved. Use the eligibility evaluation UI, generated logs, and available diagnostics to validate eligible and ineligible participants, included and excluded populations, primary and secondary assignments, multiple-assignment workers, null, blank, and unmapped values, boundary conditions, hires, rehires, transfers, and terminations, future-dated changes, dependent scenarios, Fast Formula results, and effective dates before, on, and after a relevant change. Record the expected and actual outcome for each test case. Resolve unexplained differences before activating or migrating the profile.

#### Validation checklist

| Area | What to validate |
| --- | --- |
| Population | Eligible and ineligible participants are confirmed. |
| Assignments | Primary, secondary, inactive, suspended, and Benefits-related assignments are covered as applicable. |
| Data values | Included, excluded, blank, null, inactive, and unmapped values are tested. |
| Boundaries | Relevant age, service, effective-date, and other threshold boundaries are tested. |
| Lifecycle | Hires, rehires, transfers, terminations, future-dated changes, and dependent scenarios are covered as applicable. |
| Diagnostics | Eligibility evaluation output and available logs/diagnostics explain the final determination. |

### 7. Document Ownership and Design Intent

<a id="bp-30"></a>

30. Maintain design documentation.  Record the business owner, functional owner, profile usage, consuming objects, criteria logic, formula names, derived factors, assumptions, effective dates, test cases, and change history. This is particularly important for reusable and formula-based profiles.

| Customer-ready outcome A well-designed Eligibility Profile makes the intended population easy to explain, the configuration easy to validate, and the rule safe to reuse as business requirements evolve. |
| --- |

Oracle Benefits | Eligibility Profiles Best Practices
