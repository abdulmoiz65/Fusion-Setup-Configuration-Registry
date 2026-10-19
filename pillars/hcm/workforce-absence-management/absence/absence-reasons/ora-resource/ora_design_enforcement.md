# Absence Reasons Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate supplied values and default eligibility | Require the requested operation, the required target identity, and every applicable explicit effective date, legislation, or status value; identify omitted values eligible for documented defaults, including create EffectiveStartDate |
| 2 | Apply safe defaults | Apply US for omitted LegislationCode and Active for omitted Status, plus other documented defaults; never overwrite a supplied value |
| 3 | Resolve required values | Require resolved LegislationCode and resolved Status after supplied or defaulted values are processed |
| 4 | Enforce the write-field boundary | Exclude audit fields, read-only meaning fields, and ordinary-create server-generated fields |
| 5 | Validate effective-dated and DFF behavior | Refresh the registered Data Loader template, derive `effectiveOf` for every included section, refresh describe, and resolve the exact effective-dated flex child before selecting its action |
| 6 | Stage a new parent slice when required | If the flex target lookup returns parent_stage_required, prepare and verify a parent-only load, then re-read the child before preparing a separate flex archive |
| 7 | Hand off validated data | Stop at a validated handoff to the Absence Reasons core.data-loader workflow; do not perform a direct REST mutation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every create request | Blocker | resolve_absence_reason_status | Supplied or defaulted Status does not resolve to exactly one ACTIVE_INACTIVE value | Apply Active when Status is omitted, or supply Active, Inactive, A, or I and retain the resolved LookupCode | Yes |
| Every create request | Blocker | resolve_absence_reason_legislation | Supplied or defaulted LegislationCode does not resolve to exactly one territory | Apply US when LegislationCode is omitted, or supply a unique territory code or display name and retain TerritoryCode | Yes |
| A write-oriented source contains audit or read-only meaning fields | Blocker |  | CreationDate, CreatedBy, LastUpdatedBy, LastUpdateDate, LegislationMeaning, ManagementTypeCdMeaning, or StatusMeaning is present as a write field | Remove the non-writable field and use the documented code field where applicable | Yes |
| An ordinary create source contains AbsenceReasonId or EffectiveEndDate | Blocker |  | A server-generated field is supplied without a separately validated business scenario | Omit the field and use the documented server behavior | Yes |
| A date-effective source omits effectiveOf, contains an operation-inconsistent value, or its final immutable DAT is not inspected | Blocker | refresh_absence_reasons_dataloader_template | The parent or included flexfield row lacks the exact derived `effectiveOf` value, or the final upload archive was not checked | Derive the field from the selected operation and inspect the exact DAT member; never accept a caller-authored range-mode string | Yes |
| A final DAT contains a populated non-ISO physical effective date | Blocker |  | `EffectiveStartDate` or `EffectiveEndDate` in an `absenceReasons`, `AbsenceReasonsDDFFlex`, or `AbsenceReasonsFlex` row is not serialized as `YYYY-MM-DD` | Preserve the task-specific ISO value in the final DAT; do not convert it to `YYYY/MM/DD` | Yes |
| A flexfield `MERGE` lacks its parent logical row | Blocker |  | `AbsenceReasonsDDFFlex` or `AbsenceReasonsFlex` is populated without an `absenceReasons` parent `MERGE` using the same resolved `AbsenceReasonId` and matching `effectiveOf` | Add a parent key row; for a flex-only update or retry, use a key-only parent `PATCH` and avoid unrelated parent attributes | Yes |
| A flex child PATCH lacks one exact returned target item | Blocker | resolve_absence_reason_flex_item | PATCH is selected because the business request says update, but the exact effective-dated child was not found or its returned identity was not retained | Use PATCH only for one exact returned child item. If the child is missing under an existing parent slice, use POST; if the parent slice is missing, stage the parent first | Yes |
| A flex child POST conflicts with an existing item | Blocker | resolve_absence_reason_flex_item | POST is selected even though one exact child already exists for the returned primary-key fields | Use the returned item identity and PATCH the existing child | Yes |
| One archive attempts to create a new parent effective slice and PATCH its flex child | Blocker | resolve_absence_reason_flex_item | The target parent effective slice did not exist before preparation, so the child cannot be proven addressable during the same load | Submit and verify a parent-only archive, re-run the child lookup, then build a separately approved flex archive | Yes |
| A retry reuses a failed flex archive without reconciliation | Blocker | resolve_absence_reason_flex_item | A prior load failed or partially changed the parent, but the current parent and child identities were not re-read | Reconcile both effective-dated records and rebuild the archive and approval from the returned state | Yes |
| A Task Hook preview is built for a date-effective archive | Blocker | normalize_absence_reason_effective_of | The preview relies on caller-authored `ruleResults` without inspecting the final immutable DAT member | Derive and verify `effectiveOf` from the exact archive before preview; do not accept a declared pass as evidence | No |
| A non-create date-effective source lacks one resolved current reason | Blocker | find_absence_reason_by_exact_name | Update, correction, end-date, delete-changes, and ZAP do not identify exactly one current reason | Resolve the record and its effective context before preparing the DAT | Yes |
| A delete request does not explicitly choose DELETE_CHANGES or ZAP | Blocker |  | The requested deletion scope is ambiguous | Request one deletion mode; ZAP remains subject to destructive approval | Yes |
| An item or child record is addressed | Blocker |  | A caller constructs an opaque composite key instead of following a returned self or canonical link | Retrieve the target row and follow its returned link | Yes |
| DFF or legislative DFF data is supplied | Blocker | refresh_absence_reasons_describe | Current describe metadata is unavailable or the supplied context or segment is absent from it | Refresh describe in the target environment and use only current fields | Yes |
| Any mutation is requested | Blocker |  | The operation attempts to use a direct REST client or bypasses the task's core.data-loader route | Use the existing Absence Reasons Data Loader workflow, including its preview and approval gates. The specifically documented AC1 search POST and detail GET are reads, not mutation exceptions | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| normalize_absence_reason_effective_of | Every date-effective source and final immutable DAT preview | Derived effectiveOf, selected operation/date, and verification on each included row | ora_reference_lookups.md |
| find_absence_reason_by_exact_name | A non-create date-effective source identifies its target | One resolved current reason identity before Data Loader preparation | ora_reference_lookups.md |
| resolve_absence_reason_status | Every create request | One ACTIVE_INACTIVE LookupCode mapped from the supplied or defaulted status | ora_reference_lookups.md |
| resolve_absence_reason_legislation | Every create request | One TerritoryCode mapped from the supplied or defaulted legislation | ora_reference_lookups.md |
| refresh_absence_reasons_describe | DFF data is supplied, the environment changed, or captured metadata may be stale | Current parent attributes, children, contexts, segments, and links | ora_reference_lookups.md |
| resolve_absence_reason_flex_item | Every non-create flex write, new parent effective slice with flex data, and retry after a flex failure | Exact parent-slice state, exact child match count, returned item identity, current context, and state-derived POST or PATCH decision | ora_reference_lookups.md |
| refresh_absence_reasons_dataloader_template | Every date-effective Data Loader preparation | Current registered absenceReasons DAT sections and effectiveOf field presence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.ENFORCE_DESIGN | decision | 90 | design_enforcement | eligible->AR.READINESS_GATE;blocked->AR.HANDLE_ISSUE | AR.RESOLVE_FLEX_TARGET | stop | After validation, lookup resolution, metadata refresh, flex-target resolution, and defaulting |
