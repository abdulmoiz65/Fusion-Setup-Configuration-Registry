# Manage Channel Claim Reasons Input Validation

## Operation and Source Contract

Support explicit create (POST) and update (PATCH) intent through core.data-loader, never automatic upsert. Require every prepared row's RestAction to agree with the selected operation. A missing or conflicting action is a preparation blocker, not permission to create. Evaluate mixed-operation inputs row by row without converting failed updates to creates.

The update field contract is the request schema, not the response schema or example body, in [Oracle 26B: Update one claim reason](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-channelclaimreasons-claimreasonid-patch.html), checked 2026-09-23. Newer 26C/26D pages could not be retrieved at authoring time. The documented item operation is PATCH /fscmRestApi/resources/11.13.18.05/channelClaimReasons/{ClaimReasonId}; this is a contract reference, not authorization for a direct REST write. The ten request properties below are the baseline. Before preparing a load, confirm the selected environment's live Data Loader schema exposes the required update keys, RestAction, and every requested field. A field's presence in GET/create metadata is not evidence that it is updateable. Any additional field requires an authoritative operation-specific update contract and its validation rules; stop for a contract review rather than guess or silently drop it.

## Update Fields

| Field | Type | Maximum Length | Nullable |
|---|---|---|---|
| ClaimReason | string | 120 | No |
| Description | string | 1000 | Yes |
| StartDate | date | ISO YYYY-MM-DD | Yes |
| EndDate | date | ISO YYYY-MM-DD | Yes |
| ChargebackReason | string | 255 | Yes |
| ChargebackReasonCode | string | 30 | Yes |
| CreditMemoReason | string | Not specified; apply live contract if stricter | Yes |
| CreditMemoReasonCode | string | 30 | Yes |
| WriteoffAdjustmentReason | string | Not specified; apply live contract if stricter | Yes |
| WriteoffAdjustmentReasonCode | string | 30 | Yes |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Claim reason identity | ClaimReason; ClaimReasonCode | Block the FSCR Run Book and Data Loader preview | Provide a non-empty claim reason name and a unique claim reason code | Every create request | |
| ERP Financials reference data set | SetId or SetCode or SetName | Block the FSCR Run Book and Data Loader preview | Provide at least one exact existing reference-data-set identifier managed through ERP Manage Reference Data Sets; cross-check all supplied identifiers | Every create request | resolve_reference_data_set |
| Existing update identity | ClaimReasonCode and at least one of SetId, SetCode or SetName; optional ClaimReasonId for cross-check | Block before preview | Resolve the set first, then supply the existing code and set, not proposed replacement identifiers; resolve the server-issued identity using find_claim_reason_by_code | Every update request | find_claim_reason_by_code |
| Update changes | At least one explicitly supplied update field or explicit nullable-field clear | Block empty update requests | Supply only intended changes; identity and RestAction are not changes | Every update request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Claim reason | Reject an empty or null ClaimReason or a value longer than 120 characters | Every create request; updates only when ClaimReason is supplied | |
| Claim reason code | Reject an empty ClaimReasonCode or a value longer than 30 characters | Every create request | |
| Settlement reason codes | Reject a CreditMemoReasonCode, WriteoffAdjustmentReasonCode, or ChargebackReasonCode longer than 30 characters | Any settlement reason code is supplied | |
| Chargeback reason | Reject a ChargebackReason longer than 255 characters | ChargebackReason is supplied | |
| Description | Reject a Description longer than 1000 characters | Description is supplied | |
| Dates | Validate supplied non-null dates as ISO YYYY-MM-DD after safe intake normalization. On update, compare effective dates formed by overlaying only explicit changes on current Fusion values; require EndDate not earlier than StartDate when both effective dates are non-null | Either date is supplied; current values required for update comparison | |
| Side flags | Require BuySideFlag and SellSideFlag to be boolean when supplied | Create only; not PATCH request fields in the baseline contract | |
| SetId handling | Accept optional SetId as an intake-only exact nonnegative integer within int64 and 18-digit precision. Zero is supplied, not missing, and is valid for COMMON after verification. Reject negatives, fractions, booleans, scientific notation or precision loss. Require at least one nonblank SetId, SetCode or SetName; do not require ID when code/name is supplied. Resolve before normal loader validation; omit SetId from the prepared loader artifact, never from the original workbook | Every create or update identity | resolve_reference_data_set |
| Reference data set identity | Require exactly one resolved SetCode and SetName pair; reject any conflicting supplied SetId, SetCode or SetName; blank optional identifiers are absent, never a guessed default | Every create or update identity | resolve_reference_data_set |
| Read-only attributes | Reject ClaimReasonId, CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, and links from create input | A create candidate contains a response-only attribute | |
| Documented request fields | Reject fields outside the operation-specific contract, except verified loader identity/control columns. ClaimReasonCode, SetCode, SetName, SetId, BuySideFlag, and SellSideFlag are not baseline update fields; reject attempts to change them. Audit columns and links are never writable | Every create or update request | |
| Bulk row scope | Apply every required-group, dependency, uniqueness, and field check independently to each record | More than one source row is supplied | |
| Update identity and intent | At CJMCR.VALIDATE_UPDATE require explicit update intent, exactly one lookup match, and agreement of every supplied identity with that match; a create reaching this node is DUPLICATE | Existing match returned | find_claim_reason_by_code |
| Sparse updates | Preserve all omitted fields. Blank spreadsheet cells are not a request to clear. Remove unrequested writable columns before immutable preparation; if different rows need different field sets, prepare separate sources or require proven per-row omission semantics. Never fill blanks with stale existing values or silently exclude an intended change | Every update request | |
| Explicit clears | Accept a clear only for a nullable update field and only when the user explicitly requests it and the selected loader's documented null encoding is verified. Do not invent #NULL, NULL, empty-string, or blank-cell semantics; block if the loader cannot represent the requested clear | A field is to be cleared | |
| Update key and controls | Use the live key-fields contract and the resolved existing identity. ClaimReasonId can be a loader key only when metadata requires or permits it; never treat it as a writable REST attribute. Reject POST, DELETE, or an absent RestAction on an update artifact | Prepared update artifact | |
| No-op and repeated targets | Compare requested fields with current values after date/type normalization; return NO_CHANGE without upload if nothing changes. Reject repeated update rows for the same resolved record rather than apply last-row-wins | Update before preview | find_claim_reason_by_code |
| Lookup-backed comparisons | Require current values for every comparison and both effective dates; absent response fields are an incomplete lookup, not null. Fusion remains authoritative for settlement reason validity; do not invent local reason-code catalogs | Update before preview | find_claim_reason_by_code |

## Set Identity Preparation

Read set identifiers from the channelClaimReasons worksheet/section and retain row/header provenance. Resolve SetId, SetCode and SetName before normal Data Loader mapping/preflight. SetId is not an alias for SetCode: never copy numeric ID text into a code/name field or map it directly to an unsupported loader attribute. Prepare a separate loader source containing the resolved SetCode and SetName and no SetId column, preserving unrelated values. Keep the user's workbook unchanged; disclose the ID-to-code/name resolution and intake-column omission in preview. Unresolved or conflicting input blocks preparation rather than being silently excluded.

On update, use the resolved set only to find and cross-check the existing target, including agreement with the returned SetId when supplied. A baseline set change is prohibited, not permission to target another same-code record. The intake-only exception does not make set identity writable. Revalidate the final artifact through Data Loader and Task Hook; prior approval never carries across a changed artifact.

## Date Header Mapping

For CSV/XLSX intake in the `channelClaimReasons` section, recognize these task-scoped aliases before applying the unknown-field check:

| Source Header Examples | Canonical Target |
|---|---|
| FromDate; From Date; From_Date; From-Date; Start Date | StartDate |
| ToDate; To Date; To_Date; To-Date; End Date | EndDate |

For matching only, trim surrounding whitespace, ignore case, and remove whitespace, underscores, and hyphens. Match only the resulting `fromdate` or `startdate` to `StartDate`, and `todate` or `enddate` to `EndDate`. Exact canonical headers remain unchanged. Do not infer unrelated or ambiguous headers such as `Date`, `From`, or `To`, or extend these aliases to another section or business object.

Confirm each canonical target exists in the selected live Data Loader schema, then supply an existing `--mapping-edit` option using the exact original source header. For example:

```text
--mapping-edit "channelClaimReasons/From Date=StartDate"
--mapping-edit "channelClaimReasons/To Date=EndDate"
```

Use `FromDate` or `ToDate` in those options when that is the actual header. Apply only mappings present in the input and show them in the normal mapping review. These documented aliases do not require a separate user mapping decision. This is task guidance for the assisted workflow, not a global change to the standalone Data Loader alias engine.

Read values by worksheet/section, row, and header; preserve that provenance. Preserve date values and the original workbook. Normalize unambiguous `YYYY/MM/DD` intake dates to ISO `YYYY-MM-DD` for the task's date checks without changing the calendar date. Reject ambiguous or invalid dates; validate `EndDate >= StartDate` after mapping. Disclose already end-dated records without extending dates or treating them as an alias error.

If two source columns resolve to the same target (including an alias plus its canonical header), stop for duplicate-target resolution even when their values agree. If a target is absent from live metadata, report a schema mismatch rather than inventing an attribute. Other unknown or ambiguous headers remain mapping blockers. Do not drop dates, silently exclude columns, or bypass Mapping stage by manually rebuilding a DAT file to avoid unresolved mappings.

A replacement source invalidates the previous pending preview. Any source or mapping change requires fresh Data Loader preflight and Task Hook validation of the final immutable artifact before upload approval. Header aliases never authorize an upload or reuse an earlier approval.

## Test Scenarios

| Scenario | Input Condition | Expected Result |
|---|---|---|
| Valid create | ClaimReason and ClaimReasonCode are valid; one reference data set resolves; optional settlement fields, if supplied, meet their documented field-format checks; no existing code/set match exists | Build a create-only core.data-loader preview with false defaults for omitted side flags; require approval before execution |
| Missing required fields | ClaimReason, ClaimReasonCode, or all reference-data-set identifiers are absent | Return INPUT_VALIDATION and list only the missing fields; do not build a preview |
| Invalid lookup or reference data set | SetId, SetCode or SetName has zero or multiple ERP Financials reference-data-set lookup matches | Return DEPENDENCY_BLOCKER with the supplied identifier; do not invoke Data Loader |
| Set ID only | Exact existing SetId, with no code/name | Verify ID and resolve code/name, confirm the LOV tuple, then prepare supported loader fields without SetId |
| Code or name only | SetCode only, SetName only, or blank SetId with either | Resolve without requiring ID; blank optional identifiers do not block |
| Multiple set identifiers | Any pair or all three identifiers supplied | Accept only when every nonblank identifier agrees with one verified set; never silently prioritize conflicting values |
| COMMON zero ID | SetId=0 | Treat as supplied and verify COMMON; do not reject as missing or apply a different default |
| Invalid or missing set identity | All identifiers blank, or SetId negative, fractional, boolean, scientific notation or precision-damaged | Block before preview; malformed supplied ID cannot fall back to code/name |
| Incomplete ID lookup | No match, multiple matches, missing code/name, incomplete paging, unavailable endpoint or failed LOV confirmation | Block without guessing values or falling back to another identifier |
| Set identity on update | Verified ID matches current reason versus a changed baseline set | Accept unchanged identity only; reject reassignment even if another same-code reason exists |
| Final loader source | Intake SetId has been resolved | Keep original workbook unchanged, omit SetId from prepared source, preserve other values and require fresh final preflight/Task Hook validation |
| Duplicate claim-reason code on create | Create intent and exactly one record with the same ClaimReasonCode and resolved SetCode | Return DUPLICATE; never silently switch to update |
| Dependency not available | The reference data set is unavailable | Return DEPENDENCY_BLOCKER with user-facing corrective guidance; do not create the prerequisite from this task |
| Compact date aliases | FromDate and ToDate with targets available in live metadata | Map to StartDate and EndDate through core.data-loader; retain values without an extra alias-confirmation prompt |
| Spaced and case-varied headers | ` from date ` and `TO DATE` | Use the exact original headers in mapping options and resolve to StartDate and EndDate |
| Separator variants | From_Date and To-Date, or Start Date and End Date | Resolve only the documented normalized names to their canonical date targets |
| Duplicate date target | FromDate and StartDate, or To Date and EndDate, appear together | Block duplicate-target mapping even if values agree |
| Missing target or ambiguous header | Live schema lacks StartDate, or the source header is Date | Report the schema or mapping blocker; do not guess or discard the column |
| Date format and range | From Date=2026/01/01; To Date=2026/12/31 | Preserve calendar dates, validate as ISO dates, and enforce the date range after mapping |
| Invalid date range | FromDate=2026-12-31; ToDate=2026-01-01 | Block the reversed range after alias resolution |
| Replacement workbook | A new workbook renames date headers after a pending preview | Supersede the old preview and repeat preflight, Task Hook validation, and approval for the replacement |
| Description and end date update | Existing exact code/set match; Description and To Date supplied | PATCH only those two mapped changes; compare EndDate with current StartDate and preserve all other fields |
| Full update field coverage | Exercise each of the ten Update Fields individually against a matching current record | Accept every contract-valid change when exposed by live loader metadata, not only description/dates |
| Identity-only optional ID | Code/set lookup returns one record and supplied ClaimReasonId differs | Block identity mismatch; never update either record |
| Missing or ambiguous target | PATCH row has zero or multiple exact matches | Block; no create fallback or first-match selection |
| Response-only or create-only changes | User attempts to change ClaimReasonCode, reference set, side flags, or audit fields | Reject unless a separately verified update contract explicitly permits the field; unchanged required loader keys are identity only |
| Nullable clear | Explicit clear of Description versus a blank worksheet cell | Clear only with verified loader null encoding; blank alone means unchanged; never clear ClaimReason |
| Partial-date validation | Current StartDate=2026-06-01; proposed EndDate=2026-05-01 | Block even when StartDate is absent from the workbook |
| Field boundaries | ClaimReason length 121, Description length 1001, a reason code length 31, or invalid date | Block before approval; boundary values 120, 1000, and 30 pass the corresponding length check |
| Omitted flags | Existing side flags are true and update contains Description only | No false defaults and no side-flag write |
| No-op or duplicate row | Requested values already match, or two rows target the same record | NO_CHANGE without submission for a no-op; block duplicate targets |
| Loader/API mismatch | PATCH request allows a field but selected loader lacks it | Report unsupported field for this route; do not discard it or issue direct PATCH |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCR.VALIDATE_INPUT | step | 1 | validate_input | valid->CJMCR.RESOLVE_REFERENCE_DATA_SET;invalid->RETURN_ISSUES | none | stop | Validate operation-specific supplied input and mapping before lookup; defer checks requiring current Fusion values to CJMCR.VALIDATE_UPDATE |
| CJMCR.VALIDATE_UPDATE | decision | 6 | validate_input | valid->CJMCR.CONFIRM_UPDATE_GATE;unchanged->CJMCR.RETURN_NO_CHANGE;invalid->RETURN_ISSUES | CJMCR.FIND_BY_CODE | stop | Require update intent and evaluate current-value, immutable-field, sparse-update, null, effective-date, and repeated-target checks after an exact match; create intent returns DUPLICATE via invalid |
