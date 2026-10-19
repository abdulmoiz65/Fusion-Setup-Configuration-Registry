# Absence Type Display Features and Rules

This reference defines the Display Features and Rules behavior for Absence Types. It is reverse-engineered from the Absences UI implementation named at the end of this document. It augments, and does not replace, the main Absence Types workflow.

## Scope and required inputs

This covers only the Display Features and Rules tabs. It does not authorize plans, reasons, certifications, formulas, eligibility, security, enrollments, or worker absences. Do not infer configuration from the type name.

Before a save, obtain or confirm the target environment, Absence Type ID or name, legislation, pattern, effective date, operation (`create`, `update`, or `correct`), every persona setting to change, and every rule parameter to change.

Supported patterns are exactly `GENERIC` (Generic pattern), `II` (Illness or Injury), and `MAP` (Maternity or Adoption). `MAP` uses `PartialDayCode: "N"`; do not apply MAP-only rows or rules to `GENERIC` or `II`.

## Hierarchy, personas, and defaulting

Display configuration is nested and effective dated:

```text
Absence Type
└── absenceTypeRegions[]
    └── absenceTypeRegionUsages[]
        └── absenceUsageRules[]
```

Preserve `AbsenceTypeRegionId`, `AbsenceTypeRegionUsageId`, `AbsenceUsageRuleId`, `EffectiveStartDate`, and `EffectiveEndDate` for existing records. Never replace a full hierarchy with a manually constructed partial hierarchy.

The UI models three stored personas: **Employee**, **Manager**, and **Administrator**. Each region and usage carries its own `*UsageCode`, `*LookupType`, and `*DisplayUsageCode` for those personas.

For create, retain each region's three `*LookupType` values from the fresh
pattern template alongside its usage and display codes. These are region
fields, independent of the child usage lookups. Omitting them while sending
region usage codes can fail Fusion's region LOV binding (for example,
`LOV_MgrUsageCd`). The source helper rejects that incomplete region input;
resolve it from the template rather than inventing a lookup type.

Do not map the pattern's `EnableFlagCode` to loader `EnableFlag`. The pattern
value `E` is internal template metadata, not a valid create value for that
loader field. Omit optional `EnableFlag` from every usage create row, including
the DAT header; do not substitute `ENABLE`, a Boolean, or a blank. Requested
enable/disable behavior belongs in the three persona `*UsageCode` fields.
The source helper rejects this field at preparation and exact-source verification.
If it leaked into locally generated intent, remove that template-only mapping
and regenerate before preview; do not ask the requester to repair the DAT.
Keep `EnableRuleEdit` separate: it is supported rule metadata, not this flag.

1. Treat the returned pattern template as authoritative for both rows and persona exposure. Render and persist only returned regions/usages; never manufacture a row from another pattern.
2. A normal row supports the persona values returned by its template. Apply an explicit persona edit only to that requested persona and only at the requested region or usage. Preserve every other persona value exactly as returned (create template) or read (update/correct); do not set a non-exposed persona to `null`, `ENABLE`, or `DO_NOT_DISPLAY` by inference.
3. A row returned by the authoritative standard `singlePersonnaUsages` action is a **single shared, exposed UI control**. The UI displays one `Value` column, takes the selected shared value from its employee-bound field, and overlays its `EmployeeDefaultCode` and `EmployeeLookupType` onto **all three stored personas**: Employee, Manager, and Administrator. Exclude `SUPPL_SPC_MAT_CONDITIONS` from this overlay list. The guarded US fallback below supplies the action-equivalent fields only when that action is unavailable under its documented conditions.
4. For a single-persona row, accept one requested shared value (for example, `Display only` for Block leave status). Do not ask for or accept distinct Employee, Manager, and Administrator values. Persist the selected value and lookup type identically for all three personas; the setting is editable through the one exposed UI-equivalent control, not independently per persona.
5. Apply user edits after the master defaults and the single-persona overlay. Region edits never cascade to usages; `ENTITLEMENTS` and `REMAIN_BALANCE` never cascade to child usages.
6. On create only, set the returned `SUPPLEMENTAL_DETAILS` region to `ENABLE` for all three personas. Do not invent that region if it is not in the template.

## Human-language lookup resolution

Resolve the requested field and its value separately. First match the field only
against the UI labels and codes returned for the selected pattern and section.
An exact case-insensitive label/code wins. A minor spelling error may be accepted
only when one returned label is the uniquely defensible match and no material
word changes the intent. If the field has no unique close match, stop and ask
which returned UI label the user means.

For every lookup-backed Display Feature or Rule value:

1. Obtain the exact lookup type for that field. For a normal Display Feature,
   use the requested persona's returned `*LookupType`; resolve each requested
   persona independently. For a single-persona row, use the action-returned
   `EmployeeLookupType`, or the eligible fallback catalog's exact validated
   `EmployeeLookupType`, once and mirror the resolved code to all three stored
   personas. For a Rule field, use the UI field-to-lookup map below and the
   owning usage's returned `RuleReferenceDateLookupType` where applicable.
2. Read every page of that lookup from `commonLookupsLOV`. The returned
   `LookupCode` is the stored value and `Meaning` is the user-facing value.
3. Match in this order: exact case-insensitive `LookupCode` or `Meaning`;
   normalized exact match after trimming, collapsing whitespace, treating
   underscores and hyphens as spaces, and ignoring punctuation; then one unique
   semantic match among the returned Meanings. A semantic match must preserve
   every material qualifier such as *display*, *edit*, *required*, *only*, or
   *not*; never select a merely related value.
4. Apply these UI-intent aliases only when the destination Meaning exists in
   that exact lookup: `read only` or `view only` means **Display only**;
   `editable` or `allow edit` means **Display and edit**; and `hide` means
   **Do not display**. `enable`, `enabled`, `on`, or `turn on` means **Enabled**
   when that Meaning exists; otherwise it means **Display and edit** only when
   that is the unique full-enablement Meaning returned by the lookup. Likewise,
   `disable`, `disabled`, `off`, or `turn off` means **Not enabled** when that
   Meaning exists; otherwise it means **Do not display** only when that is the
   unique disabled/hidden Meaning returned by the lookup.
5. If zero values match, more than one value remains plausible, or the prompt
   omits a material distinction (for example, `display` when both **Display
   only** and **Display and edit** exist), do not generate a code. Ask one
   concise question naming the field and persona when applicable and list only
   the valid returned Meanings. Keep lookup codes internal unless the user asks
   for technical details.

Never apply a global English-to-code substitution. In particular:

- `SCHED_OPEN_ENDED` with `ANC_DISP_DND_DO_DE`: **Enabled** resolves to the
  returned **Display and edit** row and stores `DISPLAY_AND_EDIT`, never
  `ENABLE`.
- `SUPPL_PRIMARY_CERT_DATE` with `ANC_DISP_DND_DO`: **Display only** stores
  `DISPLAY_ONLY`; plain **Enabled** has no unique valid destination and requires
  an ask-back.
- `ADDTN_DOC_UPLOAD` or `ORA_ANC_OVERRIDEDUR` with `ANC_DISP_E_NE`:
  **Enabled** stores the code returned for the **Enabled** row, commonly
  `ENABLE`.

Before preview, validate every final code against the exact lookup type used
for its field and persona. Do not reuse a code merely because another Display
Feature or Rule lookup accepts it.

## Data Loader create behavior

After legislation and pattern are known, retrieve the master template through
the core read-only REST client. Use the standard resource route:

```text
GET /hcmRestApi/resources/11.13.18.05/absencePatterns
finder=findByLegislationAndPatternCode;LegislationCode=<LEGISLATION>,PatternCode=<PATTERN>
expand=all
```

The UI endpoint aliases below are provenance for the lookup contract; they do
not authorize a REST mutation:

```text
GET oracle_hcm_absencesUI:absencePatterns/getall_absencePatterns
finder=findByLegislationAndPatternCode;LegislationCode=<LEGISLATION>,PatternCode=<PATTERN>
expand=all
```

Retrieve the single-persona overlay through the authoritative standard
resource action:

```text
POST /hcmRestApi/resources/11.13.18.05/absencePatterns/action/singlePersonnaUsages
{ "pattern": "<PATTERN>" }
```

The corresponding UI alias is provenance only:

```text
POST oracle_hcm_absencesUI:absencePatterns/doall_singlePersonnaUsages_absencePatterns
{ "pattern": "<PATTERN>" }
```

Do not construct or use a runtime-version `rv:` route for either resolver.

### Guarded US fallback when the action is unavailable

The live single-persona action remains the primary resolver. If it is still
unavailable after the one permitted cached-token refresh because of HTTP 401,
403, 404, or 405, a timeout, or a transport/environment failure, automatically
use the US catalog in `ora-resource/ora_reference_lookups.md` only when all of
these guards pass:

1. `LegislationCode` is exactly `US` and the resolved pattern is exactly
   `GENERIC`, `II`, or `MAP`.
2. The same run retrieved exactly one fresh live master template through the
   standard resource route for that exact legislation and pattern. A stored
   template or a template for another legislation or pattern is not eligible.
3. Use the locked 3/5/4 catalog to identify the action-equivalent shared usage,
   documented UI region, `EmployeeDefaultCode=DO_NOT_DISPLAY`, and exact
   `EmployeeLookupType`. Each catalog usage must occur exactly once in that
   documented region of the fresh live master template. Continue to exclude
   `SUPPL_SPC_MAT_CONDITIONS`.
4. Retrieve every page of each distinct catalog-named lookup type from the
   fresh live `commonLookupsLOV` and require exactly one current row whose
   `LookupCode` is `DO_NOT_DISPLAY`. The pattern template must not supply or
   override a fallback shared default or lookup type; its values can differ
   from the authoritative action.
5. Overlay the catalog's validated `DO_NOT_DISPLAY` default and exact lookup
   type identically on Employee, Manager, and Administrator before applying an
   explicit user edit. Validate that edit against the same fresh lookup.
6. Record `singlePersonaSource: us-catalog-fallback`, the failed resolver and
   failure class, legislation, pattern, and every resolved region/usage in the
   immutable preview evidence, including the catalog default/lookup type and
   matching live lookup row.

When all six guards pass, the fallback is the required normal resolver path;
do not ask for a separate readiness waiver in production or non-production.
The exact immutable Data Loader archive must still be previewed and explicitly
approved immediately before upload. Fail closed instead of using the fallback
for another legislation or pattern, an HTTP 200 response that is malformed or
ambiguous, a missing or duplicated catalog row, a wrong-region match, a
catalog/lookup mismatch, or an unavailable `DO_NOT_DISPLAY` lookup code.

On primary action success, use `response.body.result`, excluding
`SUPPL_SPC_MAT_CONDITIONS`. On an eligible fallback, use only the locked
catalog rows that passed both the guarded join to the fresh live template and
the fresh lookup validation; there is no action response to consume. For those
shared rows, use the catalog's `EmployeeDefaultCode` and `EmployeeLookupType`,
never the template's, and mirror them to all three personas. Use the fresh
template for placement, display codes, field type, enable-rule flag, and rule
reference metadata. Build each returned or guarded-resolved usage retaining
`AbsenceUsageCode`, `AbsenceFieldType`, `EnableRuleEdit: "Y"` only when
`EnableRuleEditFlag` is true, and `RuleReferenceDateLookupType`.

The resulting usage rows can have mixed field sets. Keep absent rule metadata
omitted in the resolved input; the portable source helper explicitly resolves
only the two inapplicable optional rule cells for a new US type, as documented
in `../../references/portable-source-preparation.md`. Do not remove supplied
rule metadata, pad other missing fields, or split the new hierarchy to make
rows uniform. Review the helper's `fieldResolutions` in the immutable preview.

Apply the master template, then the single-persona overlay, then explicit edits, then the create-only supplemental-region override. On create, omit standard rule rows and let Fusion generate the pattern defaults. Live Generic validation generated `SCHED_ABS_OCCURRENCE_LIMIT`, `SCHED_ABS_START_RULE`, and `SUPPL_TIMELY_NOTE_RULE` with server IDs when no rule rows were supplied. Emit an `absenceUsageRules` row only for an explicit non-default rule customization supported by the refreshed contract; set `ReferenceDateCodeLookupType` from the owning usage's `RuleReferenceDateLookupType`. If a required owning usage is absent, stop; do not add it. Read back every expected generated and explicit rule after creation.

Prepare the result only through `core.data-loader` as `absenceTypes` DAT/XLSX sections: `absenceTypes`, `absenceTypeRegions`, `absenceTypeRegionUsages`, and `absenceUsageRules` only when an explicit non-default rule customization applies. The refreshed Data Loader template is the starting column contract, but its presence alone does not prove a physical date field controls creation. For create, map the requested date to the validated parent `effectiveOf=RangeStartDate=<YYYY-MM-DD>` control and omit physical parent and Display Features child `EffectiveStartDate` columns. Do not send the UI's nested REST payload.

For an existing Display Features usage update, keep the hierarchy in one DAT
member but use the proven parent-user-key carrier shape. Emit
`METADATA|absenceTypes|RestAction` as a root metadata-only marker and do not
emit an `absenceTypes` MERGE row. For every target region, emit one
identity-only `absenceTypeRegions` PATCH carrier with the exact existing
`AbsenceTypeRegionId`, parent user keys `LegislationCode` and `Name`, and
`effectiveOf=RangeMode=CORRECTION;RangeStartDate=<returned region EffectiveStartDate>`.
Omit `AbsenceTypeId` from the carrier: `LegislationCode` plus `Name` resolve
the date-effective parent. Then emit the target `absenceTypeRegionUsages`
PATCH row with the exact existing `AbsenceTypeRegionUsageId` and
`AbsenceTypeRegionId`, the complete Administrator, Manager, and Employee
`UsageCode` tuple from current readback after applying the requested edit, and
the requested operation-derived `effectiveOf` value, such as
`RangeMode=UPDATE;RangeStartDate=<requested date>` for an update.

The canonical section shape is:

```text
METADATA|absenceTypes|RestAction
METADATA|absenceTypeRegions|AbsenceTypeRegionId|LegislationCode|Name|effectiveOf|RestAction
MERGE|absenceTypeRegions|<region id>|<legislation>|<type name>|RangeMode=CORRECTION;RangeStartDate=<returned region EffectiveStartDate>|PATCH
METADATA|absenceTypeRegionUsages|AbsenceTypeRegionUsageId|AbsenceTypeRegionId|AdministratorUsageCode|ManagerUsageCode|EmployeeUsageCode|effectiveOf|RestAction
MERGE|absenceTypeRegionUsages|<usage id>|<region id>|<administrator value>|<manager value>|<employee value>|RangeMode=UPDATE;RangeStartDate=<requested date>|PATCH
```

Do not use an `id,date` composite in any surrogate-key field, `SourceRef*` as
hierarchy linkage, a parent MERGE, or physical `EffectiveStartDate`, lookup,
display, meaning, or other unchanged business-value columns in these rows.
Emit only changed usage rows, but always carry all three stored persona
`UsageCode` values on each emitted usage row so an unchanged persona is
preserved rather than nulled or defaulted. The
region carrier establishes context only; it is not a region business change.
**Resolve that carrier from the UI section and pattern, not from
`AbsenceUsageCode` alone.** Before preparing an update, confirm that the
target UI-rendered region exists and owns the target usage. A same-named usage
in another region is not an equivalent target. If the expected region is
absent, classify the work as a missing-hierarchy repair: retrieve the exact
pattern region and its children, prepare the supported child-create shape,
and require a new immutable preview and approval. Do not update a duplicate
usage in `ADDITIONAL_DETAILS` to satisfy an Additional fields request. After
any terminal result, perform UI-section-level readback of the correct region,
usage, effective slice, and all stored personas; a raw usage readback in the
wrong region is not success.

For a new type, set resolved-intent `hierarchyKeyStrategy` to `native-user-keys`. Omit root and child surrogate IDs. Bind direct children with `LegislationCode` plus `Name`; use unique `AbsenceRegionCode` for regions and unique `AbsenceUsageCode` for usages, with each usage carrying its owning `AbsenceRegionCode`. Verify these LOCAL/PARENT user-key alternatives against fresh registered metadata. Fusion allocates the IDs, so no client-generated-ID collision check or global collision endpoint is required. Include exactly one new type per archive. Retain all region and usage persona lookup/display/default fields from the fresh pattern. Omit standard rule rows and verify Fusion-generated rules after load; explicit rule creation is not supported by this key strategy. Existing-record operations continue to use exact returned IDs. Never automatically replay a create.

Keep the hierarchy in one flattened archive. Never copy `AbsencePatternRegionId` or `AbsencePatternUsageId` into create IDs. Preserve current field lengths and business-key uniqueness. Exact post-create readback must independently page all regions, usages, and generated rules, verify every requested value and date, and confirm every returned ID is a positive decimal no greater than `9007199254740991` with an exact numeric round trip. Default standard rules may be omitted only where Fusion generates them. Missing/extra rows or partial state block completion and replay.

### Post-create reconciliation and collection-index lag

When a Data Loader result Message serializes an absence type, do not accept the
Message body itself as readback. Validate its root ID as an exact positive
decimal, then use `effectiveDate=<intended effective date>` with
`q=AbsenceTypeId=<exact returned ID>` to retrieve the type. The returned type
must have the immutable archive's exact Name and LegislationCode, safe
exact-number IDs, complete expected pattern hierarchy, expected generated or
explicit rules, and all requested persona values. An `onlyData=true` expanded
response is only a convenience value snapshot: it strips the links needed for
collection discovery, and its outer `hasMore=false` does not prove any nested
array complete. Issue the same exact parent read without `onlyData=true` and
without a fields projection, then follow the exact returned `rel=child` links
from parent to regions, region to usages, and usage to rules. Never synthesize
a child URL. Page each linked collection through its returned next link or its
own `limit`/`offset` until its own `hasMore=false`, retaining link hrefs, page
counts, row counts, IDs, and response hashes. If a required child link or
nested completeness receipt is absent, stop without classifying the create as
complete.

Independently check collection discovery with the canonical compound predicate
`q=Name='<exact Name>';LegislationCode='<resolved LegislationCode>'` using the
same `effectiveDate=<intended effective date>`. Treat each substituted value as
data: double every embedded single quote (`'` becomes `''`), form the complete
logical predicate, and URL-encode the complete `q` parameter value exactly
once. Never concatenate a raw Name or LegislationCode into the request path or
double-encode a pre-encoded separator. In a CLI or shell, pass the complete
URL/path as one quoted argument. The encoded semicolon is `%3B`, but the
complete argument must still be protected from shell metacharacters; never
send the predicate with `and` or let an unquoted semicolon split the command. A
name-only query with local legislation and effective-date filtering is allowed
only when the correctly escaped, encoded, and quoted compound request errors,
not when it successfully returns zero rows.

An immediate zero-row exact-name result after creation can be collection-index
lag when the exact-ID query already returns the complete matching hierarchy.
Repeat only that read-only name request at elapsed 5, 15, 30, 45, and 60
seconds. If it converges to the same root ID, continue with the normal
operation-specific classification. If it remains zero while the exact-ID
readback stays complete, report `committed by exact ID; name-index
reconciliation pending`; preserve the official loader result, do not claim
full searchable success, and do not begin the next lifecycle mutation. A real
failed create requires both no exact-ID object and no exact-name object after
the bounded reads. No zero-result name read, pending-index result, timeout,
serialized-object `Failed` signature, or other uncertain outcome authorizes an
automatic replay. Any new create attempt requires proof that no committed or
partial target exists, a new immutable archive, revalidated native business-key
bindings, and the normal approval gate.

### Post-non-create reconciliation

After every terminal update, correction, end-date, Delete Changes, ZAP, or
child mutation, run `reconcile_absence_type_non_create_result`. Its inputs are
the exact immutable archive and SHA-256, exact operation and date, pre-submit
baseline for every target, request ID, official status/counts, all intended DAT
rows, and every available object diagnostic. Require the complete detailed
object error log when the result reports an error, diagnostic, or generic
`{MESSAGE}`; for a clean success with no diagnostics, retain an explicit
zero-diagnostic receipt and counts instead. Read the target by exact ID and by
the canonical semicolon-delimited business key, both with
`effectiveDate=<operation date>`, and independently page the complete region,
usage, and rule hierarchy.

Map every intended mutation row and identity-only carrier to an exact readback
outcome, and map every returned diagnostic to an intended row or owning
top-level object; do not require one diagnostic per DAT row. Then classify each
row and the batch. An UPDATE at date D must create a slice beginning D and use
a post-submit exact-ID read at `effectiveDate=<D-1>` (plus the canonical
business-key read when supported), or a documented history route returning
both slices, to prove its predecessor ends on D-1. It must persist every
requested value and leave every unrequested root value and the complete child
hierarchy semantically unchanged except for documented effective-date and
audit fields. Apply the corresponding expected slice/presence rules to
correction, end date, Delete Changes, ZAP, and child operations. Preserve
exact-ID and business-key evidence, semantic deltas, pagination receipts,
response hashes, and `noRetry=true`. Any missing, extra, partial, conflicting,
incompletely paged, or uncorrelated state blocks the next archive and never
authorizes replay.

## UI section-to-region mapping (authoritative)

The UI does not render the **Additional fields** table from
`ADDITIONAL_DETAILS`. It merges only the `SCHEDULING` and
`SUPPLEMENTAL_DETAILS` region usage arrays. Therefore the region is part of
the identity of every Display Features update.

| Pattern | UI section | Required region | Usage codes rendered from that region |
|---|---|---|---|
| `GENERIC` | Additional fields | `SUPPLEMENTAL_DETAILS` | `SUPPL_PRIMARY_CERT_AUTH`, `SUPPL_PRIMARY_CERT_DATE`, `SUPPL_BLOCKED_LEAVE_CANDIDATE` |
| `II` | Additional fields | `SCHEDULING` | `SCHED_II_START_DATE` |
| `II` | Additional fields | `SUPPLEMENTAL_DETAILS` | `SUPPL_PRIMARY_CERT_AUTH`, `SUPPL_PRIMARY_CERT_DATE`, `SUPPL_BLOCKED_LEAVE_CANDIDATE`, `SUPPL_NOTIF_DATE` |
| `MAP` | Additional fields | `SUPPLEMENTAL_DETAILS` | `SUPPL_PRIMARY_CERT_AUTH`, `SUPPL_PRIMARY_CERT_DATE`, `SUPPL_BLOCKED_LEAVE_CANDIDATE`, `SUPPL_NOTIF_DATE` |

`ADDITIONAL_DETAILS` is used by other UI sections and must never be used as a
substitute for either row in this table. For example, **Block leave status**
is a single-persona control, but for all three patterns its UI-visible source
is `SUPPLEMENTAL_DETAILS`, not `ADDITIONAL_DETAILS`.

## Display row catalog

The order below is a UI ordering aid, not permission to add absent template rows.

| Section | `GENERIC` | `II` additions | `MAP` differences/additions |
|---|---|---|---|
| Display sections | `ENTITLEMENTS`, `REMAIN_BALANCE` | same | same |
| Primary fields | `ADDTN_REASON`, `ADDTN_COMMENT`, `SCHED_ABS_END_DATE` | `SUPPL_SPC_MAT_CONDITIONS` | also `SCHED_ABS_START_DATE`, `SUPPL_SPC_MAT_CONDITIONS` |
| Additional fields | `SUPPL_PRIMARY_CERT_AUTH`, `SUPPL_PRIMARY_CERT_DATE`, `SUPPL_BLOCKED_LEAVE_CANDIDATE` | `SCHED_II_START_DATE`, `SUPPL_NOTIF_DATE` | `SUPPL_NOTIF_DATE` |
| Approval and processing | `ORA_ANC_PAYLOAD`, `PROC_APPROVALS`, `PROCE_APPROVAL_RESTART`, `PROC_DEFER_PROCESSING`, `ORA_ANC_DEFER_SUBSEQ` | same | plus `ORA_ANC_TERM` |
| Absence validation | `REMAIN_BALANCE_VALID_RULE`, `SCHED_ADV_SCHED_RULE`, `ORA_ANC_CONCURRENCY`, `SCHED_ABS_OCCURRENCE_LIMIT` | same | exclude `SCHED_ADV_SCHED_RULE` |
| Dates and duration | `SCHED_ABS_START_RULE`, `ORA_ANC_SCH_NONWORKDAYS`, `ORA_ANC_OVERRIDEDUR` | same | `SCHED_PLAN_ABS_START_RULE`, `SCHED_ABS_START_RULE` |
| Open ended / attachments | `SCHED_OPEN_ENDED`, `ADDTN_DOC_UPLOAD` | same | same |

`ORA_ANC_OVERRIDEDUR` is the UI's **Override daily duration** usage. It is available only when the selected template returns it; therefore a requested Administrator or Manager update must retain the template's existing Employee value and all lookup/display fields unless specifically changed.

### Single-persona Additional fields

The UI calls `singlePersonnaUsages` for every selected pattern, renders its
returned rows as one-value controls, then persists the selected value to all
three persona columns. The exposed sets are:

| Pattern | Exposed single-persona rows |
|---|---|
| `GENERIC` | `SUPPL_PRIMARY_CERT_AUTH` (Authorized absence), `SUPPL_PRIMARY_CERT_DATE` (Authorization status updated), `SUPPL_BLOCKED_LEAVE_CANDIDATE` (Block leave status) |
| `II` | the Generic rows, plus `SCHED_II_START_DATE` and `SUPPL_NOTIF_DATE` |
| `MAP` | the Generic rows, plus `SUPPL_NOTIF_DATE` |

The standard action's actual returned overlay remains authoritative when it
succeeds. When and only when the guarded US fallback is eligible, the locked
3/5/4 catalog in `ora-resource/ora_reference_lookups.md` is authoritative for
these shared rows after every required template-placement and live-lookup
check passes.

## Dependencies and rules

Do not choose visibility, requiredness, approval, validation, attachment, or open-ended behavior without user direction or an explicitly authorized type to copy. If `ADDTN_REASON` is not `DO_NOT_DISPLAY` for any persona and no reason association exists, warn; never create a reason implicitly.

Apply the approval dependency separately per persona:

```text
PROC_APPROVALS = Not Enabled  => PROCE_APPROVAL_RESTART = Not Enabled
PROCE_APPROVAL_RESTART = Enabled => PROC_APPROVALS = Enabled
```

`PROC_APPROVALS` and `PROCE_APPROVAL_RESTART` are separate Data Loader usage
rows, and their row order is not an atomicity guarantee. Never put a dependent
two-row transition into one archive merely because the rows are ordered. To
move from Enabled/Enabled to Not Enabled/Not Enabled, disable restart, reconcile
the exact hierarchy, then disable approvals in a new archive built from that
readback. To move from Not Enabled/Not Enabled to Enabled/Enabled, enable
approvals, reconcile, then enable restart. Change at most one dependency field
per persona in one archive and require every intermediate state to satisfy the
two implications above.

Rules are children of `absenceTypeRegionUsages`, never sibling records. Only these attachment points may receive a newly created system-default rule:

| Usage | Patterns | Default fields |
|---|---|---|
| `SCHED_ABS_OCCURRENCE_LIMIT` | all | `ActionCode: "E"`, `ReferenceDateCodeThird: "ABSSTRTDT"`, `EvaluationCode: "CURRCALYEAR"` |
| `SCHED_ABS_START_RULE` | all | `ActionCode: "E"`, `ConditionCodeFirst: "N"`, `ConditionCodeSecond: "N"` |
| `SCHED_PLAN_ABS_START_RULE` | MAP only | `ActionCode: "E"`, `ConditionCodeFirst: "N"`, `ConditionCodeSecond: "N"` |

Every other rule property—other than the listed UI-create defaults—including formula, calculations, additional date references, units/UOM, update code, and update-field type requires a user-supplied or explicitly approved value.

Resolve lookup-backed Rule inputs through the same human-language contract
above. The UI uses these lookup types:

| Rule field | Exact lookup type source |
|---|---|
| `ActionCode` | `ANC_TYPE_RULE_ACTION` |
| `ConditionCodeFirst`, `ConditionCodeSecond` | `ORA_ANC_DATE_VALID` |
| `CalculationCodeFirst`, `CalculationCodeSecond` | `ANC_TYPE_RULE_CALCULATION` |
| `ReferenceDateCodeFirst`, `ReferenceDateCodeSecond`, `ReferenceDateCodeThird` | owning usage's returned `RuleReferenceDateLookupType`; the UI currently returns `ANC_ABS_START_DATE_TYPE`, `ANC_ABS_PLAN_START_DATE_TYPE`, or `ANC_ABS_OCCURRENCE_REF` for the supported attachment point |
| `EvaluationCode` | `ANC_ABS_OCCURRENCE_EVAL` |
| `RuleUOMFirst`, `RuleUOMSecond` | `ANC_TYPE_RULE_UOM` |
| `RuleUOMThird` | `ANC_OCCURRENCE_UOM` |

If another Rule property is described in human language but its exact UI
lookup type is not returned or documented, stop and ask for a supported UI
value or classify the missing mapping as an authoring gap. Do not borrow a
lookup from a similarly named Rule field.

## Data Loader update, correction, and verification

Before changing an existing type, read its complete hierarchy through the core
read-only REST client using its ID, target effective date, and expansions for
regions, usages, and rules. The service can wrap any hierarchy level as
`{items: []}`; flatten only for comparison and keep all original identifiers
and dates. Use the `onlyData=true` expansion only as a value snapshot. Repeat
the exact parent read without `onlyData=true` to discover links, then follow
the returned `rel=child` links through every region, usage, and rule collection
to its own `hasMore=false`; the outer parent pagination state never proves
nested completeness, and a child path must never be invented.

For update or correction, create an immutable Data Loader source containing only changed sections and the required identity-only carriers described above. Retain the Fusion-issued region, usage, and rule IDs required by the refreshed headers; use the header-specific date-effective mapping and only template-supported columns. Never send untouched values as null/default substitutes, synthetic IDs, or `*Meaning` fields that the Data Loader template does not support.

The current registered loader contract supports a parent-only mutation ZIP and
a Display-Features-only mutation ZIP, but live one-ZIP probes that combined an
`absenceTypes` parent MERGE with region/usage update rows consistently returned
`Not Found` for every child and committed no state. Therefore, when parent
business attributes and Display Features must both change, prepare two
independently validated immutable ZIPs: apply and reconcile the parent archive
first, then refresh the expanded hierarchy and apply the metadata-root child
archive. Do not claim UI-style nested REST parity by placing both graphs in one
DAT member.

`DELETE_CHANGES` is section-specific. A parent-only Delete Changes operation
removes the parent slice but does not cascade to independently dated usage
slices. If the approved intent also reverts Display Features at that date,
first reconcile the parent operation, then use a separate metadata-root child
archive with the same identity-only region carriers and usage `DELETE` rows
using `RangeMode=DELETE_CHANGES;RangeStartDate=<child slice start>`. Verify
both the parent history and every affected usage slice.

Post-save, read the expanded hierarchy again through independently paged child
collections, run the operation-aware reconciliation above, and confirm the
effective date/mode, exact slice boundaries, only requested changes, all three
persisted persona codes, MAP-only placement, each rule's parent usage, and
absence of unrelated overwrites across the complete hierarchy.

## Reverse-engineering evidence

Behavior above was verified from:

```text
extension1/sources/ui/self/applications/absences/flows/absence-types/pages/manage-absence-type-page.js
extension1/sources/ui/self/applications/absences/flows/absence-types/pages/manage-absence-type-page-chains/absenceTypeDisplayFeaturesChain.js
extension1/sources/ui/self/applications/absences/flows/absence-types/pages/manage-absence-type-page-chains/absenceTypeDisplayFeaturesUpdateActionChain.js
extension1/sources/ui/self/applications/absences/flows/absence-types/pages/manage-absence-type-page-chains/AdvancedCreateAndEditPageTemplateSpPrimaryActionChain.js
extension1/sources/ui/self/applications/absences/flows/absence-types/pages/manage-absence-type-page-chains/TableRowUpdateEndChain.js
```

The relevant UI flow calls the standard pattern resource and authoritative
single-persona action before create, transforms default codes to usage codes,
applies the single-persona overlay to all stored personas, applies user edits
last, and creates only the returned hierarchy. The guarded US fallback models
that action output only under the conditions above; it never treats differing
template defaults as action results. In update/correction the flow reads and
flattens the existing hierarchy, emits only modified rows/rules, and preserves
placement identities.
