# Input Validation

## CSV Column Intent Resolution

| CSV Column | User Intent |
|---|---|
| PJF_RATE_SCHEDULE.csv.RateScheduleName | Rate Schedule Name |
| PJF_RATE_SCHEDULE.csv.Description | Rate Schedule Description |
| PJF_RATE_SCHEDULE.csv.ScheduleType | Schedule Type |
| PJF_RATE_SCHEDULE.csv.SetCode | Reference Data Set |
| PJF_RATE_SCHEDULE.csv.SetCode1 | Job Set when Schedule Type is Job |
| PJF_RATE_SCHEDULE.csv.CurrencyCode | Currency |
| PJF_RATE_SCHEDULE_TRANSLATION.csv.PJF_RATE_SCHEDULE.RateScheduleName | Parent Rate Schedule Name for the translation |
| PJF_RATE_SCHEDULE_TRANSLATION.csv.RateScheduleName | Translated Rate Schedule Name |
| PJF_RATE_SCHEDULE_TRANSLATION.csv.Language | Translation Language |
| PJF_RATE_SCHEDULE_TRANSLATION.csv.SourceLang | Translation Source Language |
| PJF_RATE_SCHEDULE_TRANSLATION.csv.Description | Translated Description |
| PJF_RATE_SCHEDULE_LINE.csv.EmailAddress | Person work email resolved with PersonNumber when Schedule Type is Person; required by the observed FSM import contract for this target |
| PJF_RATE_SCHEDULE_LINE.csv.JobCode | Person Job Code when Schedule Type is Person |
| PJF_RATE_SCHEDULE_LINE.csv.PersonJobName | Person Job Name when Schedule Type is Person |
| PJF_RATE_SCHEDULE_LINE.csv.SetCode | Person Job Set Code when Schedule Type is Person |
| PJF_RATE_SCHEDULE_LINE.csv.Name | Person Organization when Schedule Type is Person |
| PJF_RATE_SCHEDULE_LINE.csv.JobCode1 | Job Code when Schedule Type is Job |
| PJF_RATE_SCHEDULE_LINE.csv.JobName | Job Name when Schedule Type is Job |
| PJF_RATE_SCHEDULE_LINE.csv.SetCode1 | Job Set Code when Schedule Type is Job |
| PJF_RATE_SCHEDULE_LINE.csv.ExpenditureTypeName | Expenditure Type when Schedule Type is Nonlabor |
| PJF_RATE_SCHEDULE_LINE.csv.NlrName | Nonlabor Resource when Schedule Type is Nonlabor |
| PJF_RATE_SCHEDULE_LINE.csv.Name1 | Organization when Schedule Type is Nonlabor |
| PJF_RATE_SCHEDULE_LINE.csv.Name2 | Resource Class when Schedule Type is Resource Class |
| PJF_RATE_SCHEDULE_LINE.csv.Name3 | Organization when Schedule Type is Resource Class |
| PJF_RATE_SCHEDULE_LINE.csv.StartDateActive | Rate Line Start Date |
| PJF_RATE_SCHEDULE_LINE.csv.RateScheduleName | Parent Rate Schedule Name |
| PJF_RATE_SCHEDULE_LINE.csv.ProjectRoleName | Project Role when Schedule Type is Project Role |
| PJF_RATE_SCHEDULE_LINE.csv.EndDateActive | Rate Line End Date |
| PJF_RATE_SCHEDULE_LINE.csv.MarkupPercentage | Markup Percentage for the applicable rate-line type |
| PJF_RATE_SCHEDULE_LINE.csv.Rate | Rate Amount |
| PJF_RATE_SCHEDULE_LINE.csv.RateUnit | Rate Unit of Measure code resolved from supplied UOM name/code through resolve_rate_uom, or the applicable subtype derivation/default |
| PJF_RATE_SCHEDULE_LINE.csv.PersonNumber | Person identity by supplied person number or resolved Person display name when Schedule Type is Person; serialize with EmailAddress for the observed FSM import contract |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveStartDate | Person Effective Start Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveEndDate | Person Effective End Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveStartDate1 | Person Job Effective Start Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveEndDate1 | Person Job Effective End Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveStartDate2 | Person Organization Effective Start Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveEndDate2 | Person Organization Effective End Date |
| PJF_RATE_SCHEDULE_LINE.csv.SetCode2 | Person Organization Set |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveStartDate3 | Job reference effective-start date when Schedule Type is Job |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveEndDate3 | Job reference effective-end date when Schedule Type is Job |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveStartDate4 | Nonlabor Resource Organization Effective Start Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveEndDate4 | Nonlabor Resource Organization Effective End Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveStartDate5 | Resource Class Organization Effective Start Date |
| PJF_RATE_SCHEDULE_LINE.csv.EffectiveEndDate5 | Resource Class Organization Effective End Date |

## Input Interpretation

Resolve the intent table before validation. The source-proven aliases distinguish person job, job-schedule job, person organization, nonlabor organization and resource-class organization. Date pairs 0–5 identify reference slices; StartDateActive/EndDateActive identify rate-line dates. Accept resolvable multilingual/natural-language input; serialize only the canonical code or display name documented by ora_reference_lookups.md.

For Person input by display name, run `resolve_person_identity` before resolved-line validation and populate `PersonNumber` and `EmailAddress` from the unique `publicWorkers` match. The name is lookup input, not a CSV `PersonName` column; `Name` remains the Person Organization column. Do not require manually supplied PersonNumber or EmailAddress when name resolution succeeds. The FSM import observed on CPTCXCSQY returned `JBO-27035: Attribute Email is required` for a Person line without EmailAddress, and `PJF_FSM_DUPL_PERSON_EMAIL` for a shared WorkEmail. Therefore a blank or non-unique WorkEmail blocks the affected package until a supported unique identity is supplied.

For supplied UOM intent, `resolve_rate_uom` owns name/code resolution. Apply subtype defaults only when the UOM is omitted; retain Nonlabor expenditure-type UOM derivation and compare any explicit Nonlabor UOM to that derived code instead of silently replacing either value. CSV `RateUnit` contains the resolved code, not a class code or display meaning. A successful reference GET does not prove a REST payload field writable.

Missing LOV authority or unverified eligibility parity is REFERENCE_UNRESOLVED, Warning, blocking=false. Preserve the supplied proven representation, disclose skipped checks and continue all supported checks and preview without waiver. This does not convert known invalidity, actual ambiguity, failed supported reads or missing mutation approval/capability into warnings.

## Validation Phase Contract

| Phase | Checks Owned Here | Deferred Checks |
|---|---|---|
| RATE.VALIDATE_INPUT | Raw request/line shape, operation, unconditional create name/set/currency presence, supplied amount/date syntax and supplied-field shape | Do not require new-line From Date, omitted new-header type, canonical identities, derived Job pair/UOM, or parent-flag-dependent rules before defaults/lookups |
| RATE.VALIDATE_LINES | Apply Required Groups to resolved values; subtype identity, date order, Amount Presence Contract, optional-field compatibility with the resolved type, resolved UOM and selected schema conformance | Do not repeat raw-shape checks; business overlap/history/consumer/route policies run at their owning later nodes |

Required Groups and Field Validation below are evaluated at RATE.VALIDATE_LINES unless explicitly included in the raw phase above. A missing date on a new line is defaultable input, not an early validation error. For update, omission preserves the existing row; explicit clearing of a required value is not omission. This phase division is binding even though both nodes read the same source file.

For an existing-line update, merge the explicit delta onto the independently verified baseline before applying the resolved contract. An omitted field inherits its current value; explicit null/empty/whitespace requests clearing. Thus an end-date-only update keeps its existing amount and From Date, while explicitly clearing both amounts or the required From Date fails the proposed-row contract. Create defaults apply only to newly added lines, never to omitted or explicitly cleared fields on an existing line. No missing baseline may be replaced with an empty row.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create, update, copy, end_date, delete, validate, export, import | Block | Supply explicit intent | Every request |  |
| Header identity | ProjectRatesSetCode/CSV SetCode, RateScheduleName, ScheduleType | Block missing name/set; new omitted type uses ora_defaulting_rules.md | Resolve supplied intent to one scoped identity; no exact-English requirement | Every write | find_rate_schedule |
| Header values | CurrencyCode; JobSetCode when resolved type is JOB | Block create for missing currency or Job Set | Resolve the supplied job set; preserve existing values on update | Create/update | resolve_rate_references |
| Optional header values | Description and discovered DFFs only when supplied | Do not block or ask for Description/DFFs | Preserve omitted update fields; validate supplied DFFs against the selected request contract | Create/update |  |
| Lines | Subtype identity and amount contract below; StartDateActive after defaulting; optional EndDateActive; resolved RateUnit for CSV | Preserve omitted group; missing date on a new line uses ora_defaulting_rules.md | Supply explicit line diff; validate resolved line values at RATE.VALIDATE_LINES | Line change | resolve_rate_lines |
| Route/target | TargetEnvironment, REST discovery, current baseline, optional FSM template | Block | Discover/select route before preview | Every write | verify_rate_route |
| Mutation approval | Immutable preview and checksum-bound approval through the selected core workflow | Block execution | Reuse the selected core approval gate; do not add a second approval | Every write | verify_rate_route |
| Protected-use evidence | Scoped use_state and operation eligibility | Block affected mutation if missing | Resolve applicable existing consumer protection; new create does not require proof of historical use | Protected existing-row mutation/delete only | resolve_rate_use |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Selected route is REST and covers operation and all fields | direct_writable_rest capability | Hand off to selected Data Loader adapter before REST preview | verify_rate_route |
| Selected route is FSM and exact package contract proven | fsm_csv | Build FSM preview even if REST capability also exists; never switch after approval | verify_rate_route |
| Job schedule | Conditional | Require one current job set and jobs from it | resolve_rate_references |
| Person/nonlabor/resource-class detail supplied | Conditional | Enforce dependent key hierarchy and precedence | resolve_rate_lines |
| Used schedule/line mutation or delete | Conditional | Require zero-conflict use evidence | resolve_rate_use |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Schedule Type resolves to a seeded member | Accept code, meaning or unambiguous user intent; reject only after complete static authority check | Every write | resolve_schedule_type |
| Required resolved subtype identity | Require the identity in UI Header and Line Contract; optional qualifiers remain optional | RATE.VALIDATE_LINES after reference resolution |  |
| StartDateActive <= EndDateActive when end supplied | Equal dates accepted; reversed dates block with the observed message in ora_error_handling.md | RATE.VALIDATE_LINES; same-key overlap is owned by ora_design_enforcement.md |  |
| Rate/Markup presence and exclusivity | Apply Amount Presence Contract; zero is present, not blank; never fill an absent amount with zero | RATE.VALIDATE_LINES after type and applicable parent flag resolution |  |
| Amount representation | Accept a finite numeric value or a resolvable percentage expression; normalize 32.25% to 32.25 percentage points, not 0.3225; preserve zero | Supplied amounts; numeric sign/precision/ranges require selected-route metadata, not UI inference |  |
| RateUnit and selected route fields | Serialize only resolved route-supported values; an unavailable UI field is not proof of import rejection | RATE.VALIDATE_LINES after references; missing parity warns, missing writable contract blocks the affected write | resolve_rate_lines |
| Resource Class canonical representation | Resolve seeded member and write its meaning/name in Name2, never code or ID | RESOURCE_CLASS line | resolve_resource_class |
| Translation language shape | Language and SourceLang are respective Oracle codes, required for supplied translation rows, maximum four characters; do not require equality | Translation row supplied | resolve_translation_language |
| Exported CSV coverage | Use exactly the selected fresh template's members and columns; observed shape was 6 header, 5 translation and 34 line columns, not a permanent count constant | FSM CSV selected; metadata-only template and empty baseline are valid |  |
| UI-only Rate Required | No CSV column; do not serialize flag or assume UI read-only Rate proves an import rejection | Nonlabor line | record_unresolved_rate_reference |
| Unresolved prose | Do not fabricate an ID/code/name; ask only if missing representation prevents a supported payload | An unresolved value cannot be serialized safely | record_unresolved_rate_reference |

## UI Header and Line Contract

The developer's UI observations and saved manual cases from 2026-10-14 are the source of this contract. Header asterisks establish Name, Project Rates Set, Schedule Type and Currency as required UI fields; omission errors for each header field were not individually captured. Description is optional. Do not add purpose, ownership or Task Owning Organization to the Fusion required-input contract. Static label/code mappings are owned by ora_reference_lookups.md. Validate raw shape at RATE.VALIDATE_INPUT; after defaults and lookups, validate this contract at RATE.VALIDATE_LINES. These observations describe the UI, not a tested REST/FSM payload contract.

| Schedule Type | Required Identity | Optional Qualifiers | Unit of Measure Behavior | Amount Contract |
|---|---|---|---|---|
| EMPLOYEE | Person | Job, Job Code, Expenditure Organization | Hours displayed; derivation owned by ora_defaulting_rules.md | EMPLOYEE row below |
| JOB | Job Set on header and one resolvable Job Name or Job Code per line | To Date | Hours displayed; selecting one job identifier derives its pair through ora_reference_lookups.md | JOB row below |
| PROJECT_ROLE | Project Role | To Date | Hours displayed | PROJECT_ROLE row below |
| NON-LABOR | Expenditure Type | Nonlabor Resource, Nonlabor Resource Organization | Derived from the selected expenditure type; Rate Required is display-only | NON-LABOR Y/N rows below |
| RESOURCE_CLASS | Resource Class and resolved Unit of Measure | Organization, To Date | Labor/Equipment use the supported Hours default; other classes have configurable UOM, including observed Currency and Each | RESOURCE_CLASS row below |

All new lines need a From Date after defaulting. Preserve explicit dates, including historical dates. Job Name and Job Code refer to one identity; do not request both independently. Optional qualifiers, if supplied, still require their supported parent relationship. Do not infer that every field visible in one subtype exists in all subtypes.

## Amount Presence Contract

Blank means absent, null, empty text or whitespace; numeric zero is a supplied value. A zero value is not proven eligible by this UI run: apply any evidenced route range/sign constraints separately. Validate both amounts without deleting user data. No generic exactly-one or at-least-one rule applies to all types.

| Schedule Type | Rate Required Flag | Rate Only | Markup Only | Both Supplied | Both Blank |
|---|---|---|---|---|---|
| EMPLOYEE | Not applicable | Accept presence | Accept presence | UI entering one clears the other after Tab; unordered batch input needs the user's amount choice before preview, never silent last-value-wins | Reject; PJF-2235533 observed |
| JOB | Not applicable | Required | Reject; Rate missing and Markup not exposed | Reject unsupported Markup for this UI-equivalent contract; do not silently drop it | Reject; generic Rate-required message observed |
| PROJECT_ROLE | Not applicable | Required | Reject; Rate missing and Markup not exposed | Reject unsupported Markup for this UI-equivalent contract; do not silently drop it | Reject; Rate attribute message observed |
| RESOURCE_CLASS | Not applicable | Accept presence | Accept presence | Accept both; both remained populated and persisted | Reject; PJF-2235533 observed |
| NON-LABOR | Y | Accept presence | Accept presence; checked flag does not force Rate | UI entering one clears the other; unordered batch input needs the user's amount choice before preview | Reject; PJF-2235533 observed |
| NON-LABOR | N | Rate input unavailable in UI; require independent route evidence for a non-UI operation | Required in UI | Rate input unavailable; do not discard Rate or assume import rejection from UI alone | Reject; PJF-2235133 and PJF-2235533 both observed |

An unknown Nonlabor flag is not N. With a supplied Rate or Markup, preserve the representation and disclose the unresolved branch; do not fabricate a flag. Both amounts blank fail regardless of flag. Both supplied without explicit UI editing intent require clarification, not an invented editing order. The exact Oracle messages and their scope are owned by ora_error_handling.md; do not claim Oracle emitted them during offline validation.

## REST Header and Rate Line Contract

Treat request schemas as specific to the operation, endpoint, schedule subtype, and target runtime context. Oracle 26C's collection POST page lists subtype-specific flat attributes, while its task examples create rates using the `Rates` child. The published generic child schema shows Job attributes and is not a complete Resource Class contract. Resolve these differences with target operation metadata before approval; never infer permission to POST from a GET row.

| Payload scope | Fields and rules | Evidence required |
|---|---|---|
| Header POST /fscmRestApi/resources/11.13.18.05/rateSchedules | Schedule identity, optional Description, project rates set, currency, and ScheduleTypeCode resolved by the single Schedule Type authority in ora_reference_lookups.md; do not infer codes from display names. | Exact target header-create contract, including supported code/ID alternatives and required fields |
| Resource Class line POST /fscmRestApi/resources/11.13.18.05/rateSchedules/{RateScheduleId}/child/Rates | Resource class selector, Rate and/or MarkupPercent according to Amount Presence Contract, StartDateActive, optional EndDateActive, supported UOM and organization selectors. Resolve the parent ID from the header result or an exact existing identity. | Exact Resource Class child-create contract; a generic Job schema is insufficient |
| Resource class selector | Oracle documents ResourceClassName and RateClassId; the latter is a string. Do not invent ResourceClassId, hard-code class IDs, or substitute an ID after rejection without discovering that request contract. | Exact effective reference match and write eligibility at the selected endpoint |
| Display and response attributes | Do not copy GET rows wholesale. Exclude audit fields, links, @context, returned IDs, and response-only display values. CurrencyName, ScheduleTypeName, UOM names/codes and class names are included only when the selected target request accepts/requires them. | Per-field request evidence, not mere presence in a GET response |
| Flat create or nested Rates deep insert | Neither shape is established merely by the public discriminator schema. Do not place ResourceClassName, RateClassId, Rate, dates or UOM at the root unless this exact target root-create contract supports them. Do not invent a nested Rates array. | Explicit target support for the complete requested shape |

The normal candidate for a new Resource Class schedule is a header followed by a child rate. The following examples illustrate the separation only; they are not target-validated payloads or authorization to submit. Discover required alternatives before filling the final preview.

Header candidate:

```json
{
  "RateScheduleName": "FSCR_RESOURCE_RATES_TEST_0916",
  "Description": "Resource class planning rates",
  "ProjectRatesSetCode": "Vision Corporation 202",
  "CurrencyCode": "USD",
  "ScheduleTypeCode": "RESOURCE_CLASS"
}
```

Resource Class child candidate (to the returned header's `Rates` collection):

```json
{
  "ResourceClassName": "Labor",
  "Rate": 100,
  "StartDateActive": "2026-09-16",
  "UnitOfMeasureName": "Hours"
}
```

Omit organization selectors for an unrestricted line and omit the end date for an open-ended line. Preserve the user's description/date and resolve the actual set/class/UOM; the examples must not default business values. If target metadata does not establish both operations, return missing capability evidence or select a proven FSM contract before preview. Do not create an orphan header to probe child capabilities.

## Public REST References

Checked 2026-09-16 against Oracle Fusion Cloud Project Management 26C:

- [Create a rate schedule](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-rateschedules-post.html): discriminator-specific request schemas, field types, and header constraints.
- [Manage Rates for Rate Schedules](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/manage_rates_for_rate_schedules.html): separate child POST examples, including Resource Class name and UOM name.
- [Create a Rates child](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-rateschedules-ratescheduleid-child-rates-post.html): child operation; the generic Job schema must not be applied to other subtypes without target evidence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE.VALIDATE_INPUT | step | 1 | validate_input | valid->RATE.APPLY_DEFAULTS;warning->RATE.APPLY_DEFAULTS;invalid->RATE.RETURN_ISSUES | none | stop | Raw phase only per Validation Phase Contract; never demand defaultable or reference-derived values before their nodes |
| RATE.VALIDATE_LINES | step | 5 | validate_input | valid->RATE.ROUTE_OPERATION;warning->RATE.ROUTE_OPERATION;invalid->RATE.RETURN_ISSUES | RATE.RESOLVE_LINES | stop | Validate resolved header/subtype/amount/date values; defaults and references precede this gate |
| RATE.ROUTE_OPERATION | decision | 6 | evaluate_result | supported->RATE.RESOLVE_DEPENDENCIES;warning->RATE.RESOLVE_DEPENDENCIES;unsupported->RATE.RETURN_REFUSAL;invalid->RATE.RETURN_ISSUES | RATE.VALIDATE_LINES | stop | After supported checks; missing LOV authority alone is warning, not unsupported operation |
