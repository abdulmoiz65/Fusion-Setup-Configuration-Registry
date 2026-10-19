# Costing of Payrolls Input Validation

Apply rules only to their declared operation. COP.SELECT_OPERATION validates
the requested operation and selects Search or the existing HDL branch;
branch-specific input checks run in that branch's validation node.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Search, Create, Update, End Date, or Zap | Blocked | Select the requested branch only. Correct, account-only Delete and Delete (ED Split) remain unsupported; never substitute a route. | Every request | |
| Search environment | Exact target environment and host selected by the active project workflow | Blocked | Resolve the environment, identity, and read privileges through the active workflow before a lookup. | Search | |
| Search filters | Optional payroll_name_search, effective_date, costing_filter, LDG names or IDs, and one period-type code or label | Defaults apply to omitted name, date, and costing state only | Apply the Search defaults, then resolve requested LDG names and period choices through the Search lookup nodes. | Search | |
| Search result scope | Payroll costing summary, LDG choices/context only, or period-type choices only | Use payroll costing summary for a normal Search request | Honor an explicit request for choices/context only and return from its lookup without running the main payroll search. | Search | |
| Create payroll selector | PayrollId or an exact PayrollName; LegislativeDataGroupName or LDGId; EffectiveStartDate | Blocked | Supply the business selectors and requested start before external reads. Resolve canonical HDL keys through the Create identity node; do not require the user to know technical IDs. | Create | resolve_create_payroll |
| Update payroll identity | PayrollId or exact PayrollName; LegislativeDataGroupName or LDGId; EffectiveStartDate | Blocked | Resolve the canonical PayrollCode, LDG and flex through the Update reference node. Do not ask for a business EffectiveEndDate. | Update | resolve_create_payroll |
| Update cost allocation account rows | Explicit target subtype and changed segment values; current complete account distribution from Fusion | Blocked | Resolve current accounts and preserve all unmodified values and proportions. The verified Update contract changes segments of the sole COST row and carries existing DFLT/SUSP forward unchanged. | Update | query_payroll_costing |
| Create account distribution | At least one COST, SUSP, or DFLT account with an explicit percentage and segment values or a permitted full account | Blocked | Validate against the selected LDG's runtime KFF. EffectiveDate is derived from the requested Create start and need not be supplied separately. | Create before archive preparation | validate_payroll_costing_segments |
| HDL source and target | UTF-8 HDL source; exact target environment; immutable archive preview | Blocked | Build and validate the source through core.data-loader before approval. | Before an import handoff | |
| End Date request | PayrollId or exact PayrollName; LDG name or ID; explicit target EffectiveStartDate; separate requested EffectiveEndDate | Blocked | Before authentication or live reads, request only missing business values. Resolve today once in the active workflow timezone when explicitly requested and show the resulting date. The end is inclusive; never reuse the selected start as the end. No account input is required. | End Date | |
| Zap request | Zap or Delete Record And History; exact payroll/LDG selectors and target EffectiveStartDate | Blocked | Normalize Delete Record And History to Zap. The start selects a logical allocation; no business end date or account distribution input is needed. Resolve all its historical account identities before preparation. | Zap | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Create: exact payroll/LDG identity, runtime KFF and account values, and absence of active costing are verified | Ready | Apply documented defaults and prepare the two-member HDL archive for validation. | |
| Update: the Cost Allocation key flexfield, hierarchy, legislative data group assignment, and payroll setup are confirmed | Ready | Continue to the verified effective-dated HDL Update route. | |
| Create, Update, End Date or Zap: a prerequisite or approved source value is absent | Blocked | Stop and obtain the missing setup or source value; do not invent an identity or lookup result. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Search date | If supplied, require a real calendar date in YYYY-MM-DD. Omission is handled by Search defaulting. Keep this REST date contract separate from HDL date formatting. | Search | |
| Search costing state | Accept All or all, WithCosting or with_costing, and WithoutCosting or without_costing. Reject conflicting or unknown states; normalize through the lookup's wire mapping. | Search | |
| Search filter shape | Accept one payroll search string, zero or more explicitly selected LDGs, and zero or one period type. A requested LDG or period filter must have a nonempty selection; do not treat an unresolved filter as omitted. | Search | |
| Search finder input | Reject finder grammar delimiters in payroll-name text and period input when their escaping is not source-backed; do not invent an escaping contract for comma, semicolon, or pipe. Reject unhandled quote or wildcard syntax in LDG name fragments rather than alter their meaning. URL encoding does not escape the decoded finder grammar. | Search before query assembly | |
| Create selector consistency | Preserve numeric PayrollId and LDGId values as exact identifiers. If both an ID and name are supplied, require them to identify the same returned row. Build query parameters from named values and encode once; if a name needs undocumented query-grammar escaping, obtain an exact selected ID instead of rewriting the name. | Create identity resolution | resolve_create_payroll |
| Date format | Accept requested costing dates in YYYY-MM-DD or YYYY/MM/DD, normalize to calendar dates, and render every HDL date as YYYY/MM/DD. REST lookup dates use YYYY-MM-DD. | Create, Update, End Date or Zap | |
| Create date input | Require EffectiveStartDate. Do not request a business EffectiveEndDate; Create derives 4712/12/31. Reject a different supplied end date and disclose that it describes an End Date operation. Each account EffectiveDate must equal the parent start; reject a conflicting supplied date. | Create | |
| Operation-specific end date | A requested end date belongs to End Date. Update handles the end internally; same-start-date Correct preserves it. These date rules do not enable the currently unsupported Correct execution branch. End Date uses its separate parent-only contract. | Update, Correct, or End Date interpretation | |
| Source type | Require PAY for CostAllocationV3 and CostAllocationAccountV3 payroll rows. | Every payroll HDL row | |
| Metadata and data pairing | Require one matching METADATA line before every MERGE or DELETE discriminator and preserve identical attribute order. | Every HDL member | |
| Record identity | Require PayrollCode and LegislativeDataGroupName; do not invent a source key, source type, or segment. | Every MERGE or DELETE row | |
| Account representation | Require the current validated template's permitted ConcatenatedSegment or Segment fields and explicit SourceSubType and Proportion. Defaulting assigns consecutive positive SubTypeSequence values starting at 1. | Existing Update branch | |
| Create account representation | Require populated individual runtime Segment values and empty ConcatenatedSegment for COST. Require one complete validated ConcatenatedSegment and empty Segment columns for SUSP or DFLT; a full account may be constructed from validated component input in runtime sequence with the runtime delimiter. | Every Create account row | validate_payroll_costing_segments |
| Create account cardinality and totals | Accept only COST, SUSP, and DFLT in this contract. Require each percentage from 0 through 100 and each rendered fraction from 0 through 1. Total each subtype separately: it must be from 0 through 1. SUSP and DFLT each allow at most one row and, when supplied, require Proportion 1. Do not sum different subtypes together or invent omitted accounts. | Create | |
| Create archive shape | Require exactly CostAllocationV3.dat and CostAllocationAccountV3.dat, encoded as UTF-8. Apply the Create DAT contract below, matching header/value counts, unique attributes, the same canonical payroll/LDG keys, and generated account sequences. Reject DELETE, SET instructions, and ReplaceLastEffectiveEndDate in a Create archive. | Create source/schema validation | |
| Create loader result | Require the approved archive's Content ID and Request ID and terminal success for both objects before verifying Fusion state. Initiated or pending returns a resume reference; a failed, unknown, or partial result is not successful Create. | Create after the one core.data-loader submission | |
| Update scope | Require exactly one COST row in the complete current distribution, an explicit segment change, and a new start strictly later than the latest open-ended history start. Preserve other accounts, account counts, percentages and all unchanged segments. Multiple COST rows, account additions/removals, a same-start Correct, end-dated latest state or an insertion before an existing future split is outside this tested contract; stop without substituting another operation. | Update | query_payroll_costing_history |
| Correct scope | Stop Correct as unsupported because this task lacks a source-backed HDL Correct contract. Do not require or use a REST write failure, reconciled-failure flag, or fallback approval. | Correct | |

## Create DAT Contract

These column contracts govern the runbook's DAT preparation and
core.data-loader validation. They are not alternative upload tools. Obtain the
current loader template through core.data-loader and stop on a conflicting
attribute contract; do not change that shared service or weaken validation.

| Member | Discriminator | Ordered Attributes After Discriminator | Records |
|---|---|---|---|
| CostAllocationV3.dat | CostAllocationV3 | EffectiveEndDate; EffectiveStartDate; SourceType; PayrollCode; LegislativeDataGroupName | One METADATA and one MERGE for the selected payroll/LDG Create. |
| CostAllocationAccountV3.dat | CostAllocationAccountV3 | SourceType; PayrollCode; LegislativeDataGroupName; EffectiveDate; SourceSubType; Proportion; SubTypeSequence; ConcatenatedSegment; runtime Segment columns | One METADATA header followed by one MERGE per approved account row, preserving supplied row order. |

The exact fixed headers are:

```text
METADATA|CostAllocationV3|EffectiveEndDate|EffectiveStartDate|SourceType|PayrollCode|LegislativeDataGroupName
METADATA|CostAllocationAccountV3|SourceType|PayrollCode|LegislativeDataGroupName|EffectiveDate|SourceSubType|Proportion|SubTypeSequence|ConcatenatedSegment
```

Extend the account header with the Segment columns confirmed by the runtime
descriptor and loader template, in numeric Segment column order. Use the
descriptor's sequence separately for building a full account; it must not
change a segment's physical Segment column mapping. Never hardcode the number
of segments from an example, omit interior empty values, or trim trailing
empty columns so that MERGE/header counts differ.

Apply HDL escaping to attribute values after building the account's logical
representation. In particular, when the runtime KFF delimiter is a vertical
bar, encode each bar inside ConcatenatedSegment as `\|` in the DAT; it is data,
not an HDL column separator. Escape a literal backslash as `\\` first and a
newline as `\n`. Validate column counts with an escape-aware parser and compare
decoded values with the immutable expectation. Never replace the runtime
delimiter with a dot or add SET FILE_DELIMITER to evade this contract.
See [Oracle: How You Manage Reserved Characters](https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/how-you-manage-reserved-characters.html).

| Field | Create Value or Constraint |
|---|---|
| Parent EffectiveEndDate | 4712/12/31, generated internally. |
| Parent EffectiveStartDate | Requested costing start in YYYY/MM/DD. |
| SourceType in both members | PAY. |
| PayrollCode in both members | The resolved canonical HDL payroll key; never PayrollId, SourceId, or a Search row Code. |
| LegislativeDataGroupName in both members | Canonical Name from the exact selected LDG response. |
| Account EffectiveDate | Exactly the parent EffectiveStartDate. |
| SourceSubType | Explicit COST, SUSP, or DFLT from the approved account input. |
| Proportion | Approved percentage divided by 100 once with decimal arithmetic. |
| SubTypeSequence | Generate 1 through N across the supplied account-row order, following this task's existing convention. Do not reset by subtype or copy the literal sequence from an Oracle example. |
| COST values | Empty ConcatenatedSegment; place validated values only in their descriptor-mapped Segment columns. |
| SUSP/DFLT values | Complete validated ConcatenatedSegment using runtime order and delimiter; every Segment column is empty. |
| Parent/account relationship | PAY, PayrollCode, LegislativeDataGroupName, and account EffectiveDate bound to the parent start identify the same allocation scope. Do not invent technical parent or account IDs for Create. |
| Account row key | Within that allocation scope, SourceSubType and generated SubTypeSequence identify each account row; require a unique pair and preserve it in the verification expectation. |

Normalize the user input before generating the immutable expected result.
Keep this expectation bound to the source and archive fingerprint for
post-load verification. A requested change after preview invalidates that
fingerprint and requires a new preparation/validation cycle.

## Verified Update Contract

The authorized live trial verified a new effective split with an omitted parent
EffectiveEndDate, full account carry-forward and a change to the sole COST row.
These rules are self-contained; a runtime must not read another task or trial
artifact. Other update shapes need their own evidence before execution.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Update state | Require complete history and one effective parent whose start/end match the latest history interval. The latest end must be 4712-12-31 and the requested start must be strictly later than its start. Capture the full history and account baseline before preparation. | Update | query_payroll_costing_history |
| Update distribution | Clone every current account into the new effective distribution, preserving response order for generated sequences. Change only the explicitly selected COST segments; preserve unmodified COST segments, including nulls, DFLT/SUSP full accounts and percentages. Reject an ambiguous target or an unexpected subtype. | Update | query_payroll_costing |
| Update account representation | Apply the same runtime-validated COST individual segments and SUSP/DFLT full-account representation and per-subtype totals used by Create. Validate every populated value at the requested new start. A partial business change is not a sparse DAT row. | Update | validate_payroll_costing_segments |
| Update archive | Require exactly CostAllocationV3.dat and CostAllocationAccountV3.dat in one immutable ZIP. Both begin with SET PURGE_FUTURE_CHANGES N. Only MERGE data rows are permitted; no DELETE or ReplaceLastEffectiveEndDate. | Update source validation | |
| Update parent columns | After the discriminator use EffectiveStartDate; SourceType; PayrollCode; LegislativeDataGroupName, in that order. Render one MERGE with the new start, PAY and canonical keys. Omit EffectiveEndDate from both METADATA and MERGE; do not write an explicit close row for the old interval. | Update source validation | |
| Update account columns | Use the Create account header order, including all descriptor-mapped runtime Segment columns. Render the complete current distribution with approved changes; EffectiveDate equals the new parent start. Generate SubTypeSequence 1 through N in retained row order and normalize percent to fractional Proportion once. Preserve HDL escaping and empty columns. | Update source validation | |
| Update expected effect | The old interval ends the day before the new start and keeps its account values. A new interval begins on the requested date and ends at the previously open end, with only approved account changes. Earlier history remains unchanged. Bind this expectation to the immutable archive. | Update preview and verification | |
| Update result | Accepted initiation is pending, not verified success. Require terminal success of the same approved load for both objects before comparing history, old accounts and new accounts. | Update result | |

## End Date DAT Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Last interval only | Require complete history and the supplied target start to identify exactly the latest interval. Require start less than or equal to requested end, and requested end less than or equal to current end. A later split, incomplete history, or attempted extension blocks the operation. | End Date preflight | query_payroll_costing_history |
| Already matching end | After complete baseline validation, equal requested/current end returns already_ended without a new archive or submission. | End Date preflight | query_payroll_costing |
| Parent-only archive | Require exactly CostAllocationV3.dat, one METADATA and one MERGE. Columns after CostAllocationV3 are EffectiveEndDate; EffectiveStartDate; SourceType; PayrollCode; LegislativeDataGroupName; ReplaceLastEffectiveEndDate, in that order. Render the requested inclusive end, unchanged selected start, PAY, canonical payroll/LDG keys and Y. | End Date source validation | |
| Excluded content | Reject CostAllocationAccountV3.dat, DELETE, every SET directive, blank dates, and #RETAIN, #ALL or #NULL date tokens. ReplaceLastEffectiveEndDate is a METADATA attribute with a matching MERGE value, never a SET instruction. | End Date source validation | |
| Date and encoding | Parse valid calendar dates and render YYYY/MM/DD. Require UTF-8, unique attributes, escaped values and matching header/value counts. Do not apply the Create end default or Update retain directive. | End Date source validation | |
| Special attribute | Retain ReplaceLastEffectiveEndDate=Y through core.data-loader validation. Its absence from the ordinary template/attribute list does not alone disprove component capability. A shared-validator rejection still blocks upload; never suppress it or remove the attribute to force a pass. | End Date source validation | |
| Expected result | Bind complete history and account baseline, selected start, current end and requested inclusive end to the immutable preview. Only the latest end may change; prior history and account values/counts/proportions must remain unchanged. | End Date preview and verification | |

## Zap DAT Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Zap parent DAT shape | CostAllocationV3.dat contains one METADATA and exactly one DELETE row, with columns EffectiveEndDate, EffectiveStartDate, SourceType, PayrollCode, LegislativeDataGroupName in that order. Use the latest end and earliest start of the selected logical history, PAY, and the resolved names. Both dates are required for this user-key DELETE; do not default an end-dated record to 4712/12/31. | Zap source validation | |
| Zap account DAT shape | Include CostAllocationAccountV3.dat only when zap_history_accounts is nonempty. Require one METADATA and one DELETE per distinct resolved physical account, using CostAllocAccountId, CostAllocationRecordId, EffectiveDate, SourceType, PayrollCode, LegislativeDataGroupName, SourceSubType in that order and the bound read values. Confirm these columns against the current Data Loader template. Identity-only DELETE rows omit Proportion, SubTypeSequence, ConcatenatedSegment, and all Segment columns; never generate account values or a replacement sequence. Parent-only requires zap_no_children_proven. | Zap source validation | query_payroll_costing_history_accounts |
| Zap archive shape | Require only the parent DAT and the conditional account DAT, matching METADATA/DELETE column counts, unique headers, and dates in YYYY/MM/DD. Reject MERGE, SET instructions, ReplaceLastEffectiveEndDate, and date tokens. Account DELETE targets must exactly cover the resolved child set. | Zap source validation before preview and handoff | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COP.SELECT_OPERATION | decision | 1 | validate_input | search->COP.SEARCH.VALIDATE_INPUT;hdl->COP.HDL.VALIDATE_INPUT;unsupported->COP.HDL.HANDLE_ERROR;invalid->COP.HDL.HANDLE_ERROR | none | stop | Validate the requested operation and route Search or HDL Create, Update, End Date or Zap. Correct, account-only Delete and Delete (ED Split) remain unsupported. |
| COP.SEARCH.VALIDATE_INPUT | decision | 2 | validate_input | valid->COP.SEARCH.APPLY_DEFAULTS;invalid->COP.HDL.HANDLE_ERROR | COP.SELECT_OPERATION | stop | Search: validate environment selection and supplied filter shapes; omitted optional filters continue to Search defaulting. |
| COP.HDL.VALIDATE_INPUT | decision | 10 | validate_input | valid_create->COP.CREATE.RESOLVE_IDENTITY;valid_update->COP.UPDATE.RESOLVE_STATE;valid_end_date->COP.END_DATE.RESOLVE_STATE;valid_zap->COP.ZAP.RESOLVE_STATE;invalid->COP.HDL.HANDLE_ERROR | none | stop | Validate operation-specific selectors and dates before reads. End Date requires a target start and separate inclusive end, not account input. |
| COP.CREATE.VALIDATE_SOURCE | decision | 25 | validate_input | valid->COP.HDL.ENFORCE_ROUTE;invalid->COP.HDL.HANDLE_ERROR | COP.HDL.CHECK_DEPENDENCIES,COP.CREATE.VALIDATE_SEGMENTS | stop | After Create lookups/defaults, the invoking runbook prepares both DAT members and the immutable ZIP through core.data-loader. Validate the Create DAT contract, loader schema, and Task Hook preview without submitting or requesting an earlier approval. |
| COP.CREATE.RESULT | decision | 42 | evaluate_result | terminal_succeeded->COP.CREATE.VERIFY;pending->COP.CREATE.PENDING;terminal_failed->COP.HDL.HANDLE_ERROR;timed_out->COP.HDL.HANDLE_ERROR;unknown->COP.HDL.HANDLE_ERROR | COP.HDL.GATE_CREATE | stop | Evaluate the exact submitted Create archive's Content ID, Request ID, and loader status; verification requires terminal success for both objects. |
| COP.UPDATE.VALIDATE_SOURCE | decision | 26 | validate_input | valid->COP.HDL.ENFORCE_ROUTE;invalid->COP.HDL.HANDLE_ERROR | COP.HDL.CHECK_DEPENDENCIES,COP.UPDATE.VALIDATE_SEGMENTS | stop | Enforce the verified Update DAT contract, exact immutable expectation, live loader schema and Task Hook preview before approval. |
| COP.UPDATE.RESULT | decision | 52 | evaluate_result | terminal_succeeded->COP.UPDATE.VERIFY;pending->COP.UPDATE.PENDING;terminal_failed->COP.HDL.HANDLE_ERROR;timed_out->COP.HDL.HANDLE_ERROR;unknown->COP.HDL.HANDLE_ERROR | COP.HDL.GATE_UPDATE | stop | Evaluate the same accepted Update load. Resume on an explicit status or verification request; no automatic resubmission. |
| COP.END_DATE.CHECK_STATE | decision | 22 | validate_input | valid->COP.END_DATE.APPLY_DEFAULTS;already_ended->COP.END_DATE.NO_CHANGE;invalid->COP.HDL.HANDLE_ERROR | COP.END_DATE.RESOLVE_STATE | stop | Validate the latest interval, explicit date bounds and complete baseline. Equal end is a verified no-op. |
| COP.END_DATE.VALIDATE_SOURCE | decision | 27 | validate_input | valid->COP.END_DATE.ENFORCE;invalid->COP.HDL.HANDLE_ERROR | COP.END_DATE.APPLY_DEFAULTS | stop | Validate the exact parent-only DAT and immutable archive through core.data-loader and Task Hook; preserve the special date-effectivity attribute. |
| COP.END_DATE.RESULT | decision | 56 | evaluate_result | pending->COP.END_DATE.PENDING;terminal_succeeded->COP.END_DATE.VERIFY;terminal_failed->COP.HDL.HANDLE_ERROR;timed_out->COP.HDL.HANDLE_ERROR;unknown->COP.HDL.HANDLE_ERROR | COP.END_DATE.GATE | stop | Return pending on accepted initiation; resume the same loader result only on explicit status or verification request, without resubmission. |
| COP.ZAP.CHECK_STATE | decision | 34 | validate_input | valid->COP.ZAP.CHECK_DEPENDENCIES;invalid->COP.HDL.HANDLE_ERROR | COP.ZAP.RESOLVE_ACCOUNTS | stop | Require one selector match, complete nonoverlapping logical history and exact detail coverage with consistent physical identities. No missing child set may be treated as empty. |
| COP.ZAP.VALIDATE_SOURCE | decision | 37 | validate_input | valid->COP.ZAP.ENFORCE;invalid->COP.HDL.HANDLE_ERROR | COP.ZAP.APPLY_DEFAULTS | stop | Validate the exact parent and conditional account DELETE members against the Zap contract and current core.data-loader DELETE/schema support. Prepare immutable archive and Task Hook preview; stop at actual validation failures. |
| COP.ZAP.RESULT | decision | 61 | evaluate_result | pending->COP.ZAP.PENDING;terminal_succeeded->COP.ZAP.VERIFY;terminal_failed->COP.HDL.HANDLE_ERROR;timed_out->COP.HDL.HANDLE_ERROR;unknown->COP.HDL.HANDLE_ERROR | COP.ZAP.GATE | stop | Accepted initiation is pending. On an explicit later status request require terminal success of the same Content ID/Request ID for every included object before verification. Never automatically replay a deletion. |
