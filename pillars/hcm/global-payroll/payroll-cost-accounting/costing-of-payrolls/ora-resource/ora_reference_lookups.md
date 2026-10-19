# Costing of Payrolls Reference Lookups

Search reads payroll costing summary rows and the LDG and period-type choices
needed to filter them. The contracts below are self-contained and derived from
supplied request/response evidence. All requests are GET, with no request body.
The resource paths use the developer-selected standard latest form. The
authorized Create and latest-interval Update trials verified the mutation
lookups and their post-load comparisons; this does not certify every Search filter.
The expanded LDG projection and flex aliases below were explicitly confirmed
by the developer in addition to the supplied request/response evidence.
Create and Update use the self-contained payroll identity, Generic Costing, runtime
KFF, and segment LOV contracts below. The common costing mechanics were
explicitly authorized for reuse with PAY and the selected PayrollId. They do
not depend on another task's resources at runtime.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_costing_ldg | Search includes LDG names or IDs to resolve, requests their flex structure, or asks to list LDG candidates; Create and Update always resolve one LDG and its flex structure. End Date and Zap resolve the canonical LDG without requiring flex validation. | Requested LDG names, name fragment, or IDs; selected target environment. | <host>/hcmRestApi/resources/latest/legislativeDataGroupsLOV; GET with the LDG query contract below. | LegislativeDataGroupId,Name,CostAllocationIdFlexNumber | Retrieve every page. A fragment returns candidates; resolve each requested name by exact Name equality or explicit user selection. For supplied IDs, retrieve the collection without a name q filter and match LegislativeDataGroupId exactly. Never select the first partial match. Create and Update require exactly one canonical returned Name and ID with a populated flex number. | LegislativeDataGroupId -> LDGId and selected LegislativeDataGroupIds; Name -> selected LDG names and canonical LegislativeDataGroupName for HDL; CostAllocationIdFlexNumber -> FlexNumId with CostAllocationIdFlexNum and IdFlexNum as confirmed aliases, scoped to that LDG | Zero matches for a requested filter: stop and request a corrected identity. Multiple candidates: return candidates and request selection unless Search explicitly requested multiple LDGs. An empty flex value remains absent for summary Search but blocks Create or Update KFF validation. |
| list_payroll_period_types | Search supplies a period-type code or label, or requests the available period types. | Period-type selection, if any; selected target environment. | <host>/hcmRestApi/resources/latest/payrollGenericLOV; GET with the Period type query contract below. | ResultValue1,Meaning | Resolve an explicit code against ResultValue1, or a display label against Meaning. Preserve the returned code exactly. | ResultValue1 -> period_type_code; Meaning -> period_type_label; items -> available_period_types | An unfiltered empty list is returned as empty. An unmatched requested selection or ambiguous label blocks filtering until corrected or selected. Multiple list entries are normal. |
| search_payroll_costing | Search inputs and optional LDG and period-type selections are resolved. | payroll_name_search; effective_date; costing_filter; selected LegislativeDataGroupIds, if any; period_type_code, if any; selected target environment. | <host>/hcmRestApi/resources/latest/payrollGenericLOV; GET with the Payroll costing query contract below. | Code,ResultValue1,ResultValue10,ResultValue11,ResultValue12,ResultValue2,ResultValue3,ResultValue4,ResultValue5,ResultValue6,ResultValue7,ResultValue8,ResultValue9 | Compose the declared finder criteria and aligned parameter values, preserving all requested filters. Map each item with the fixed DisplayAttributes order below. | items -> payroll_costing_results with PayrollId, PayrollName, PeriodType, PeriodTypeCode, LegislativeDataGroupId, LdgName, EffectiveStartDate, EffectiveEndDate, PayrollStartDate, PayrollEndDate, CostAllocationId, CostAllocationIdFlexNum | Empty results are a successful search with zero matches. Multiple results are normal; return them without choosing a mutation target. Report incomplete pagination explicitly and never present a partial result as complete. |
| resolve_create_payroll | Create, Update, End Date or Zap needs an exact payroll identity at its requested EffectiveStartDate. | Selected PayrollId or exact PayrollName; resolved LDG ID and canonical Name; Requested EffectiveStartDate. | <host>/hcmRestApi/resources/latest/payrollDefinitionsLOV; GET with the Create payroll identity query below. | PayrollId,PayrollName,LegislativeDataGroupId,LegislativeDataGroupName,EffectiveStartDate,EffectiveEndDate | Require one complete effective row matching the selected payroll and resolved LDG. Check the requested start falls within the returned payroll definition dates. Preserve the canonical returned name, including significant whitespace; do not substitute ReportingName or the Search Code. | PayrollId -> payroll_id and lookup_source_id; PayrollName -> canonical_payroll_name and HDL payroll_code, following the official Payroll HDL example's use of the payroll name as PayrollCode; returned LDG and definition dates -> payroll_identity_evidence | Zero, multiple exact rows, inconsistent LDG, missing identity, or incomplete pagination blocks the dependent operation. |
| query_payroll_costing | Create absence, Update or End Date preflight, or post-load verification (including Zap) requires parent and account state. | Exact payroll_id-derived SourceId; LDGId; SourceType PAY; operation-selected effective date; page size and offset. | <host>/hcmRestApi/resources/latest/genericCosting; GET with the Generic Costing query below. | Parent CostAllocationId,CostAllocationRecordId,EffectiveStartDate,EffectiveEndDate,SourceId,SourceType,LegislativeDataGroupId; expanded CostAllocationAccounts with CostAllocAccountId,SourceSubType,Account,Proportion,IdFlexNum,SubTypeSequence and CostPartialKff segment values | Require the exact PAY, SourceId, LDG, and requested effective-date context on every page. Before Create require zero effective parents. Update and End Date require one matching current parent and complete account expansion as their baseline. End Date preflight reads the selected start; its verification reads the requested end and the following day, requiring absence only on the following day. After successful Create/Update load require exactly one parent and compare complete accounts with the operation-specific immutable expectation. Post-Zap verification instead requires complete absence at every saved historical start; do not re-resolve a deleted allocation. | create_absence_evidence; effective_parent; ordered_accounts; verification_facts; verified_create_result | A matching active parent blocks Create; Update requires that parent. A same-start request is unsupported Correct. Multiple parents, mismatched identity, incomplete child expansion, or failed reads are not absence or success. |
| resolve_runtime_costing_kff | Create or Update validates and prepares account representations. | The exact resolved LDG CostAllocationIdFlexNumber, also called IdFlexNum. | <host>/fscmRestApi/applcoreApi/latest/flexfields/runtime/x/describe?discrValue={IdFlexNum}&x=oracle.apps.hcm.payrolls.costs.setup.restModel.view.CostAllocationAccountsVO%23CostPartialKff; GET only | Presented API field,title,sequence,segmentColumnName,declared LOV contract,discriminatorValue,delimiter | Bind the descriptor to the resolved flex discriminator. Retain presented segments, exact segmentColumnName mappings, runtime ordering, and delimiter; do not assume eight segments or a dot delimiter. Require complete and unique metadata for each supplied segment. | runtime_segment_definitions; runtime_segment_columns; runtime_lov_contracts; runtime_delimiter; id_flex_num | Missing or conflicting metadata, discriminator mismatch, missing required LOV bindings, or a delimiter needed for a full account blocks the dependent operation. |
| validate_payroll_costing_segments | Create or Update has resolved the descriptor and must validate supplied or carried-forward account values and full SUSP/DFLT accounts. | Runtime segment definitions, supplied values, current IdFlexNum, effective date and any context required by the declared LOV binding. | GET the runtime-declared LOV serviceRef on the selected environment, with its declared finder and bind values; resolve the dynamic contract only from resolve_runtime_costing_kff. | Declared value field and display fields, paging metadata, required dependent-segment values | For each populated segment, use its descriptor mapping. Where a LOV is declared, resolve all binds and require exactly one matching value from a complete result; retain its display value. For a full account, decompose in runtime sequence with the runtime delimiter before component validation. Segments without a LOV follow only descriptor-declared type/required constraints. | validated_segment_values; validated_account_rows; user_account_segments; user_full_account | Unknown fields, missing required segments/binds, invalid values, ambiguous matches, incomplete paging, or an undeclared service URL block preparation. Do not invent a value, LOV, or account. |
| query_payroll_costing_history | Update, End Date or Zap preflight, or post-load verification, requires complete effective history. | Resolved PayrollId; exact LDGId; SourceType PAY; page size and offset. | <host>/hcmRestApi/resources/latest/payrollGenericLOV; GET with the PAY history query below. | Code,ResultValue1,ResultValue2,ResultValue3,ResultValue4,ResultValue5; count,offset,limit,hasMore | Resolve all pages; map Code to CostAllocationId and ResultValue1/2 to start/end. Require valid nonoverlapping descending intervals, unique allocation/start pairs and the selected identity context. Update requires one logical allocation with latest end 4712-12-31 and a requested start strictly after that latest start. End Date instead requires the supplied target start to equal the latest history start, and the requested inclusive end to fall between that start and its current end; do not require an open end for End Date. Zap binds the supplied start to exactly one history row, then retains every split of that CostAllocationId, including earlier and later splits. After Zap, compare against saved identities without requiring the deleted selector to resolve again. | complete_effective_history;latest_effective_parent;update_history_baseline;zap_history_keys | Missing, ambiguous, invalid or incomplete history blocks preflight. Empty history is valid only for expected post-Zap absence. For Update, a same-start request is Correct and an insertion before a later split is unsupported. |
| query_payroll_costing_history_accounts | Zap preflight or approval freshness after complete history is resolved. | Each distinct CostAllocationId and EffectiveStartDate in zap_history_keys; resolved PayrollId SourceId; PAY; exact LDG ID; historical end date. | GET <host>/hcmRestApi/resources/latest/genericCosting/{CostAllocationId},{EffectiveStartDate}?expand=CostAllocationAccounts, once per history key; encode path values and query once. | Parent CostAllocationId; CostAllocationRecordId; EffectiveStartDate; EffectiveEndDate; SourceId; SourceType; LegislativeDataGroupId; complete CostAllocationAccounts with CostAllocAccountId, SourceSubType, EffectiveDate when returned, Proportion, Account, and populated Segment fields. | Accept one direct item or unwrap exactly one terminal collection item. Require all parent IDs, dates, PAY, SourceId, and LDG to match the history key and resolved context. Require a complete child array or items collection with hasMore=false; a missing expansion is not an empty collection. Preserve each child's physical ID and its bound parent's CostAllocationRecordId. Use the returned child EffectiveDate when present, otherwise the bound parent's EffectiveStartDate. Retain one DELETE target per distinct CostAllocAccountId; repeated observations must agree on parent record and account identity, otherwise stop. Require one matching detail response for every history key and retain immutable evidence. Runtime KFF is not required for deleting resolved identities. | zap_history_parents; zap_history_accounts; complete_history_account_fanout; zap_no_children_proven. | Stop on missing or extra details, source/date mismatch, incomplete paging, missing physical IDs, or conflicting duplicate child identity. Parent-only is valid only when every historical detail explicitly has zero children. |

## Create Payroll Identity Query

```text
GET <host>/hcmRestApi/resources/latest/payrollDefinitionsLOV
effectiveDate=<create_effective_start_YYYY-MM-DD>
q=PayrollId=<selected_payroll_id> and LegislativeDataGroupId=<resolved_ldg_id>
fields=PayrollId,PayrollName,LegislativeDataGroupId,LegislativeDataGroupName,EffectiveStartDate,EffectiveEndDate
onlyData=true
limit=<page_size>
offset=0
```

When selecting by exact name, replace the PayrollId predicate with
PayrollName='<selected_payroll_name>', retaining the LDG predicate. Discovery
through Search may supply the selected PayrollId, but its Code is never an HDL
key. Oracle documents PayrollName rather than PayrollCode on this resource.
The official Payroll HDL example uses the payroll name in the PayrollCode
column of both objects. Combining those contracts, map the uniquely resolved
canonical PayrollName to HDL PayrollCode; do not request a nonexistent
PayrollCode REST field or derive it from the technical PayrollId. The current
loader template remains a required validation gate for this HDL user key.
The canonical PayrollName-to-PayrollCode mapping was confirmed by the
authorized successful Create and Update loads and their parent/account reads.
If the loader rejects the payroll key, stop and investigate the backend key
contract separately rather than guess another value or resubmit automatically.
The payroll definition dates bound identity validity and are not the costing
parent's requested start and default end dates.

Send REST-Framework-Version: 9 and combine q predicates with the advanced
expression operator `and`. Do not use the framework-version-1 semicolon
separator inside q; it produces an unexpected-expression-token error in the
tested payroll definition resource. The semicolon in a documented finder
value belongs to a different grammar and remains unchanged.

## Generic Costing Query

```text
GET <host>/hcmRestApi/resources/latest/genericCosting
effectiveDate=<create_effective_start_YYYY-MM-DD>
finder=findByLegislativeDataGroupIdSourceTypeSourceId;LegislativeDataGroupId=<ldg_id>,SourceId=<payroll_id>,SourceType=PAY
expand=CostAllocationAccounts.CostPartialKff
limit=<page_size>
offset=0
```

SourceId is the resolved PayrollId. It is not PayrollCode, PayrollName,
CostAllocationId, CostAllocationRecordId, a department identifier, or a Search
row Code. Use the requested costing start date for the active-parent check,
not today's Search default. A successful complete empty collection establishes
absence at that date only. Search costing flags and a missing summary
CostAllocationId do not replace this check.

An existing active parent ends the Create branch before archive preparation.
Present Update or same-start-date Correct as separate operation choices; do
not automatically change operation or reuse Create approval. Correct's date
semantics are recorded, but its execution remains outside this Create step.

## Create Account Verification

| Check | Expected Result |
|---|---|
| Loader outcome | The same approved archive has a terminal successful core.data-loader result for both DAT members; an accepted request or partial success is insufficient. |
| Parent identity | Exactly one effective parent with PAY, the resolved PayrollId as SourceId, and the resolved LDG ID. Retain the returned allocation and record IDs in active runtime context. |
| Parent dates | EffectiveStartDate equals the requested Create start and EffectiveEndDate equals 4712-12-31. Do not substitute payroll definition dates. |
| Account coverage | A complete CostAllocationAccounts expansion has exactly the expected number of rows and subtypes. An absent expansion is not an empty account list. Match the expected subtype, generated SubTypeSequence, and validated account values rather than relying on response order. |
| Account identity and values | Require returned account IDs and compare each populated runtime Segment column through its descriptor mapping. For SUSP/DFLT compare the returned full account or its complete normalized components against the approved full account; preserve leading zeros. IdFlexNum must match the selected LDG flex structure. |
| Proportions | For this Create verification, Generic Costing returns percentages from 0 through 100. Divide by 100 once using decimal arithmetic before comparing with fractional HDL Proportion. Do not compare a returned 100 directly to HDL 1. |
| Success | Report verified Create only when all parent and account comparisons pass. A missing value, unexpected extra row, partial expansion, or mismatch yields a classified failure with expected-versus-actual facts. Do not replay the import. |

## Create Lookup Execution Rules

The runtime descriptor exposes `segments`, ordered `segmentApiNames`, and
per-segment `sequenceNumber`, `segmentColumnName`, `isPresented`, `isRequired`,
and `lov`. Use sequenceNumber for logical account order. Match an uppercase
SEGMENT column to the exact corresponding Segment attribute in the live loader
template; do not assign columns from a segment's position or title alone.
The descriptor's LOV `parameters.finder` can already be percent-encoded:
decode that value once before passing it as a named query value to the client,
which encodes it for transport. Bind a declared FLEXFIELD.VALIDATION_DATE to the
requested costing date. Resolve all other clientBindVariables from their
declared context; retain optional/required distinctions rather than inventing
binds. A successful LOV value lookup must still have complete pagination.

| Situation | What Happens |
|---|---|
| Identity node | COP.CREATE.RESOLVE_IDENTITY runs resolve_costing_ldg, then resolve_create_payroll. It retains one exact LDG, its canonical Name and flex, and one exact payroll valid at the requested start. |
| Absence node | COP.CREATE.CHECK_ABSENCE runs only query_payroll_costing before KFF work or archive preparation. Existing active costing is a Create blocker. |
| KFF node | COP.CREATE.RESOLVE_KFF runs resolve_runtime_costing_kff. Construct the descriptor query from raw named values and encode once; the %23 shown in the URL represents a literal hash in the x query value. |
| Segment node | COP.CREATE.VALIDATE_SEGMENTS runs validate_payroll_costing_segments after the descriptor node. Never hardcode segment positions, LOV services, bind names, or display labels from an example. |
| Verification node | COP.CREATE.VERIFY runs query_payroll_costing after the exact loader result is terminal-successful, and applies Create Account Verification to the saved immutable expectation. |
| REST route | Use core.fusion-api.rest-api-client GET only, after active workflow environment, identity, privileges, input, and diagnostic prerequisites pass. Runtime LOV references must resolve to the selected configured environment; no writes or alternate clients are selected by these lookups. |
| Continuation and diagnostics | Require complete parent and child collections and stop on paging errors or no progress. Retain partial successes with an errors array and nonzero failure status. Persist only redacted diagnostic facts under the active project policy; never copy tokens, raw customer payloads, or session paths into this skill. |

## LDG Query Contract

```text
GET <host>/hcmRestApi/resources/latest/legislativeDataGroupsLOV
finder=findByWord;
fields=LegislativeDataGroupId,Name,CostAllocationIdFlexNumber
orderBy=Name
limit=25
offset=0
```

To search a name fragment, add this decoded query value:

```text
q=UPPER(Name) like UPPER('%<ldg_name_fragment>%')
```

Omit q when listing candidates or matching supplied LDG IDs against the
collection. The developer also confirms that omitting fields returns the flex
attribute in the default projection; prefer the explicit projection above.

| REST Field | Task Context | Meaning |
|---|---|---|
| LegislativeDataGroupId | LDGId; selected LegislativeDataGroupIds | LDG identity for the search filter and the associated flex context. |
| Name | Selected LDG name | Display and exact name matching. |
| CostAllocationIdFlexNumber | FlexNumId; CostAllocationIdFlexNum; IdFlexNum | Confirmed names for the same LDG flex structure value within costing context. The REST projection must use CostAllocationIdFlexNumber, not one of the aliases. |

Keep each flex value attached to its LDG identity. Do not collapse multiple LDG
results into a single FlexNumId. An empty flex value is unavailable information,
not zero and not evidence that the LDG itself is missing. When both this lookup
and a payroll summary provide a nonempty flex value for the same LDG, compare
them; disclose a conflict and stop rather than silently overwrite either one.

## Period Type Query Contract

```text
GET <host>/hcmRestApi/resources/latest/payrollGenericLOV
finder=findByWord;PayRestName=HcmLookupValuePVO,AdditionalViewCriteria=findByLookupType,ParameterKeys=LookupTypeBindVar,ParameterValues=PAY_PROC_PERIOD_TYPE,DisplayAttributes=LookupCode||Meaning||Description
fields=ResultValue1,Meaning
onlyData=true
```

The unfiltered request above is sufficient to retrieve the choices. An empty
selection expression is not needed. These are period types/frequencies, not
individual payroll calendar periods, time-period IDs, or date ranges.

| Returned Field | Meaning | Use |
|---|---|---|
| ResultValue1 | LookupCode | Pass this exact code as pPeriodType. |
| Meaning | Display label | Show it to the user; do not send the label as the code. |

Examples of supplied reference pairs are Week / Weekly and Bi-Month /
Bimonthly. Retrieve current choices rather than treating these examples as a
complete fixed enumeration. Only one selected period type is evidenced; do not
invent a multi-value pPeriodType encoding.

## Payroll Costing Query Contract

```text
GET <host>/hcmRestApi/resources/latest/payrollGenericLOV
finder=findByWord;AdditionalViewCriteria=<criteria>,ParameterKeys=<parameter_keys>,ParameterValues=<parameter_values>,PayRestName=PayrollCostSearchVO,DisplayAttributes=PayrollId||PayrollName||PeriodType||PeriodTypeCode||LegislativeDataGroupId||LdgName||EffectiveStartDate||EffectiveEndDate||PayrollStartDate||PayrollEndDate||CostAllocationId||CostAllocationIdFlexNum
q=PayRestName = 'PayrollCostSearchVO'
fields=Code,ResultValue1,ResultValue10,ResultValue11,ResultValue12,ResultValue2,ResultValue3,ResultValue4,ResultValue5,ResultValue6,ResultValue7,ResultValue8,ResultValue9
limit=10000
onlyData=true
```

Build the three finder values as follows; examples are decoded query values.

```text
Base:
  criteria = findBySearchString
  parameter_keys = pCostingFilter||pSearchStr||pEffectiveDate
  parameter_values = <costing_filter>||<payroll_name_search>||<YYYY-MM-DD>

With selected LDGs, append to the corresponding values:
  criteria += ||findByLegislativeDataGroupIds
  parameter_keys += ||pLegislativeDataGroupIds
  parameter_values += ||<ldg_id_1>|<ldg_id_2>

With a selected period type, append to the corresponding values:
  criteria += ||findByPeriodType
  parameter_keys += ||pPeriodType
  parameter_values += ||<period_type_code>
```

Use a single pipe between selected LDG IDs and a double pipe between parameter
slots. A single selected LDG is one ID without a pipe. When both optional
filters are present, append LDG before period type. ParameterKeys and
ParameterValues must have the same number of double-pipe-separated slots.
Omit an unused criterion, key, and value together; do not leave empty slots.

| Filter | Wire Contract | Interpretation |
|---|---|---|
| Payroll Name | pSearchStr receives the supplied search text; percent sign alone means no name restriction. | Captured text searches return partial-name matches, including matches away from the start of the name. Do not treat them as exact identity resolution or infer case/accent behavior. |
| Effective date | pEffectiveDate receives YYYY-MM-DD. | Query state at the selected date; changing this date is not a request for all effective history. |
| All | pCostingFilter=all | Include rows with and without costing at the selected date. |
| WithCosting | pCostingFilter=with_costing | Request the service's rows with costing at the selected date. |
| WithoutCosting | pCostingFilter=without_costing | Request the service's rows without costing at the selected date. |
| LDG | pLegislativeDataGroupIds receives selected LegislativeDataGroupId values. | Use resolved identities, not LDG names, as parameter values. Multiple selected LDGs are evidenced. |
| Period | pPeriodType receives the selected ResultValue1 from list_payroll_period_types. | This is the period-type code, not Meaning or a payroll calendar-period identifier. |

## Filter Combinations

These decoded examples use synthetic values. Substitute runtime selections;
none of the values below is a configured environment or record identity.

```text
Name + effective date, all costing states:
  AdditionalViewCriteria=findBySearchString
  ParameterKeys=pCostingFilter||pSearchStr||pEffectiveDate
  ParameterValues=all||Example Payroll||2026-01-15

Effective date only, all costing states:
  AdditionalViewCriteria=findBySearchString
  ParameterKeys=pCostingFilter||pSearchStr||pEffectiveDate
  ParameterValues=all||%||2026-01-15

Two selected LDGs + effective date:
  AdditionalViewCriteria=findBySearchString||findByLegislativeDataGroupIds
  ParameterKeys=pCostingFilter||pSearchStr||pEffectiveDate||pLegislativeDataGroupIds
  ParameterValues=all||%||2026-01-15||<ldg_id_1>|<ldg_id_2>

Period type + effective date:
  AdditionalViewCriteria=findBySearchString||findByPeriodType
  ParameterKeys=pCostingFilter||pSearchStr||pEffectiveDate||pPeriodType
  ParameterValues=all||%||2026-01-15||Bi-Month

Name + LDG + period type + effective date + costing state:
  AdditionalViewCriteria=findBySearchString||findByLegislativeDataGroupIds||findByPeriodType
  ParameterKeys=pCostingFilter||pSearchStr||pEffectiveDate||pLegislativeDataGroupIds||pPeriodType
  ParameterValues=with_costing||Example Payroll||2026-01-15||<ldg_id>||Week
```

Changing only the first ParameterValues slot to all, with_costing, or
without_costing changes the costing filter while preserving the other filters.
A captured combined search returning no rows still demonstrates the request
shape; it does not establish that matching records exist.

## Search Result Mapping

Map by the fixed DisplayAttributes positions, not JSON property order or the
lexicographic order of fields. Numeric-looking identities arrive as strings;
retain their exact representation.

| Response Field | Business Field | Interpretation |
|---|---|---|
| Code | Search row code | Opaque row code; not PayrollCode or PayrollId. Do not parse it to manufacture an HDL identity. |
| ResultValue1 | PayrollId | Payroll identifier. It is not a supplied HDL PayrollCode. |
| ResultValue2 | PayrollName | Payroll display name. |
| ResultValue3 | PeriodType | Period-type display value. |
| ResultValue4 | PeriodTypeCode | Period-type code. |
| ResultValue5 | LegislativeDataGroupId | LDG identifier associated with this payroll row. |
| ResultValue6 | LdgName | LDG display name. |
| ResultValue7 | EffectiveStartDate | Costing effective start date; may be an empty string. |
| ResultValue8 | EffectiveEndDate | Costing effective end date; may be an empty string. |
| ResultValue9 | PayrollStartDate | Payroll start date, separate from costing dates. |
| ResultValue10 | PayrollEndDate | Payroll end date, separate from costing dates. |
| ResultValue11 | CostAllocationId | Cost allocation identifier; may be an empty string for a row without costing. |
| ResultValue12 | CostAllocationIdFlexNum | Flex structure value returned on this search row; may be empty and may also be populated when CostAllocationId is empty. FlexNumId and IdFlexNum are developer-confirmed costing aliases. Keep the raw returned value and distinguish it from an LDG lookup's CostAllocationIdFlexNumber. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Runtime route | Use core.fusion-api.rest-api-client only when the active project workflow reaches this read-only Search step and its task, environment, identity, privilege, and diagnostic prerequisites pass. Use the selected environment host; requests have no body. Authoring these contracts does not run them. |
| Query encoding | Build named query parameters and URL-encode each value once through the declared client. Encode percent signs and pipe delimiters as query data; preserve their decoded finder semantics. Never concatenate unvalidated user text into a raw URL. |
| Optional LDG resolution | COP.SEARCH.RESOLVE_LDG calls only resolve_costing_ldg when LDG names, IDs, flex context, or candidates are requested. If no LDG lookup is needed, skip it. Resolve every requested selection before using it as a filter; the returned identity and flex value do not establish broader costing setup readiness. |
| Optional period resolution | COP.SEARCH.RESOLVE_PERIOD calls only list_payroll_period_types when a code, label, or list is requested. Otherwise skip it. Pass a selected code to the search only after a unique match. |
| Choices or LDG context only | If the request is only for LDG choices/context or period-type choices, return listed from the corresponding lookup after complete pagination and end at its dedicated terminal. Do not run the main payroll search. If a requested filter still needs a selection, return blocked with candidates rather than listed or resolved. |
| Main lookup | COP.SEARCH.FIND calls only search_payroll_costing after the prior nodes have completed or explicitly skipped their optional lookup. Preserve the resolved filters for every page. |
| Pagination | Start at offset 0; the captured resource descriptions define offset as the starting collection position. While hasMore is true, request the same resource and query with offset equal to the response offset plus count. Require count to agree with the returned item count and positive progress. Never infer completeness from limit=10000 or the first LDG page. |
| Pagination failure | Stop on a failed page, repeated offset/page, zero progress with hasMore=true, or inconsistent collection metadata. Preserve already obtained results as explicitly partial with an errors array; return failure rather than empty or complete success. |
| LDG or period ambiguity | Return candidates and missing selection information. Do not select the first row, drop a filter, create setup, or broaden the request automatically. |
| Empty search | Return zero matches with the exact applied filters and effective date. Do not retry with fewer filters or claim that costing is absent at every date. |
| Missing costing values | Preserve empty CostAllocationId and costing date values as absent. Do not substitute payroll dates, zero, or a flex value. A populated CostAllocationIdFlexNum does not prove that the payroll has costing. |
| Flex context | Return selected LDG context separately from raw payroll summary rows. Resolve CostAllocationIdFlexNumber only from resolve_costing_ldg and summary CostAllocationIdFlexNum only from ResultValue12; the confirmed aliases do not change the REST field names or permit filling another LDG's values. |
| Result scope | Return summary identities, names, period type, costing and payroll dates, CostAllocationId, and CostAllocationIdFlexNum when present. This lookup does not return account rows or complete effective history and does not verify an HDL import. |
| Identity selection | Preserve distinct returned rows. A name match or a single displayed page is not sufficient to choose an HDL target. Search itself does not convert PayrollName, PayrollId, or Code into PayrollCode; Create separately resolves and validates the canonical payroll definition using resolve_create_payroll. |
| Response metadata | Discard session links and context metadata from reusable guidance and diagnostics. Construct every subsequent page from the declared standard resource and query values. Keep runtime identifiers only in the active context; persist sanitized summaries under the active project's policy. |

## PAY History Query

```text
GET <host>/hcmRestApi/resources/latest/payrollGenericLOV
finder=findByWord;AdditionalViewCriteria=findByLegislativeDataGroupIdSourceIdSourceType,ParameterKeys=pSourceId||pSourceType||pLegislativeDataGroupId,ParameterValues=<payroll_id>||PAY||<ldg_id>,PayRestName=PayCostSearchVO,DisplayAttributes=EffectiveStartDate||EffectiveEndDate||HistoryComments||LastUpdatedBy||LastUpdateDate,SortBy=EffectiveStartDate DESC
onlyData=true
limit=<page_size>
offset=0
```

Pass logical query values separately to the governed client for one encoding.
Map ResultValue3/4/5 to HistoryComments/LastUpdatedBy/LastUpdateDate. Retain only
sanitized facts in durable diagnostics. Complete all offset pages and reject
no-progress, duplicate or overlapping intervals. Do not use Search summaries
as a replacement for this history lookup.

## Update Lookup and Verification Rules

| Situation | What Happens |
|---|---|
| Transport | All Fusion GETs use core.fusion-api.rest-api-client and explicit REST-Framework-Version: 9. Numeric IDs can be JSON strings; compare exact decimal identifier strings without floating-point conversion. |
| Child expansion | With framework 9, CostAllocationAccounts and CostPartialKff can be collection objects with items and hasMore instead of arrays. Normalize both supported shapes. Require complete child pagination; if hasMore is true follow the returned same-host collection route through the governed client using the standard latest base and the same effective-date context. A missing expansion or a failed page is not an empty collection. |
| Update identity and state | COP.UPDATE.RESOLVE_STATE invokes resolve_costing_ldg, resolve_create_payroll, query_payroll_costing_history and query_payroll_costing. Read current costing at the requested new start; require it to match the latest complete history interval and bind all identities, dates and account values to the preview baseline. |
| Update KFF | COP.UPDATE.RESOLVE_KFF invokes resolve_runtime_costing_kff. COP.UPDATE.VALIDATE_SEGMENTS clones the current distribution, applies only explicit changes to the sole COST row and invokes validate_payroll_costing_segments for all populated new and retained values at the requested new start. Preserve leading zeros and existing empty COST segments. |
| Update verification gate | COP.UPDATE.VERIFY runs only after terminal success of the same approved archive for both objects. An accepted request or partial load is insufficient. |
| Update history comparison | Invoke query_payroll_costing_history. Require the same logical allocation, exactly one additional interval, the prior latest interval ending one day before the new start, and the new interval ending at the prior open end. Every earlier interval must be unchanged; reject extra, overlapping or missing history. |
| Update account comparison | Invoke query_payroll_costing at the day before the new start and at the new start. Require matching PAY, PayrollId and LDG; verify the expected dates and distinct parent record IDs. The old interval must retain its entire baseline distribution. The new interval must match the full expected distribution with only approved changes. Verify returned account IDs and flex; normalize percentage to fractional Proportion once. Match the unique subtype and account values, not response order; SubTypeSequence is not returned by every GET and must not be fabricated. |
| Scope of evidence | The verified contract updates segments of a sole COST account on the latest open-ended interval while carrying existing DFLT/SUSP unchanged. It does not establish sparse-account semantics, multiple COST selection, end-dated updates, future-split propagation, Correct, End Date or Zap. |

## End Date Lookup and Verification Rules

| Situation | What Happens |
|---|---|
| End Date scope | Resolve only canonical payroll and LDG identity, complete PAY history, and the parent/account baseline at the explicitly selected EffectiveStartDate. No KFF descriptor or value LOV is needed because account values are not rendered or changed. |
| End Date reads | COP.END_DATE.RESOLVE_STATE invokes resolve_costing_ldg, resolve_create_payroll, query_payroll_costing_history and query_payroll_costing. Reuse their exact standard latest GET contracts and framework 9. Bind the selected start to exactly one latest history row and require its allocation ID and start/end to match the detailed parent. Normalize exact string/numeric identifiers and complete child collections. |
| End Date baseline | Preserve every historical interval and all current account identities, subtypes, flex IDs, percentages, populated segment values and full Account values as immutable comparison evidence. A missing expansion is not an empty account set. Do not create account rows, normalize percentages or generate sequences. |
| End Date verification | After terminal success of the exact parent-only load, invoke query_payroll_costing_history and require the same number of intervals and logical allocation IDs. Only the selected latest end may change; its start and all prior intervals must be unchanged. At the inclusive requested end, query_payroll_costing must return the same selected start and an unchanged complete account distribution. On the next calendar day it must return a complete empty parent collection. Compare percentages directly, without HDL normalization. |
| Already ended | If the selected latest end already equals the requested end and baseline checks pass, report that verified current state without generating or submitting another load. Do not describe it as a new mutation. |

## Zap Lookup and Verification Rules

| Situation | What Happens |
|---|---|
| Zap identity and history | COP.ZAP.RESOLVE_STATE invokes resolve_costing_ldg, resolve_create_payroll and query_payroll_costing_history at the supplied selector start. Resolve canonical PayrollCode, LDG and SourceId PAY. Retain the selected logical allocation and all its historical keys, not only the selected split. No KFF descriptor or value LOV is needed. |
| Zap historical details | COP.ZAP.RESOLVE_ACCOUNTS invokes query_payroll_costing_history_accounts for every saved history key, including end-dated splits. Preserve exact physical account IDs, parent record IDs, effective dates and SourceSubType from complete responses. Apply framework 9 and the existing collection normalization rules. A missing expansion is not proof of zero children. |
| Zap baseline | Bind complete source/LDG identity, all history and physical account targets to the immutable archive. Deduplicate by exact CostAllocAccountId only when all bound identity fields agree. No user-supplied account target, generated sequence or transformed account value is used. |
| Zap verification | On an explicit status/verification request after terminal success of every included business object, reuse the saved payroll/LDG, logical allocation and historical keys. Invoke query_payroll_costing_history and require the targeted allocation absent on every page. Invoke query_payroll_costing at every saved historical start and require zero parents and no account expansion. Failed, incomplete or missing reads never prove absence. Do not require the deleted record to resolve again. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COP.SEARCH.RESOLVE_LDG | decision | 4 | reference_lookup | resolved->COP.SEARCH.RESOLVE_PERIOD;skipped->COP.SEARCH.RESOLVE_PERIOD;listed->COP.SEARCH.DONE_LDG;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.SEARCH.APPLY_DEFAULTS | stop | Search: call resolve_costing_ldg only for requested LDG names, IDs, flex context, or candidates; otherwise return skipped without a call. Return listed only for an LDG-only result scope. |
| COP.SEARCH.RESOLVE_PERIOD | decision | 5 | reference_lookup | resolved->COP.SEARCH.FIND;skipped->COP.SEARCH.FIND;listed->COP.SEARCH.DONE_PERIOD_TYPES;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.SEARCH.RESOLVE_LDG | stop | Search: call list_payroll_period_types only for a requested period type or choice list; otherwise return skipped without a call. Return listed only for a period-type-list-only result scope. |
| COP.SEARCH.FIND | decision | 6 | reference_lookup | found->COP.SEARCH.DONE;empty->COP.SEARCH.DONE;failed->COP.HDL.HANDLE_ERROR | COP.SEARCH.RESOLVE_PERIOD | stop | Search: call search_payroll_costing with all resolved filters; found or empty requires complete pagination. |
| COP.CREATE.RESOLVE_IDENTITY | decision | 11 | reference_lookup | resolved->COP.CREATE.CHECK_ABSENCE;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.HDL.VALIDATE_INPUT | stop | Create only: resolve the canonical LDG and flex, then the payroll definition and HDL identity. |
| COP.CREATE.CHECK_ABSENCE | decision | 12 | reference_lookup | absent->COP.CREATE.RESOLVE_KFF;exists->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.CREATE.RESOLVE_IDENTITY | stop | Create only: require zero active Generic Costing parents for PAY, PayrollId, LDG, and the requested start date. |
| COP.CREATE.RESOLVE_KFF | decision | 13 | reference_lookup | resolved->COP.CREATE.VALIDATE_SEGMENTS;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.CREATE.CHECK_ABSENCE | stop | Create only: retrieve the runtime descriptor for the selected LDG flex. |
| COP.CREATE.VALIDATE_SEGMENTS | decision | 14 | reference_lookup | valid->COP.HDL.APPLY_DEFAULTS;invalid->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.CREATE.RESOLVE_KFF | stop | Create only: validate the supplied account components using the runtime descriptor and its declared LOV contracts. |
| COP.CREATE.VERIFY | decision | 44 | reference_lookup | verified->COP.CREATE.DONE;failed->COP.HDL.HANDLE_ERROR | COP.CREATE.RESULT | stop | Verify the exact parent and account expectations only after terminal success for both Create DAT members. |
| COP.UPDATE.RESOLVE_STATE | decision | 16 | reference_lookup | resolved->COP.UPDATE.RESOLVE_KFF;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.HDL.VALIDATE_INPUT | stop | Update only: resolve canonical payroll/LDG/flex, complete PAY history and the matching current parent/account baseline using the Update lookup rules. |
| COP.UPDATE.RESOLVE_KFF | decision | 17 | reference_lookup | resolved->COP.UPDATE.VALIDATE_SEGMENTS;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.UPDATE.RESOLVE_STATE | stop | Resolve the current runtime descriptor for the Update LDG flex. |
| COP.UPDATE.VALIDATE_SEGMENTS | decision | 18 | reference_lookup | valid->COP.HDL.APPLY_DEFAULTS;invalid->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.UPDATE.RESOLVE_KFF | stop | Build the complete expected distribution with only explicit COST segment changes and validate all populated values at the new effective date. |
| COP.UPDATE.VERIFY | decision | 54 | reference_lookup | verified->COP.UPDATE.DONE;failed->COP.HDL.HANDLE_ERROR | COP.UPDATE.RESULT | stop | Apply Update history and account comparisons to the immutable baseline and expectation after terminal loader success. |
| COP.END_DATE.RESOLVE_STATE | decision | 21 | reference_lookup | resolved->COP.END_DATE.CHECK_STATE;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.HDL.VALIDATE_INPUT | stop | End Date only: resolve canonical payroll/LDG, complete history and the exact selected parent/accounts using the End Date lookup rules; skip KFF validation. |
| COP.END_DATE.VERIFY | decision | 58 | reference_lookup | verified->COP.END_DATE.DONE;failed->COP.HDL.HANDLE_ERROR | COP.END_DATE.RESULT | stop | Apply End Date history and inclusive-end/next-day account comparisons only after terminal success of the exact parent-only load. |
| COP.ZAP.RESOLVE_STATE | decision | 32 | reference_lookup | resolved->COP.ZAP.RESOLVE_ACCOUNTS;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.HDL.VALIDATE_INPUT | stop | Resolve canonical payroll/LDG and complete PAY history for the exact selector start; retain the entire selected logical allocation. |
| COP.ZAP.RESOLVE_ACCOUNTS | decision | 33 | reference_lookup | resolved->COP.ZAP.CHECK_STATE;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.ZAP.RESOLVE_STATE | stop | Invoke query_payroll_costing_history_accounts for every selected history key and retain complete physical child identities or explicit proof of no children. |
| COP.ZAP.VERIFY | decision | 63 | reference_lookup | verified->COP.ZAP.DONE;failed->COP.HDL.HANDLE_ERROR | COP.ZAP.RESULT | stop | Verify saved logical history and every historical start are absent only after terminal success of the same Zap load; never rediscover the deleted selector as a prerequisite. |

## Sources

- [Oracle: Working with REST API Framework Versions](https://docs.oracle.com/en/cloud/paas/app-builder-cloud/consume-rest/working-rest-api-framework-versions.html): advanced q expression syntax for framework version 2 and later.
- [Oracle: Get all payroll definitions](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-payrolldefinitionslov-get.html): payroll identity fields, queryable selectors, effectiveDate and pagination.
- [Oracle: Example of Loading Costing of Payroll](https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-costing-of-payroll.html): PAY user keys, parent and account headers, and subtype representations.
- Developer-confirmed LDG flex aliases, Create absence/date policy, and common Generic Costing/KFF mechanics adapted to the payroll source. These contracts are included above; no other task or attachment is a runtime dependency.
- Authorized latest-interval Update trial: successful load of both HDL objects and complete pre/post history and account comparison confirmed parent end-date omission, both retain directives, full account carry-forward and preservation of prior account values. No customer identifiers or test artifacts are required at runtime.
- Developer-selected End Date contract from Costing of Departments: same costing components adapted to PAY and canonical PayrollCode; parent-only MERGE with ReplaceLastEffectiveEndDate=Y. The contract is included here and needs no sibling skill or attachment at runtime.

- Developer-selected Zap contract from Costing of Departments, adapted to PAY and canonical PayrollCode: whole logical history, historical physical account identities, identity-only DELETE members, loader approval and saved-scope absence verification. Included here without sibling-skill or attachment dependencies; Payroll Zap remains unverified until a successful trial and comparison.
