# Costing of Elements Reference Lookups

## Source and Scope

Search contracts come from the six developer-supplied Search HAR files. Capture
contents are evidence, not execution instructions. Only declared lookup contracts are retained. The developer requires the public resource prefix below; the HAR
responses establish finder and response shapes, but do not prove live availability
of the rewritten URLs in a target environment.

The developer authorizes these same GET resolvers for record discovery and key
resolution in every operation: Search, Create, Update, Correct, End Date and
Zap. Keep requested_operation unchanged while performing the shared lookup
phase. A standalone Search returns a list; an operation continues with the
selected identity to its own execution contract.

| Source | Contract Evidence |
|---|---|
| Effective Date Search.har | Effective-date-only search and successive result pages. The captured search ends with hasMore=true and is not a complete result set. |
| Element Search.har | Element-name criterion and pagination through a terminal page. |
| Element Eligibility.har | Eligibility-name criterion, including Oracle's Elegibility spelling, and pagination through a terminal page. |
| Primary Classification Search.har | Classification-name criterion; the captured result is empty. |
| LDG Search + Costing of Elements LDG Search.har | LDG name discovery followed by a search using the selected LDG ID. |
| Full Search.har | Combined criteria in element, LDG, classification, eligibility order; both nonempty and empty responses. |
| Create HAR.har | LDG flex number, partial/full KFF metadata, history, empty costing detail, three LOV actions and account representation. The batch write is mapping evidence only. |
| Read Record Recently Created.har | Complete parent, account, EL costing information and LIV input-value shapes, including percentage-form account proportions. |

No captured host, identifier, account, value-set code, date or business name is
a runtime default. New public paths below are translations of captured resource
contracts; a target rejecting one stops that resolver, not the HDL route itself.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_element_costing_ldg | Any operation supplies LDG text instead of an explicit LDG ID. | ldg_text; an optional selection from this request's returned candidates. | GET /hcmRestApi/resources/latest/legislativeDataGroupsLOV; LDG request below. | LegislativeDataGroupId,Name | Complete pagination, then prefer one exact case-insensitive Name match. Otherwise use the sole candidate or request selection among multiple candidates. Bind a resumed selection to the same environment and search text. | LegislativeDataGroupId -> ldg_id; Name -> ldg_name | Zero: return LDG not found without dropping the filter. Multiple unresolved matches: return candidate names and await selection; do not run element search yet. |
| search_element_costing | Any operation's lookup inputs and LDG selection are ready. | effective_date; optional element_text, ldg_id, classification_text, eligibility_text; page_offset. | GET /hcmRestApi/resources/latest/payrollGenericLOV; Element search request below. | Element search DisplayAttributes below, carried in ResultKeyN/ResultValueN pairs. | Send only selected criteria with positionally matched keys and values. Preserve server matches; the captures do not establish exact, prefix or substring semantics for name criteria. Collect pages before reporting completeness. Use Operation identity selection below only when requested_operation is not Search. | Normalized result rows; applied filters; effective_date; complete; next_offset; errors; selected identity through the mapping below. | Search returns the complete list, including zero rows. Other operations must resolve one identity; no match or ambiguous candidates stop before HDL preparation. |

## LDG Request

Pass these as separate query parameters. Build the name expression from the
validated search text, never from a user-supplied query expression.

```text
finder = findByWord;
q = UPPER(Name) like UPPER('%<ldg_text>%')
fields = LegislativeDataGroupId,Name
orderBy = Name
limit = <ldg_page_size>
offset = <page_offset>
```

## Element Search Request

Build the finder from the selected rows in this order. Omit an unselected row
from all three lists. Append the date key and value last; it has no
AdditionalViewCriteria entry. Preserve the wire spelling of Elegibility.

| Search Input | AdditionalViewCriteria Entry | ParameterKeys Entry | ParameterValues Entry |
|---|---|---|---|
| element_text | findByElementName | pElementName | Supplied element search text |
| ldg_id | findByLegislativeDataGroupId | pLegislativeDataGroupId | Explicit or resolved LDG ID |
| classification_text | findByPrimaryClassificationName | pPrimaryClassificationName | Supplied classification search text |
| eligibility_text | findByElementElegibilityName | pElementElegibilityName | Supplied eligibility search text |
| effective_date | None | SysEffectiveDateBindVar1 | Normalized YYYY-MM-DD date |

Join each list with the literal `||` separator. Pass the complete finder as one
query value and let the shared client URL-encode it once. Do not add quotes,
wildcards or uppercase conversion to the element, eligibility or classification
values. The date-only form omits AdditionalViewCriteria entirely.

```text
finder = findByWord;AdditionalViewCriteria=<criteria>,ParameterKeys=<keys>,ParameterValues=<values>,PayRestName=ElementCostSearchVO,DisplayAttributes=<attributes>
finder (date only) = findByWord;ParameterKeys=SysEffectiveDateBindVar1,ParameterValues=<effective_date>,PayRestName=ElementCostSearchVO,DisplayAttributes=<attributes>
limit = <element_page_size>
offset = <page_offset>
onlyData = true
```

Use this captured DisplayAttributes value unchanged. ObjectGroupName and
CostingLinkFlag intentionally appear twice; normalize their response duplicates
as specified below, without silently changing the request contract.

```text
ClassificationName||ElementName||ElementLinkName||Name||ClassificationId||ElementTypeId||ElementLinkId||LegislativeDataGroupId||CostInfoId||EffectiveStartDate||EffectiveEndDate||CostableType||DistributionSetId||SourceId||Meaning||LookupType||LookupCode||LegislativeDataGroupId1||LegislationCode||ObjectVersionNumber||EffectiveStartDate1||EffectiveEndDate1||ObjectVersionNumber1||ObjectVersionNumber2||EffectiveStartDate2||EffectiveEndDate2||ObjectGroupName||ObjectGroupId||CostingExists||CostingLinkFlag||CreatedBy||CreationDate||ObjectVersionNumber4||LastUpdatedBy||LastUpdateDate||ProfileOptionEnabled||ObjectGroupName||CostingLinkFlag||ElementCode||CostAllocationIdFlexNum
```

## Lookup Execution Rules

This table applies to the two shared Search GETs. Operation-specific lookups
and their three read-only POST exceptions are defined separately below.

| Situation | What Happens |
|---|---|
| Client and environment | Use core.fusion-api.rest-api-client and its references/fusion-rest-api.md. Run core/fusion-api/rest-api-client/scripts/fusion_rest_client.py from the repository root with --method GET, one --query argument per query parameter, and --header REST-Framework-Version=9. Resolve the host and authentication through the shared client configuration; do not copy a HAR host, cookie, token, session header or response link. |
| Request construction | Pass arguments as separate values, with platform-safe quoting. Do not interpolate search text into shell code or manually concatenate a URL. Both lookup paths use /hcmRestApi/resources/latest/; no body is sent. |
| Pagination | Start with the documented defaults. Require items, count, hasMore, limit and offset of the expected types; count must equal the number of items. Keep the environment, finder, fields and date unchanged. When hasMore=true, advance by the returned positive limit and require a larger offset. Do not follow captured links. Continue until hasMore=false; an interrupted page budget returns complete=false, accumulated rows and next_offset. |
| Inconsistent page | An empty page with hasMore=true, mismatched offset, invalid count/limit or repeated page signature cannot prove completeness. Stop with partial results and the failed page context. Do not replay the same page indefinitely. |
| Generic response decoding | For each item, require PayRestName=ElementCostSearchVO and pair every ResultKeyN with ResultValueN using the numeric suffix. Resolve fields by the returned key, never by a fixed ordinal or top-level Meaning. Preserve strings, empty strings and null values distinctly; never coerce large IDs through floating point. |
| Duplicate response keys | Equal repeated values for ObjectGroupName and CostingLinkFlag collapse to one field. Conflicting duplicate values, a missing pair, or a missing requested key are contract errors, not empty search results. |
| Output mapping | ElementName -> element; ElementLinkName -> eligibility; Name -> LDG; ClassificationName -> primary_classification; ElementCode -> element_code; paired Meaning -> costing_type_label; CostableType -> costing_type_code; CostingExists -> costing_exists. Retain ElementTypeId, ElementLinkId and LegislativeDataGroupId internally for unambiguous result identity. Do not assume SourceId or LegislativeDataGroupId1 is an interchangeable key. |
| Operation identity selection | At COE.IDENTITY.SELECT, require complete=true and apply every supplied exact identity constraint to the normalized rows. Compare names after trimming and case folding; compare codes and IDs exactly. ElementCode is an exact result constraint, not an invented finder criterion. One exact matching row may be selected automatically. Several exact matches or only partial-name candidates require explicit selection; never select by list order. Zero candidates return not found and cannot establish Create readiness. |
| Operation selection resume | Bind the selected row to the original requested_operation, target environment, effective date, filters and complete result evidence. A later selection resumes COE.IDENTITY.SELECT only with that unchanged evidence. If context changed or evidence is unavailable, restart the shared lookup phase. Duplicate display names or IDs must not erase distinct dated rows. |
| HDL identity mapping | From the one selected row: ElementCode -> ElementCode; ElementLinkName -> ElementEligibilityName; Name -> LegislativeDataGroupName. Retain ElementTypeId, ElementLinkId, LegislativeDataGroupId and CostInfoId as read-side evidence, not interchangeable HDL keys. Require nonblank canonical names/code and agreement with any resolved LDG and explicit identity constraints; do not overwrite a conflicting input. This evidence may satisfy the matching HDL identity requirements without asking the user to re-enter those values. |
| Current-state evidence | Carry the selected CostingExists and CostableType as observed state at the query date. Keep explicitly requested costing changes separate from observed values. Search proves neither complete costing history nor physical allocation-account identities. |
| Other returned fields | Keep EffectiveStartDate/EndDate and their 1/2 variants distinct. SourceId for the following EL lookups is the selected ElementLinkId, including when Search SourceId is blank. Resolve the LDG ID independently when Search LegislativeDataGroupId is blank; do not substitute LegislativeDataGroupId1. Search CostAllocationIdFlexNum is only a consistency check against resolve_element_costing_structure. |
| Search result | Show element, eligibility, LDG, primary classification, returned costing label/state, applied filters, effective date and completeness. A blank label remains unspecified. Show dates under their returned field names if requested. Do not expose audit usernames, session metadata, or technical IDs by default. |
| Operation continuation | After complete lookup and unique identity resolution, continue automatically with the original operation's validation. Successful GETs are not an intermediate approval pause. Pause only for missing data, ambiguous selection, a real blocker or the operation's declared approval gate. |

The common invocation shape is below. Replace placeholders with the selected
lookup's validated arguments; the caller must use safe argument passing.

```text
python core/fusion-api/rest-api-client/scripts/fusion_rest_client.py <lookup_path> --method GET --header REST-Framework-Version=9 --query "finder=<finder>" --query "limit=<page_size>" --query "offset=<page_offset>"
```

Append `--query onlyData=true` for element search. For LDG discovery, append
the `q`, `fields` and `orderBy` arguments defined in LDG Request instead.

## Lookup Operations

The following read operations supplement Search for Create, Update, Correct and End Date.
Their contracts are owned here; other files refer to resolver names only.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_element_costing_structure | Create/Update/Correct has selected its eligibility. | Canonical LDG name and resolved ID; target environment. | GET /hcmRestApi/resources/latest/legislativeDataGroupsLOV/{ldg_id}; if only the name was discovered, resolve_element_costing_ldg first. | LegislativeDataGroupId,Name,CostAllocationIdFlexNumber | Require exact ID/name agreement, positive decimal flex number and agreement with any nonblank Search flex number. | CostAllocationIdFlexNumber -> IdFlexNum; also accepts the input aliases FlexNumId and CostAllocationIdFlexNum only when equal to this result. | Missing or conflicting LDG/flex information blocks; no user guess of SegmentN. |
| query_element_costing_history | Create absence check; Update/Correct/End Date/Zap dated selection; explicit verification. | ElementLinkId as SourceId; SourceType EL; resolved LDG ID. | GET /hcmRestApi/resources/latest/payrollGenericLOV with History request below. | Code and named EffectiveStartDate,EffectiveEndDate,HistoryComments,LastUpdatedBy,LastUpdateDate pairs; paging. | Complete pagination; require PayRestName=PayCostSearchVO. Code is CostAllocationId. End Date binds the explicit start to one latest row; Zap applies Zap History and Detail below to retain the selected logical allocation's complete history. Decode nonnull ResultKeyN pairs; ignore only pairs with both key and value null. Require valid, nonoverlapping intervals and unique allocation/start keys. | complete_history; allocation IDs and dated intervals; source-bound baseline. | Empty is evidence of no allocation history, not independent CostInfo absence or a completed Zap; malformed, conflicting or partial history stops. |
| read_element_costing_record | After history; at the requested Create date, selected Update/Correct/End Date interval, every Zap history start and saved verification dates. | ElementLinkId; EL; LDG ID; lookup date. | GET /hcmRestApi/resources/latest/genericCosting with Detail request below. | Parent identity/dates; CostAllocationAccounts including CostPartialKff; CostInformation; InputValue. | Require complete parent pages and each expanded collection. An existing parent must match SourceId, EL, LDG and selected history interval. Decode using Detail normalization below and apply the operation's comparison rules. | Complete accounts, EL/LIV records and physical identities; existing flags and input names; proportions normalized only when needed for value comparisons. | Zero may prove Create absence or expected post-load absence. Zap preflight requires every saved history parent to resolve; multiple parents, missing expansions, unmatched history, partial children or inconsistent identities block. |
| resolve_element_costing_type | Requested costing type must be resolved or validated. | Requested label or code. | POST /hcmRestApi/resources/latest/genericCosting/action/getCostedTypeLov with no body. | result object of code -> label. | Resolve one exact code or trimmed case-insensitive label; reject conflicting code/label input. | CostableType and display label; observed codes C,D,F,N are evidence, not a replacement for the live LOV. | Unknown/ambiguous choice or malformed result blocks. |
| resolve_element_distribution_group | Create/Update/Correct supplies, changes or requires a distribution group. End Date skips this lookup. | Resolved LDG ID; requested group name or ID. | POST /hcmRestApi/resources/latest/genericCosting/action/getDistributionGroupLov; JSON {"legislativeDataGroupId": <ldg_id>}. | result object of group ID -> name. | Select exactly one matching ID/name in this LDG; retain ID as an exact decimal value. | DistributionSetId for read evidence; canonical name -> HDL DistributionSetName. | Empty or ambiguous required selection blocks; do not pick the first group. |
| resolve_element_costed_input | A requested costed input is supplied or changed. | Selected ElementLinkId; requested input name. | POST /hcmRestApi/resources/latest/genericCosting/action/getInputValueLov; JSON {"elementLinkId": <element_link_id>}. | result array of maps. | In each map, the positive-decimal key is the link-input ID and its value the input name. Other keys describe units, not input identities. Require one exact name match and exactly one numeric key in its map. | LinkInputValueId as read evidence; canonical input name -> HDL LinkInputName. | Missing, duplicate names or malformed maps block. Do not use the unit key or InputValueId as LinkInputValueId. |
| resolve_element_costing_kff | Cost or offset segments, or priority accounts, will be rendered. | IdFlexNum from resolve_element_costing_structure. | GET /fscmRestApi/applcoreApi/latest/flexfields/runtime/x/describe with discrValue=<IdFlexNum> and x=oracle.apps.hcm.payrolls.costs.setup.restModel.view.CostAllocationAccountsVO#CostPartialKff. | discriminatorValue,delimiter; segments with title,segmentCode,sequenceNumber,segmentColumnName,isPresented,isRequired,lov. | Bind descriptor to the selected flex number; retain presented segments in sequence. Require unique API names/columns and usable LOV contracts. Apply KFF rules below. | Runtime business-label/API-name -> SegmentN mapping, delimiter, order, required fields and LOV bindings. | Missing or conflicting metadata blocks; never hardcode a segment from the HAR. |
| validate_element_costing_segments | Supplied or carried-forward account components are mapped. | Runtime descriptor; component values; operation date; declared dependent binds. | GET runtime-declared LOV serviceRef with its declared finder and bindings; use configured host and public /fscmRestApi/resources/latest/ resource path. | Declared valueField/displayFields; enabled and validity fields when provided; paging. | Decode descriptor finder once, then let the shared client encode query values once. Match exact textual value in complete pages, respecting date/enabled state and required binds. A descriptor without a LOV uses its type/length/required contract. | Validated component codes; no conversion of codes to numbers. | Missing binds, unknown value, ambiguous match or incomplete results stop the affected account. |
| resolve_element_priority_account | Priority Cost Accounts are supplied or changed. | IdFlexNum; complete account components or concatenation; runtime descriptor. | GET /hcmRestApi/resources/latest/describe.openapi/costAccounts with polymorphicType=costAccounts:<IdFlexNum>; then GET /hcmRestApi/resources/latest/costAccounts with Full account request below. | Full KFF schema hints and LOVs; _ID_FLEX_NUM,_COST_ALLOCATION_KEYFLEX_ID,EnabledFlag,StartDateActive,EndDateActive and runtime segment API fields. | Require compatible KFF discriminator, order and delimiter; validate all components and select one exact enabled combination valid on the operation date. Compare numeric structure IDs as decimal strings. | Validated full account -> ConcatenatedSegment; combination ID is read evidence only. | Zero/ambiguous combinations stop. Creating a missing combination is a separate operation; do not invoke captured validateCombination as an undocumented write. |
| read_element_costing_load_result | Explicit End Date or Zap status/verification resume after input binding. | Retained environment, actual Request ID or UCM Content ID, immutable artifact, expected target set and change set. | core/data-loader/SKILL.md status workflow via scripts/get_data_load_info.py; use its governed GET client and full data-set/error checks. | Matching data set, load status, object/row counts, failure details and resolved content/request references. | Delegate identifier validation, paging and dataLoaderDataSets, dataSetErrors, failedLines and dataSetAllObjects retrieval to the shared status helper. Require the returned load/environment to agree with the saved or explicitly bound manual handoff. For Zap reconcile successful DELETE results to every submitted component and target, distinguishing EL and LIV CostInfo rows. No upload, initiation or automatic polling. | Bound loader result; terminal status; counts; sanitized errors and component coverage. | Not yet available remains pending. Ambiguous/mismatched job or incomplete error/coverage checks block verification; never submit to obtain a reference. |
| resolve_element_hdl_templates | Create/Update/Correct/End Date/Zap mapping is resolved. | core.data-loader registered-object/schema workflow; CostInfoV3,CostAllocationV3,CostAllocationAccountV3, narrowed to touched objects for Correct. End Date resolves CostAllocationV3 and CostInfoV3; Zap resolves these plus CostAllocationAccountV3 when accounts exist. | core/data-loader/SKILL.md and scripts/data_loader_metadata.py registered-object, item, UCM and attribute retrieval through its governed client. | Exact top discriminator, BusinessObjectId, current UcmContentId, METADATA and attribute/key definitions. | Delegate metadata retrieval to core.data-loader. Use its targeted find_business_objects lookup for each exact discriminator and paginate; a capped unfiltered catalogue is not proof of absence. Resolve one BusinessObjectId, then its current item UcmContentId, not an arbitrary historical template row. Download via its byte reader with Accept */* and framework header 9. Parse METADATA and component/key metadata; require the chosen ordinary attributes and operations to be supported. Zap requires current DELETE capability and complete keys for EL allocation/accounts and EL/LIV CostInfo; field presence alone is insufficient. For End Date, apply the special-attribute boundary in ora_design_enforcement.md to both components; do not reject preparation solely because ReplaceLastEffectiveEndDate is absent from an ordinary list. | Current schemas, template provenance, validated key sets and operation support. | Missing/ambiguous registration, template, ordinary attribute or DELETE identity support blocks before archive acceptance. Do not ask the user to supply a template that the declared loader can retrieve. |

## History and Detail Requests

Pass each query value separately to the governed client. The double pipes below
are literal finder separators, encoded once by that client.

```text
History:
finder = findByWord;AdditionalViewCriteria=findByLegislativeDataGroupIdSourceIdSourceType,ParameterKeys=pSourceId||pSourceType||pLegislativeDataGroupId,ParameterValues=<element_link_id>||EL||<ldg_id>,PayRestName=PayCostSearchVO,DisplayAttributes=EffectiveStartDate||EffectiveEndDate||HistoryComments||LastUpdatedBy||LastUpdateDate,SortBy=EffectiveStartDate DESC
onlyData = true
limit = 500
offset = <offset>

Detail:
finder = findByLegislativeDataGroupIdSourceTypeSourceId;LegislativeDataGroupId=<ldg_id>,SourceId=<element_link_id>,SourceType=EL
effectiveDate = <YYYY-MM-DD>
expand = CostAllocationAccounts.CostPartialKff,CostInformation,InputValue
limit = 450
offset = <offset>

Full account:
finder = CF;VarCsr=oracle.apps.hcm.payrolls.costs.setup.restModel.view.CostAllocationAccountsVO#costKff,VarSin=<IdFlexNum>
q = (_ID_FLEX_NUM=<IdFlexNum> and <runtime_api_name>='<component_value>' and ...)
totalResults = true
limit = 25
offset = <offset>
```

| Situation | What Happens |
|---|---|
| Transport | Use core.fusion-api.rest-api-client and references/fusion-rest-api.md with REST-Framework-Version=9. Every business read uses the configured host and public resource path. Keep session proxy bypass and OAuth handling in the shared client workflow. |
| Read-only POST exception | Only the three named get*Lov actions above are authorized lookup POSTs, not costing writes. Use Content-Type=application/vnd.oracle.adf.action+json and structured JSON arguments for the two parameterized actions. Do not replace them with GET or impose a mutation approval on a lookup. The no-body type action needs no invented parameters. |
| Excluded calls | Never execute the captured batch, trace, futureRecordExists, findExistingRecord, validateCombination or genericCosting CRUD. The history/detail resolvers establish state; HDL through core.data-loader remains the only costing mutation route. |
| Collection completeness | Apply the Search pagination checks to every history, detail, combination and segment-LOV collection. Keep request context fixed across pages. A missing expansion is not an empty array. For an expanded child with hasMore=true, stop with incomplete evidence; these HARs do not establish child continuation paths. |
| Detail normalization | When comparing account values, CostAllocationAccounts.Proportion is a percentage in these responses: divide by 100 with decimal arithmetic, even for values less than or equal to 1. Input percentages and HDL fractions are separate representations; never infer their units from magnitude. Keep null, empty and zero distinct. Zap retains raw account values only as preservation/freshness evidence; it does not render or validate proportions, segments or sequences. |
| Child identities | EL CostInformation.SourceId must equal ElementLinkId; LIV InputValue.SourceId is the link-input ID, while its InputValueId is a different identity. Retain CostInfoId per EL/LIV record, parent CostAllocationId and CostAllocationRecordId, and each CostAllocAccountId. Require LDG and child date bounds to match the selected scope. For End Date retain each independent pre-load end; do not infer child dates from the allocation. |
| Runtime labels | Resolve exact title, segmentCode or API name first, then a unique case-insensitive match. Natural Account may match the single Account segment when no exact Natural Account segment exists; ambiguity requires selection. Map SEGMENTn to HDL Segmentn, never n from display order. |
| Partial accounts | COST/BAL use only supplied runtime-mapped Segment columns. Missing optional components remain absent; do not require a full combination or fill zeros. CostPartialKff values and Segment columns must agree when both are present. A required component follows its descriptor; optional components need no full-account validation. |
| Full accounts | OVRRIDE uses every component in full KFF sequence and its delimiter, validated by validate_element_costing_segments and resolve_element_priority_account. Full metadata uses FND_ACFF_SegSeqNo and FND_ACFF_Delimiter; follow schema references only within the configured public API. Require its fields/order to agree with the runtime descriptor; do not equate nullable partial fields with optional full components. |
| Safe query construction | Build full-account filters only from descriptor field names and validated string values. Reject control characters and unescaped quote/finder delimiters when the current client has no proven escaping contract. Never accept a raw q, finder or service URL from business input. |

## End Date Read Comparisons

| Situation | What Happens |
|---|---|
| Preparation baseline | After complete query_element_costing_history, call read_element_costing_record at each returned interval start and at the requested end when it is within the selected allocation interval. Bind every snapshot to its allocation/start key and require complete accounts and EL/LIV expansions. At the selected start and requested end, resolve one EL CostInformation record and the complete set of existing LIV CostInfo records, including disabled inputs. Match CostInfoId, SourceId and canonical LinkInputName across both dates; retain every independent date and option value. Missing/duplicate identities or changed record sets block. Retain all snapshots in approved local staging; apply the End Date operation contract before rendering. |
| Approval freshness | COE.END_DATE.RECHECK_STATE repeats those same history/detail reads for the already selected identity. Compare environment, allocation/history keys and dates, accounts, EL/LIV identities/options/dates and relevant concurrency/audit facts. Compare collections by identity, not response order; ignore only transport/link differences. Unchanged evidence preserves the existing archive and approval. Any material difference or incomplete read blocks submission and invalidates approval; do not update the approved baseline in place. |
| Verification | After terminal loader success and an explicit verification request, query_element_costing_history must retain the same allocation/start keys and all earlier intervals, with the latest allocation ending on the requested date. Call read_element_costing_record at each prior start, the requested end and the next calendar day. At the requested end require the parent, EL and every baseline LIV to have that exact end, unchanged physical identities/starts and all original accounts/options. Compare the full expected target set, including records already closed before loading; submitted-row success alone is insufficient. Earlier snapshots and unrelated records must remain unchanged. Require zero allocation parents the next day, but use explicit EL/LIV end dates at the requested end as evidence of their closure. Require complete reads and current history intervals when matching detail. Missing or changed evidence is unverified/partial, never success or permission to replay. |
| Comparison normalization | Match collections by stable identity and compare all business fields. For post-load preservation comparisons ignore only links, @context, SysEffectiveDate and audit/version fields CreatedBy,CreationDate,LastUpdatedBy,LastUpdateDate,LastUpdateLogin,ObjectVersionNumber. SysEffectiveDate is query context. Retain audit/version evidence for approval freshness; normalization must not hide a concurrent change. |
| Earlier artifact verification | A status/verification resume for a previously prepared allocation or cost_information_only archive retains its original expected scope and baseline. Compare its submitted changes and preserved records without widening that old artifact. Report its limited result; do not claim the new complete End Date contract passed unless all three component types were independently verified. This compatibility rule never permits preparing a new partial-scope request. |

## Zap History and Detail

Use the existing History and Detail Requests; no new REST mutation or item
route is introduced. Resolve all facts in the selected environment before
building physical DELETE targets.

| Situation | What Happens |
|---|---|
| History selector | Complete query_element_costing_history for the bound ElementLinkId/EL/LDG. The supplied EffectiveStartDate must equal exactly one history start; retain every interval of that row's CostAllocationId, including earlier, later and end-dated periods. Retain other allocations as preservation evidence. Do not infer the scope from Search CostingExists or a current-date detail alone. |
| Historical details | Call read_element_costing_record at every selected history start. Require matching CostAllocationId, CostAllocationRecordId, SourceId, SourceType EL, LDG and exact history dates, with complete CostAllocationAccounts, CostInformation and InputValue expansions. If other logical allocations exist for the same source, read every one of their history starts too, solely to check target exclusivity and preserve them. Never add their targets to the deletion set. |
| Accounts | Bind each CostAllocAccountId to its enclosing CostAllocationRecordId, returned SourceSubType and canonical source keys. Use returned EffectiveDate when present, otherwise the bound parent's EffectiveStartDate, following the department/payroll DELETE contract; a returned date outside the parent interval blocks. Deduplicate by physical account ID only when every bound identity value agrees. All returned subtypes are targets; do not select only COST or apply Create proportion rules. An account member may be omitted only when every selected interval explicitly has zero accounts. |
| EL and LIV | Require one EL CostInformation row per selected interval, with SourceId=ElementLinkId and matching LDG/dates. Retain every existing InputValue CostInfo row, including CostedFlag=false; its SourceId is the link-input identity and its canonical input name maps to LinkInputName. Require each row's CostInfoId, matching LIV/LDG and parent-aligned dates. A complete empty InputValue expansion proves no LIV for that interval; a missing expansion or missing CostInfo identity does not. Do not substitute InputValueId, CostAllocationId or an EL CostInfoId for a LIV identity. |
| CostInfo coverage | Preserve every observed EL/LIV slice, then group by CostInfoId with invariant source type, source ID, LDG and canonical user keys. Use that ID's own earliest observed start/latest end for its DELETE, not another object's dates. Conflicting identities, overlapping slices, independently dated/uncovered CostInfo or an ID shared with unselected history blocks the complete operation. Search's single CostInfoId is not a substitute for this historical EL/LIV target set. |
| Bound evidence | Bind complete source/history/detail evidence, target IDs, dates and row counts to the immutable artifact. Preserve disjoint history periods without inventing intermediate slices. Keep customer data and internal IDs only in approved ignored staging; durable run diagnostics contain sanitized facts and artifact references. |
| Freshness | Before presenting the destructive approval, COE.ZAP.REFRESH repeats the source Search at the saved selector date, complete history and every baseline detail read. Require unchanged environment, eligibility identity, history, physical targets, values and relevant version/update facts. Compare collections by identity, ignoring only transport/link differences. Changes invalidate the prepared preview; do not silently refresh its baseline. Later contextual approval restores this completed check and uses the loader's exact-artifact/context verification, without repeating discovery or rebuilding bytes. |

## Zap Verification

| Situation | What Happens |
|---|---|
| Loader prerequisite | On explicit verification of the accepted run, require terminal successful DELETE results for the allocation, every EL/LIV CostInfo target and every included account. Match all component/row results to the immutable archive; success of the parent alone is partial failure. |
| Saved history and details | Repeat query_element_costing_history with the saved source/LDG. The targeted CostAllocationId must be absent on every page, with unrelated history unchanged. Repeat read_element_costing_record at every saved selected start: require zero selected parents and no targeted account/CostInfo IDs. Re-read unrelated baseline intervals and compare complete snapshots, using the business-field normalization in End Date Read Comparisons. Failed or incomplete reads never prove absence. Do not require the deleted costing to resolve again. |
| Eligibility preserved | Repeat search_element_costing with the saved canonical eligibility/element/LDG and each selected historical start. Require the same ElementLinkId and element/LDG identity to remain. Search CostInfoId must not equal a deleted EL target; require CostingExists=N wherever no unrelated allocation remains. Preserve unrelated costing instead of forcing N when it legitimately remains. Search is corroborating source evidence, not a replacement for the saved deletion scope. |
| Independent CostInfo boundary | Deleting the parent can hide nested CostInformation and InputValue. The declared REST contracts do not independently query orphan EL/LIV CostInfo. Report confirmation as explicit successful EL/LIV DELETE results plus saved-scope read-back; never claim empty genericCosting alone proves their deletion. Missing per-target loader evidence blocks verified completion. |
| Failure or partial load | Retain successful and failed components separately and stop without resubmission. The payment-source-specific recovery is not an element recovery contract; do not invent an orphan lookup or reconstruct lost targets from chat. |

## HDL Mapping and Template Resolution

These are transformation contracts, not a replay of the REST write. Validate
their attributes against the current templates before rendering. Oracle's
[element eligibility example](https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-element-eligibility-costing.html)
documents EL/LIV costing information and the three separate business objects.

| Source fact | HDL destination | Transformation |
|---|---|---|
| Selected canonical identity | All three objects: ElementEligibilityName,ElementCode,LegislativeDataGroupName | Reuse Search mapping. Use canonical user keys for new records; do not emit generic SourceId. |
| CostInformation | CostInfoV3, SourceType EL | CostableType from type LOV; TransferToGlFlag from explicit boolean; DistributionSetName from group LOV when applicable. LinkInputName and CostedFlag do not represent the EL costing type. |
| InputValue | CostInfoV3, SourceType LIV | One row per selected input; LinkInputName from input LOV; CostedFlag is Y or N. Never put its raw InputValueId in LinkInputValueId. |
| End Date parent | CostAllocationV3, SourceType EL | Preserve selected EffectiveStartDate; set EffectiveEndDate to the explicitly requested inclusive end. Add ReplaceLastEffectiveEndDate from defaults. Retain canonical eligibility/element/LDG keys; do not use ORG, DepartmentName or raw SourceId. Assemble with the EL/LIV changes under the End Date source contract; no account rows. |
| End Date EL/LIV | CostInfoV3, SourceType EL and LIV | Reuse canonical identity and each existing LIV's canonical LinkInputName from complete detail. Keep each independent start and observed EL type/TransferToGlFlag/DistributionSetName or LIV CostedFlag; set only the end to the same requested date and the special attribute from defaults. No LOV re-selection, input creation or change to other options. |
| Allocation parent | CostAllocationV3, SourceType EL | EffectiveStartDate and operation-specific end; same canonical identity. |
| Cost Account / Offset Account | CostAllocationAccountV3, SourceType EL, SourceSubType COST / BAL | IdFlexNum and validated Segment1 through Segment30 as applicable; EffectiveDate is the operation start. Proportion and sequence come from ora_defaulting_rules.md. |
| Priority Cost Account | CostAllocationAccountV3, SourceType EL, SourceSubType OVRRIDE | REST Account maps to ConcatenatedSegment, not Account and not CostAllocationKeyflexId. Leave all Segment columns empty for this row. |
| Existing correction identity | CostInfoV3.CostInfoId | Use only the selected EL/LIV record's physical ID with its unchanged start/end and changed attributes; never reuse an EL ID for a LIV row. |
| Zap parent | CostAllocationV3, SourceType EL | Canonical eligibility/element/LDG user keys; earliest start and latest actual end of the selected logical allocation's complete history. Confirm the date/user-key identity cannot address an unselected allocation. |
| Zap accounts | CostAllocationAccountV3 | Bound CostAllocAccountId, CostAllocationRecordId, EffectiveDate and SourceSubType from Zap historical details, with EL and the parent's canonical user keys. Emit identity only; no account-value defaults. |
| Zap EL/LIV CostInfo | CostInfoV3 | One target per resolved CostInfoId with its own full observed date range and SourceType. Supplement the physical ID with the existing canonical ElementEligibilityName,ElementCode,LegislativeDataGroupName identity and LinkInputName for LIV; EL leaves LinkInputName empty. Validate that exact source-specific DELETE key form through core.data-loader. Do not copy PM PaymentMethodId, invent SourceId or try alternative live keys if validation fails. |

resolve_element_hdl_templates delegates live metadata retrieval to the named
core service. Its requests and credentials remain owned by core.data-loader.
Use its normal schema retrieval and validation; do not create another loader.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COE.SEARCH.RESOLVE_LDG | decision | 6 | reference_lookup | resolved->COE.SEARCH.ENFORCE_ROUTE;no_match->COE.SEARCH.LDG_NOT_FOUND;ambiguous->COE.SEARCH.NEEDS_LDG_SELECTION;failed->COE.HDL.HANDLE_ERROR | COE.SEARCH.CHECK_DEPENDENCIES | stop | Invoke resolve_element_costing_ldg only for the LDG-text branch; resolved requires complete candidate evidence and one selected identity. |
| COE.SEARCH.FETCH | decision | 8 | reference_lookup | found->COE.SEARCH.RETURN_TO_OPERATION;empty->COE.SEARCH.RETURN_TO_OPERATION;partial->COE.SEARCH.PARTIAL;failed->COE.HDL.HANDLE_ERROR | COE.SEARCH.ENFORCE_ROUTE | stop | Invoke search_element_costing for the original operation and normalize every page. found and empty require complete=true; an intentional pagination stop uses partial, while a response or request failure uses failed. |
| COE.SEARCH.RETURN_TO_OPERATION | decision | 9 | evaluate_result | search->COE.SEARCH.DONE;operation->COE.IDENTITY.SELECT;invalid->COE.HDL.HANDLE_ERROR | COE.SEARCH.FETCH | stop | A complete result returns to the saved requested_operation: Search ends with its list; Create, Update, Correct, End Date and Zap require identity selection. Never replace the operation with Search. |
| COE.IDENTITY.SELECT | decision | 10 | evaluate_result | resolved->COE.IDENTITY.CHECK_OPERATION;no_match->COE.IDENTITY.NOT_FOUND;ambiguous->COE.IDENTITY.NEEDS_SELECTION;invalid->COE.HDL.HANDLE_ERROR | COE.SEARCH.RETURN_TO_OPERATION | stop | Apply Operation identity selection, selection resume and HDL identity mapping to the complete search_element_costing evidence without another GET. |
| COE.HDL.RESOLVE_CONTEXT | decision | 16 | reference_lookup | resolved->COE.HDL.CHECK_SCOPE;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.VALIDATE_INPUT | stop | Run query_element_costing_history then read_element_costing_record at the requested date for Create or selected interval for Update/Correct. Resolve structure for Create/Update/Correct only. End Date applies Preparation baseline under End Date Read Comparisons to the allocation, EL and all existing LIV records, retaining every interval snapshot without KFF/LOV validation. |
| COE.HDL.RESOLVE_VALUES | decision | 18 | reference_lookup | resolved->COE.HDL.VALIDATE_VALUES;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.CHECK_SCOPE | stop | End Date has no value changes: retain baseline evidence and skip type/group/input, KFF, segment and priority-account resolvers. For other operations resolve requested type, group and inputs with the three named LOV actions. For Create/Update accounts run resolve_element_costing_kff and validate_element_costing_segments, plus resolve_element_priority_account for OVRRIDE. Reuse unchanged EL/LIV values from the complete baseline; Correct flags/type-only skips account resolvers. |
| COE.ZAP.HISTORY | decision | 21 | reference_lookup | resolved->COE.ZAP.DETAILS;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.VALIDATE_INPUT | stop | Invoke query_element_costing_history under Zap History and Detail; bind the selector to one logical allocation and retain its entire history plus unrelated baseline intervals. Empty or unmatched history blocks preparation without claiming orphan absence. |
| COE.HDL.RESOLVE_TEMPLATES | decision | 23 | reference_lookup | resolved->COE.HDL.RENDER;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.CHECK_DEPENDENCIES | stop | Invoke resolve_element_hdl_templates for the exact mapped objects; no upload or approval pause at this step. |
| COE.END_DATE.READ_RESULT | decision | 26 | reference_lookup | resolved->COE.END_DATE.RESULT;failed->COE.HDL.HANDLE_ERROR | COE.END_DATE.VALIDATE_RESUME | stop | Invoke read_element_costing_load_result once for the explicit status/verification request, including the shared loader error checks. Do not upload or poll automatically. |
| COE.END_DATE.VERIFY | decision | 28 | reference_lookup | verified->COE.END_DATE.DONE;failed->COE.HDL.HANDLE_ERROR | COE.END_DATE.RESULT | stop | Apply End Date Read Comparisons verification through query_element_costing_history and read_element_costing_record. Enter only after verify_succeeded; any missing evidence or mismatch fails rather than replaying the load. |
| COE.ZAP.DETAILS | decision | 29 | reference_lookup | resolved->COE.ZAP.CHECK_SCOPE;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.HISTORY | stop | Apply Zap History and Detail through read_element_costing_record for every selected and exclusivity-check interval. Resolve physical accounts and EL/LIV targets; require complete evidence before scope enforcement. |
| COE.ZAP.RESOLVE_TEMPLATES | decision | 33 | reference_lookup | resolved->COE.ZAP.RENDER;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.CHECK_DEPENDENCIES | stop | Invoke resolve_element_hdl_templates for all included DELETE objects and source-specific key forms; no KFF or value LOV requests. |
| COE.ZAP.REFRESH | decision | 37 | reference_lookup | unchanged->COE.ZAP.GATE;changed->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.ENFORCE | stop | Apply Zap History and Detail freshness through the existing source/history/detail resolvers before the single approval preview. A changed baseline invalidates the prepared artifact; this node never submits or rebuilds it. |
| COE.END_DATE.RECHECK_STATE | decision | 57 | reference_lookup | unchanged->COE.END_DATE.SUBMIT;changed->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.GATE_END_DATE | stop | Apply End Date Read Comparisons approval freshness using the bound identity. Preserve exact approved bytes and baseline. Changed or incomplete state invalidates approval; this check never rerenders or reselects identity. |
| COE.ZAP.READ_RESULT | decision | 61 | reference_lookup | resolved->COE.ZAP.RESULT;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.VALIDATE_RESUME | stop | Invoke read_element_costing_load_result for the saved accepted Zap, retaining component/row outcomes and complete error checks. No upload or automatic polling. |
| COE.ZAP.VERIFY | decision | 63 | reference_lookup | verified->COE.ZAP.DONE;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.RESULT | stop | Apply Zap Verification only after verify_succeeded, using the saved source, complete history, physical targets and loader results. Missing evidence or surviving targets fail without replay. |
