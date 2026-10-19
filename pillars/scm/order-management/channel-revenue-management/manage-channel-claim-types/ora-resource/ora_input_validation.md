# Manage Channel Claim Types Input Validation

## Operation Contract

Support explicit create and update intent through core.data-loader. Creation rules below apply only to create rows; update rules take precedence for PATCH rows, including child-only changes. User-supplied worksheet changes are the local source of intended changes, while Fusion lookups are authoritative for existing identity and current values. Never infer update intent from a duplicate create.

Contract checked 2026-09-23 against Oracle 26B [parent PATCH](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-channelclaimtypes-claimtypeid-patch.html) and [child PATCH](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-channelclaimtypes-claimtypeid-child-businessunitlevelmappings-businessunitlevelmappingid-patch.html). Newer 26C/26D parent PATCH pages were not retrievable. Use the request schema, not response properties or example bodies: the parent example includes identity fields absent from its PATCH schema. Reverify live loader compatibility during each preparation; additional writable fields require an authoritative operation-specific contract.

## Parent Update Fields

| Field | Type | Maximum Length | Nullable |
|---|---|---|---|
| ClaimType | string | 120 | No |
| Description | string | 1000 | Yes |
| StartDate | date | ISO YYYY-MM-DD | Yes |
| EndDate | date | ISO YYYY-MM-DD | Yes |
| ChargebackTransactionType | string | 255 | Yes |
| ChargebackTransactionTypeSequenceId | integer int64 | precision 18 | Yes |
| CreditMemoTransactionType | string | Not specified; apply live contract if stricter | Yes |
| CreditMemoTransactionTypeSequenceId | integer int64 | precision 18 | Yes |
| InvoiceTransactionType | string | 255 | Yes |
| InvoiceTransactionTypeSequenceId | integer int64 | precision 18 | Yes |

The parent PATCH schema also includes the businessUnitLevelMappings array with the child PATCH schema. This is a child-update container, not a scalar field or permission to replace/delete the collection.

## Child Update Fields

| Field | Type | Maximum Length | Nullable |
|---|---|---|---|
| BusinessUnit | string | 255 | Yes |
| ReceivablesActivityForReceiptWriteOffIdInDeduction | integer int64 | precision 18 | Yes |
| ReceivablesActivityForReceiptWriteOffInDeduction | string | 255 | Yes |
| ReceivablesActivityForWriteOffAdjustmentIdInInvDeduction | integer int64 | precision 18 | Yes |
| ReceivablesActivityForWriteOffAdjustmentInInvDeduction | string | 255 | Yes |

## Update Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Existing parent | Require ClaimTypeCode and at least one of SetId, SetCode or SetName resolved to one set, one exact match and agreement of optional ClaimTypeId; no renaming code or moving set | Every update, including child-only | find_claim_type_by_code |
| Existing child | Require parent identity plus existing BUMappingCode or BusinessUnitLevelMappingId. Resolve within that parent, cross-check every supplied child key and current BusinessUnitId, reject duplicates and mis-parentage | Child update | find_existing_bu_mapping |
| Writable fields | Accept only the two PATCH field tables plus verified identity/control columns. Reject attempts to change ClaimTypeCode, set identity, side flags, BUMappingCode, BusinessUnitId, parent/child IDs, audit fields, or links | Every update | |
| Business Unit change | BusinessUnit is a writable name on PATCH, not the create-only helper. Normalize BusinessUnitName intake to BusinessUnit using explicit mapping after live-schema confirmation. Resolve a supplied non-null new name, retain BusinessUnit as the intended change, and never substitute a BusinessUnitId mutation. Existing BusinessUnitId is identity evidence, not the proposed new ID | BusinessUnit supplied on child update | resolve_business_unit_identity |
| Sparse required fields | Do not require ClaimType, a new BusinessUnit name, or AR fields when not changed. Require at least one intended change across parent/children. Child-only has no parent mutation | Every update | |
| Types and lengths | Enforce the PATCH field tables only on supplied changes. Integer IDs are exact integers within int64 and 18-digit precision, not floats or scientific notation; preserve their digits. ClaimType cannot be blank or null | Every update | |
| Effective dates | Normalize unambiguous YYYY/MM/DD to ISO, overlay requested dates on current dates and reject effective EndDate before StartDate. Missing current fields are incomplete evidence, not null | Parent date update | find_claim_type_by_code |
| Omission and clears | Omitted fields and absent children stay unchanged. Blank cells are not clears. Explicit clears require a nullable field and documented loader null encoding; do not invent a marker. Separate sources for differing change columns unless per-row omission is proven | Every update | |
| Live loader contract | Verify PATCH, each writable field, exact section, IDs/keys and parent-child linkage. Do not add SetId from a GET response to a template that lacks it. BusinessUnit absent from the child loader blocks that requested change | Final preparation | |
| No change and repeated targets | Compare intended fields against complete current values; return NO_CHANGE when all match. Reject repeated parent or child mutation targets. Multiple distinct children under one parent are valid | Every update | find_existing_bu_mapping |

When reviewing an edited export, match rows by stable parent code/set and child identity, not row position. Removed rows are exclusions, never deletions. Exclude baseline/reference sheets and notes from loader records. Derive sparse changes against the preserved original, then revalidate against live values; conflicting intervening changes require review before preview.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parent claim type identity | ClaimType; ClaimTypeCode | Block the FSCR Run Book and Data Loader preview | Provide a non-empty claim type name and a unique claim type code | Every parent create row | |
| ERP Financials reference data set | SetId or SetCode or SetName | Block the preview when the supplied reference data set cannot be resolved uniquely | Provide one exact existing ERP Financials reference-data-set identifier. The Data Loader template resolves its set identity from the matched SetCode and SetName pair | Every parent create row | resolve_reference_data_set |
| Business-unit mapping identity | BusinessUnitId or BusinessUnit or BusinessUnitName; BUMappingCode | Block only the supplied businessUnitLevelMappings child row | Provide an exact BusinessUnitId or Business Unit name, plus BUMappingCode, for every new child mapping. FSCR verifies one active BU; when both ID and name are supplied they must agree. Updates use Existing child under Update Validation instead. | Child create only | resolve_business_unit_identity |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ClaimType | Reject an empty ClaimType | Every parent create row | |
| ClaimTypeCode | Reject an empty ClaimTypeCode | Every parent create row | |
| SetId handling | Accept optional SetId as an intake-only exact nonnegative integer within int64 and 18-digit precision. Zero is supplied, not missing, and is valid for COMMON after verification. Reject negatives, fractions, booleans, scientific notation or precision loss. Require at least one nonblank SetId, SetCode or SetName; do not require ID when code/name is supplied. Resolve before normal loader validation; omit SetId from the prepared loader artifact, never from the original workbook | Every create or update identity | resolve_reference_data_set |
| Reference data set identity | Require one resolved SetCode and SetName pair; reject any conflicting supplied SetId, SetCode or SetName; blank optional identifiers are absent, never a guessed default | Every create or update identity | resolve_reference_data_set |
| Buy-side and sell-side applicability | Require BuySideFlag and SellSideFlag to be boolean when supplied; evaluate omitted flags as their documented false defaults and require at least one effective side to be true before default materialization | Every parent create row | |
| Effective dates | Require supplied StartDate and EndDate to be ISO YYYY-MM-DD dates after safe YYYY/MM/DD normalization; reject EndDate earlier than StartDate | Create dates; updates use the current-value overlay above | |
| Child mapping parentage | Require each businessUnitLevelMappings row to link to exactly one channelClaimTypes parent using verified loader linkage; do not generate a Data Loader Map worksheet | Any child mapping is supplied | |
| Business Unit identity | Require BusinessUnitId or a nonblank BusinessUnit or BusinessUnitName. Names are optional when ID is supplied; supplied name aliases must agree | Child create only | resolve_business_unit_identity |
| BusinessUnitId | Accept an exact positive integer ID without precision loss, fractions or scientific notation. Verify it against the active BU lookup; never trust it unchecked. When only a name is supplied, populate the resolved ID before final Data Loader validation. | Child create only | resolve_business_unit_identity |
| BUMappingCode | Reject an empty BUMappingCode in a supplied child mapping | Child create only; update allows existing mapping ID instead | |
| AR-related optional fields | Validate operation-specific schema, types and lengths, but do not validate dependent AR business values or look up transaction types, credit memo types, chargeback types, or receivables activities | Any AR-related field is supplied | |
| Read-only attributes | Reject response-only parent and child identifiers, audit attributes, and links from create input | A create candidate contains response-only data | |
| Documented request fields | For create only, treat BusinessUnit and BusinessUnitName as intake-only helper fields and remove them after resolving BusinessUnitId. Updates retain writable BusinessUnit subject to live loader support. Reject unknown fields rather than discard intended changes | Every request | resolve_business_unit_identity |
| Bulk row scope | Apply parent and child checks independently to each parent record and its associated child rows | More than one parent row is supplied | |

## Data Loader Mapping Guidance

### Worksheet and column identity

Read XLSX values as worksheet, row, and header pairs using a workbook reader. Shared-string indexes are storage references, not column positions; never infer field ownership from a flattened shared-string list. Preserve that source location in mapping evidence and diagnostics.

The parent channelClaimTypes sheet owns SetId, SetCode and SetName. The child businessUnitLevelMappings sheet owns BUMappingCode and its Business Unit identity. Preserve BUMappingCode literally; do not use it as SetCode, SetName, BusinessUnit, or BusinessUnitId, even when its text resembles one of those values. A child ClaimTypeCode must identify its associated parent; flag a mismatched code instead of silently reassigning the child.

### Set identity preparation

Resolve parent SetId, SetCode and SetName before normal Data Loader mapping/preflight. SetId is not an alias for SetCode: never copy numeric ID text into a code/name field or map it directly to an unsupported loader attribute. Prepare a separate loader source containing the resolved SetCode and SetName and no SetId column, preserving every unrelated value and parent-child relationship. Keep the user's workbook unchanged; disclose the ID-to-code/name resolution and intake-column omission in preview. Unresolved or conflicting input blocks preparation rather than being silently excluded. On update, use the resolved set only to find and cross-check the existing target; a baseline set change is prohibited, not permission to target another same-code record. Revalidate the final artifact through Data Loader and Task Hook; prior approval never carries across a changed artifact.

### Accepted parent date aliases

These aliases are scoped to channelClaimTypes and are authorized by this task's intake contract:

| Source Header | Target Attribute | Scope |
|---|---|---|
| FromDate | StartDate | channelClaimTypes parent only |
| ToDate | EndDate | channelClaimTypes parent only |

Verify that the exact target attributes exist in the selected live Data Loader schema. When they exist and each has one source column, apply the applicable existing core.data-loader option during mapping/preflight:

```text
--mapping-edit channelClaimTypes/FromDate=StartDate
--mapping-edit channelClaimTypes/ToDate=EndDate
```

Apply only aliases present in the source. Preserve their values, validate them using the effective-date rule above, and show the mappings in the normal loader review. Do not require another user mapping decision solely for these documented aliases. Do not add global aliases, rewrite the user's workbook, or waive other mapping failures. If an alias and its canonical header both target the same attribute, stop for duplicate-target resolution, even if the values agree. If a target attribute is absent from live metadata, report a schema mismatch instead of forcing it into the payload. An artifact changed by mapping must pass fresh Data Loader preflight and subsequent Task Hook validation before upload approval.

The following section requirements apply to create only. Updates use the sparse Update Validation contract above, retain requested writable BusinessUnit names, and require only verified target/linkage columns plus intended changes.

| Data Loader Section | Parent Relationship | Required Input | Optional Input Guidance |
|---|---|---|---|
| channelClaimTypes | Root parent | ClaimType; ClaimTypeCode | Supply SetId, SetCode or SetName as reference-data-set evidence. FSCR resolves the SetCode and SetName pair through ERP Financials. SetId is allowed in intake but omitted from the prepared loader artifact after successful resolution. Supply BuySideFlag, SellSideFlag, StartDate, and EndDate when applicable. Retain API-supported AR-related fields without FSCR validation. |
| businessUnitLevelMappings | Child of channelClaimTypes | Intake: BusinessUnitId or BusinessUnit or BusinessUnitName; BUMappingCode. Final loader source: resolved BusinessUnitId; BUMappingCode. | Resolve the submitted ID or name to exactly one active Financials Business Unit, retain or populate its verified BusinessUnitId, and remove any intake-only name field before normal Data Loader validation. Add child rows only for mappings that belong to the parent claim type. Do not include a child sheet or row when no mapping is needed. |

## Test Scenarios

| Scenario | Input Condition | Expected Result |
|---|---|---|
| Valid parent claim type creation | ClaimType, ClaimTypeCode, reference-data-set evidence, side applicability, and dates are valid; the lookup resolves one SetCode and SetName pair | Build a create-only core.data-loader preview and require approval before execution |
| Valid claim type with business-unit mappings | Valid parent plus one or more child rows with an exact active BusinessUnitId or BusinessUnit or BusinessUnitName and BUMappingCode | Verify each ID or resolve each name to one BusinessUnitId, validate parent-child discrimination, and build one Data Loader preview |
| Missing required parent fields | ClaimType or ClaimTypeCode is absent | Return INPUT_VALIDATION and do not build a preview |
| Missing or invalid business-unit mapping fields | A supplied child mapping lacks both BU ID and name, or lacks BUMappingCode, has an invalid parent discriminator, resolves to zero or multiple active Business Units, or supplies a conflicting BusinessUnitId | Return INPUT_VALIDATION or DEPENDENCY_BLOCKER for the affected child row and do not build a preview |
| Invalid reference data set | SetId, SetCode or SetName has zero or multiple matching sets, or supplied identifiers conflict | Return DEPENDENCY_BLOCKER and do not invoke Data Loader |
| Duplicate claim-type code on create | Create intent and one exact ClaimTypeCode/set match | Return DUPLICATE; do not switch to update |
| AR-related value supplied without FSCR validation | An API-supported AR-related optional field is present | Preserve the field for Data Loader and disclose that FSCR cannot validate its value |
| Parent date aliases | Parent FromDate=2026-01-01 and ToDate=2026-12-31; live schema exposes StartDate and EndDate | Apply the two scoped mapping options, preserve values, and validate the resulting date range without requesting alias confirmation |
| Duplicate date target | Parent contains both FromDate and StartDate, or both ToDate and EndDate | Block duplicate-target mapping; do not discard either column silently |
| Date target unavailable | Parent uses FromDate but live schema lacks StartDate | Report schema mismatch; do not invent an attribute |
| Distinct set and BU mapping codes | Parent SetCode=EXAMPLE_SET; child BUMappingCode=EXAMPLE_BU_MAP | Resolve only EXAMPLE_SET as the reference set and preserve EXAMPLE_BU_MAP as the child mapping code |
| Child belongs to another parent | Child ClaimTypeCode=EXAMPLE_OTHER while the only parent is EXAMPLE_CLAIM | Block the unmatched child; do not substitute the parent's code |

## Set Identity Acceptance Cases

| Scenario | Expected Result |
|---|---|
| SetId only, exact match | Resolve code/name; omit intake ID from final loader source |
| SetCode only, no ID | Preserve code lookup; resolve name without requesting ID |
| SetName only, no ID | Preserve name lookup; require a unique exact match without requesting ID |
| Any pair or all three supplied consistently | Accept only when all supplied identifiers match one set |
| SetId=0 resolves COMMON | Accept zero; do not treat it as missing or require a positive ID |
| Blank ID with valid code/name | Use supplied code/name; no ID requirement |
| All identifiers absent, malformed ID or precision loss | Block input validation before lookup |
| Supplied identifiers conflict, no match, multiple matches or incomplete evidence | Block; never prefer one value silently or fall back from failed ID |
| Update includes SetId matching the existing target | Treat as identity only; no set reassignment |
| Update attempts set reassignment or unsupported SetId in final artifact | Block before approval |
| Valid ID lookup lacks code/name or code/name cannot be confirmed in loader set LOV | Block unresolved dependency; no guessed values |

## BU Identity Acceptance Cases

| Scenario | Expected Result |
|---|---|
| Create with ID only; one active exact ID match | Accept without requesting a name; retain verified ID |
| Create with name only; one active exact name match | Populate verified ID; omit helper name from create payload |
| Create with ID and matching name | Accept the matched active BU |
| Create with ID and conflicting name or conflicting name aliases | Block; never replace the supplied ID or silently ignore a name |
| Missing both ID and name; malformed, fractional or precision-lost ID | Block before lookup |
| No match, inactive BU, unknown ActiveFlag, multiple matches or incomplete paging | Block without fallback or guessed values |
| AR-only update with existing BU ID and no new name | Resolve existing mapping; no new BU name required |
| Update changes BusinessUnit name with existing BusinessUnitId context | Resolve new name; validate ID against existing mapping; never PATCH BusinessUnitId |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCT.VALIDATE_PARENT | step | 1 | validate_input | valid->CJMCT.VALIDATE_CHILD_MAPPINGS;invalid->RETURN_ISSUES | none | stop | Validate explicit create/update intent and operation-specific parent inputs; defer current-value checks to VALIDATE_UPDATE |
| CJMCT.VALIDATE_CHILD_MAPPINGS | step | 2 | validate_input | valid->CJMCT.FIND_BUSINESS_UNIT;not_applicable->CJMCT.FIND_BUSINESS_UNIT;invalid->RETURN_ISSUES | CJMCT.VALIDATE_PARENT | stop | A request includes zero or more businessUnitLevelMappings child rows |
| CJMCT.VALIDATE_UPDATE | decision | 10 | validate_input | valid->CJMCT.CONFIRM_UPDATE_GATE;unchanged->CJMCT.RETURN_NO_CHANGE;invalid->RETURN_ISSUES | CJMCT.FIND_EXISTING_MAPPINGS | stop | Require update intent, exact existing identities and complete current values; validate writable changes, effective dates, sparse/no-null semantics and repeated targets |
