# Manage Channel Claim Sources Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | Explicit create, create_child, or update intent; matching RestAction | Block | Split mixed operations; never infer upsert. Explicit classify/skip intent permits preparation-time classification, not server upsert | Every request | |
| Create mapping | ClaimClassCode; ClaimSourceCode; ClaimPrefix; SetId or resolvable SetCode/SetName | Block | Resolve exact set before preparation | Create only | resolve_reference_data_set |
| Update parent identity | ClaimSourceMapId or exact existing ClaimClassCode + ClaimSourceCode + set | Block | Resolve and cross-check every supplied identity | Update only | resolve_existing_claim_source |
| Update child identity | Verified parent plus SourceSettlementMethodId | Block | Resolve existing child within parent; proposed SettlementMethod is not an identity | Existing child update | resolve_existing_settlement_method |
| Optional defaults | DefaultClaimType or DefaultClaimTypeId; DefaultClaimReason or DefaultClaimReasonId | Preserve if omitted on update | Resolve non-null proposed reference through resolve_default_claim_type or resolve_default_claim_reason and its reference-set eligibility rule | When supplied/changed | |
| Create settlement method | SettlementMethod; SettlementMethodCode; AccountingFor or AccountingForCode | Block | Resolve method and accounting lookup values | Each child create | |
| Existing parent for child creation | ClaimSourceMapId or exact class/source/set identity | Block | Resolve existing parent before child lookup; do not require a parent create body | create_child only | resolve_existing_claim_source |

## Child Create Fields

Use SettlementMethod and SettlementMethodCode (code at most 30 characters), AccountingFor and/or AccountingForCode (code at most 30 characters), and optional boolean DefaultFlag and EnabledFlag. Resolve names/codes consistently. Generated SourceSettlementMethodId is omitted; verified parent identity is loader linkage, not a generated child key. Oracle exposes SeededFlag in its POST schema, but this skill's ordinary user-created configuration workflow does not set predefined status: omit copied export flags and disclose the exclusion; an explicit request to set predefined status is outside this workflow. BuySideFlag and SellSideFlag are export context, not child create fields.

For create_child, require a live-supported child POST with exact existing-parent linkage. A header-only root worksheet may preserve XLSX structure but must produce no fabricated parent mutation. Unsupported linkage is a catalog mismatch, not permission to use direct REST. Split parent updates and child creates before preview. Duplicate parent/method create rows block.

## Parent Update Fields

Only these scalar fields occur in the parent PATCH request schema. The nested settlementMethods array is represented by separately validated existing child rows, not a replacement collection.

| Field | Type | Limit | Nullable |
|---|---|---|---|
| ClaimPrefix | string | 5 | No |
| DefaultClaimReason | string | Not specified | Yes |
| DefaultClaimReasonId | integer int64 | precision 18 | Yes |
| DefaultClaimType | string | Not specified | Yes |
| DefaultClaimTypeId | integer int64 | precision 18 | Yes |
| Description | string | 1000 | Yes |
| EnabledFlag | boolean | true or false | Yes |

## Child Update Fields

| Field | Type | Limit | Nullable |
|---|---|---|---|
| AccountingFor | string | Receivables or Payables | Yes |
| DefaultFlag | boolean | true or false | Yes |
| EnabledFlag | boolean | true or false | Yes |
| SettlementMethod | string | Exact lookup name | No |

These are request-schema fields, not every non-readOnly response field. AccountingForCode and SettlementMethodCode are absent from child PATCH. The predefined accounting restriction is owned by design enforcement. Sources and retrieval caveat are recorded in the skill's Contract Sources section.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Required create values and lengths | Nonblank class/source codes at most 30 characters, nonblank prefix at most 5, description at most 1000; set must resolve | Create | |
| Update scalar contract | Enforce the exact Parent/Child Update Fields types, lengths and nullability; positive int64 IDs without precision loss; do not require unmodified create fields | Update | |
| Boolean input | Normalize unambiguous boolean workbook values through loader mapping; reject ambiguous values; false is a supplied value, never absence | Supplied flag | |
| Worksheet/header mapping | Normalize spacing, underscores and case only for unambiguous known names; keep parent/child worksheet scope and loader identity columns; conflicting aliases block. No date fields exist here, so FromDate, ToDate, StartDate and EndDate are unsupported, not aliases | Workbook preparation | |
| Update-only excluded fields | ClaimSourceMapId and SourceSettlementMethodId are verified keys only. Parent ClaimClass, ClaimClassCode, ClaimSource, ClaimSourceCode, SetId, SetCode, SetName; child AccountingForCode and SettlementMethodCode; all audit fields, SeededFlag and links are context only. Reject proposed edits, omit them from request bodies; retain only verified keys required by loader metadata | Update | |
| Create excluded fields | Reject generated child IDs, audit fields and links in create body. SeededFlag is excluded by this workflow's predefined-status policy, not classified as API read-only; disclose copied export flags omitted from preparation | Create or create_child | |
| Sparse semantics | Omitted or blank cells preserve current values. Explicit clear must be separately requested, nullable and representable by documented loader null encoding; otherwise block. Never turn blank into false, zero, empty string or null | Update | |
| Paired reference edits | Compare name/ID pairs with trusted baseline. Resolve changed member independently; unchanged companion is context and omitted. If both are explicitly changed they must resolve to the same object. A clear must not resend a stale non-null companion; fail if loader cannot represent the clear safely | Update default type/reason | |
| Export baseline | Full-data workbooks require trusted baseline and fresh target evidence before distinguishing context from edits; missing baseline needs explicit field-level change intent. Detect identity/context edits and drift; do not silently discard requested unsupported edits | Update preparation | |
| Duplicate rows | Reject duplicate parent targets or duplicate parent/child ID pairs; never let row order decide last-wins behavior | Any batch | |
| RestAction and metadata | Every update row must be PATCH; every create row must be POST. Verify exact writable field, key, control and child-linkage support against live loader metadata; unsupported scope blocks without silently dropping columns | Final artifact | |
| Sparse row shapes | Separate artifacts by changed-field set unless per-row omission is documented. No JSON child cells or fabricated parent updates for child-only changes | Update preparation | |
| Final changes | Recompare normalized proposed values against current evidence. Create returns create; nonempty parent or child diff returns changed; complete no-op returns unchanged. Remove partial no-op rows only during preparation and rerun preflight | Final update validation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCS.VALIDATE_INPUT | step | 1 | validate_input | valid->CJMCS.RESOLVE_EXISTING;invalid->RETURN_ISSUES | none | stop | Validate normalized operation and supplied input shape before lookup |
| CJMCS.VALIDATE_CHANGES | decision | 7 | validate_input | create->CJMCS.CONFIRM_CREATE;create_child->CJMCS.CONFIRM_CHILD_CREATE;changed->CJMCS.CONFIRM_UPDATE;unchanged->CJMCS.RETURN_NO_CHANGE;invalid->RETURN_ISSUES | CJMCS.APPLY_DEFAULTS | stop | Apply final resolved-field, sparse-diff and immutable-artifact checks; explicit create_child requires new child rows only under an existing parent; no-op performs no write |
