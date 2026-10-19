# Configure Legislations for Human Resources Lookups

This file owns the installedLegislations Search request, filter translation,
pagination, matching, Create eligibility and rule options, Delete target resolution,
and explicit post-load verification. Only allow-listed business fields are retained.

The request contracts below are self-contained. Runtime values come from the
selected Fusion environment; example rows never establish available options.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_installed_legislations | Search gates passed, or a Delete/Verify Delete/unavailable-Create resolver delegates its collection traversal after its own scope gate | Validated search filters and the selected environment's configured restBaseUrl | GET /hcmRestApi/resources/latest/installedLegislations | Read TerritoryShortName, TerritoryCode, Meaning, ImplementedFlag and collection items, count, hasMore, limit, offset, totalResults; request the captured unprojected representation | Apply Installed Query Construction and Installed Lookup Execution Rules; all supplied filter groups constrain the server query; complete all pages of that filtered result | Search status, complete flag, business-facing rows, retrieved count, applied filters, and sanitized failure evidence when applicable | Zero complete consistent matches is NO_MATCHES; one is MATCHES; several is MULTIPLE_MATCHES and all candidates are returned; never select one automatically |
| resolve_installed_legislation_for_delete | Delete scope gate passed; during preparation or Task Hook validation | Validated legislation_name and/or legislation_code and the selected environment's configured restBaseUrl | GET /hcmRestApi/resources/latest/installedLegislations, using the Installed Request Contract and Installed Query Construction; send the code-only filter when a code is supplied, otherwise the name-only filter | Same collection and row fields as find_installed_legislations | Delegate complete traversal of the filtered result to find_installed_legislations, then apply the Delete identity rules in Installed Lookup Execution Rules; do not run the CLHR.SEARCH node or terminate at the Search terminal | matched: TerritoryCode to legCode, TerritoryShortName to resolved_legislation_name, complete lookup evidence, selected environment and original identifiers; no guessed or normalized replacement code | no_matches or selection_required stops preparation and presents candidates when present; conflict blocks mismatched name/code; error preserves incomplete/failed evidence |
| verify_installed_legislation_deleted | Verify Delete scope gate passed after successful load and original context checks | Exact original legislation_code and the same configured environment and read-access context used for selection | GET /hcmRestApi/resources/latest/installedLegislations, reusing the Installed Request Contract and code-only Installed Query Construction | Same collection and row fields as find_installed_legislations | Traverse all pages of the code-filtered result with find_installed_legislations and compare returned TerritoryCode values to the original code using the exact identifier comparison in Installed Lookup Execution Rules | absent only when complete and consistent with zero exact-code matches; present when an exact-code match exists; error for failed or inconclusive evidence | Other substring matches do not establish presence; failures, incomplete pages, changed context, or a rejected filter never establish absence |
| resolve_available_legislation_for_create | First Create lookup, before every rule-specific call | Optional legislation_name and/or legislation_code | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector available_legislations in Payroll LOV Requests | TerritoryShortName, TerritoryCode, CurrencyCode via named result pairs; collection pagination | Complete the available collection; exact trimmed casefold name/code; both supplied identifiers must match one row; no first/partial match selection | selected: shared resolved_legislation_name and legCode plus environment and complete evidence; choice_required: names/codes; unavailable: supplied target absent from complete list | No supplied target or partial/ambiguous candidates: list available names/codes and ask for one; exact name/code conflict is error; no exact match with no partial candidates delegates classify_unavailable_legislation |
| classify_unavailable_legislation | Only after complete available-legislation lookup returns unavailable | Original supplied name/code in same environment | GET /hcmRestApi/resources/latest/installedLegislations; reuse installed request contract and code-only filter when code supplied, otherwise name-only filter | Same fields as find_installed_legislations | Validate the original identifier under installed-filter input rules before calling; delegate complete filtered traversal to find_installed_legislations; exact match and name/code consistency as for Delete, without invoking Delete nodes | existing: ALREADY_EXISTS, display matched name/code and suggest a separately requested Edit; absent: LEGISLATION_UNAVAILABLE | Partial/ambiguous identity: error with TARGET_SELECTION_REQUIRED and candidates; conflicting identity: error with TARGET_CONFLICT; failed/incomplete lookup is inconclusive; absence means invalid or unavailable for Create, never proof of a global invalid country |
| resolve_payroll_relationship_rule | Shared Create selection established | Optional payroll_relationship_rule Meaning | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector payroll_relationship_rule | Meaning and LookupCode via named result pairs | Complete choices; exact trimmed casefold Meaning; retain choices and missing/invalid status for input validation; locate the default candidate by Meaning Create New Record only when the value is omitted and no rule-choice request is pending | Resolved/default candidate LookupCode to legRuleMap.I; validate omission default candidate code equals I; current Meaning choices | When the omission default is needed, a missing/duplicate candidate or code discrepancy is contract error; invalid explicit label records invalid with current choices; never replace an invalid value with default |
| resolve_deduction_card_tru_rule | Shared Create selection established | Optional deduction_card_tru_rule Meaning | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector deduction_card_tru_rule | Meaning and LookupCode via named result pairs | Complete choices; exact trimmed casefold Meaning; retain missing/invalid status for input validation | Same selected LookupCode to both legRuleMap.CALC_BREAK and legRuleMap.GET_TU; current Meaning choices | Missing input records required choice; unknown or ambiguous input records invalid and current choices; never choose an option automatically |
| resolve_default_currency | Shared Create selection established, requested_options empty and no explicit currency override | Exact shared legCode | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector default_currency | CurrencyCode and Name via named result pairs; top-level Meaning is the default currency display name | Require exactly one row after complete pagination and a nonempty code/name; if top-level Meaning and Name disagree, fail contract validation | Default candidate currencyCode from CurrencyCode; display currency name from Meaning | Zero/multiple rows or contradictory labels block; do not infer currency from available-legislation CurrencyCode or country memory |
| resolve_currency_override | Shared Create selection established and explicit currency override or request for options | Supplied currency name and/or code | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector currency_choices | CurrencyCode and Name via named result pairs; ignore top-level Meaning | Complete LOV; for options-only return choices with no invalid-value finding; otherwise exact trimmed casefold name/code and both identifiers must select the same unique row | Explicit currencyCode and display Name; current selectable name/code pairs | No exact/ambiguous/conflicting match records invalid with choices; do not fall back to default currency |
| resolve_default_relationship_mappings | Shared Create selection established, requested_options empty; defaults needed for omitted input or edits to default rows | Shared Create selection as context; no unsupported legCode bind | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector default_relationship_mappings | RelationshipTypeName, RelationshipTypeId, ProcessInRun, Meaning and RelTypeMapId via named result pairs | Preserve complete response order; display Meaning as System Person Type, RelationshipTypeName as Payroll Relationship Type, and ProcessInRun as read-only; resolve Meaning through resolve_default_system_person_code | Ordered default row candidates; RelationshipTypeId stays paired with its Meaning; ignore RelTypeMapId for prepared arrays | Missing keys, conflicting IDs/labels or unresolvable system type block; empty default collection yields empty candidates without invented rows |
| resolve_system_person_type_options | Shared Create selection established; explicit additions/replacements/changed System Person Type or request for options | Shared legCode and proposed System Person Type Meaning/code | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector system_person_types | LookupCode and Meaning via named result pairs | Complete LOV; options-only returns choices without requiring a supplied value; otherwise exact trimmed casefold Meaning/code and resolve each changed/new row uniquely; retain live returned code even if absent from embedded default crosswalk | System Person Type display Meaning and sysPersonType code for that row; current choices | Unknown/ambiguous value records invalid and displays live options; embedded default crosswalk is not an allowlist for additions |
| resolve_payroll_relationship_type_options | Shared Create selection established; explicit additions/replacements/changed Payroll Relationship Type or request for options | Shared legCode and proposed Payroll Relationship Type label | GET /hcmRestApi/resources/latest/payrollGenericLOV; selector payroll_relationship_types | RelationshipTypeName, RelationshipTypeId, ProcessInRun via named result pairs | Complete LOV; options-only returns choices without requiring a supplied value; otherwise exact trimmed casefold RelationshipTypeName and resolve the same row's ID and ProcessInRun together | relTypeIds candidate and read-only Process in Payroll for each edited row; display current labels and Yes/No | Unknown/ambiguous value records invalid with live choices; no ID inferred from label or another environment |

## Payroll LOV Requests

All selectors use the configured restBaseUrl with GET
/hcmRestApi/resources/latest/payrollGenericLOV through the governed client.
Use REST-Framework-Version=9, Accept-Language=en and onlyData=true. The first
page uses limit=25 and offset=0. Do not send fields, q, orderBy or extra binds:
this contract establishes only finder and pagination for these selectors.
The installedLegislations q contract below is separate.

Build one finder parameter as data, never a URL or shell expression. Begin
with findByWord;PayRestName=oracle.apps.hcm.legconfig.setup.restModel.view.
followed immediately by the VO name below. Append nonempty components in this
order: AdditionalViewCriteria, ParameterKeys, ParameterValues, DisplayAttributes,
each as a comma followed by name=value. In list-valued components join the
listed entries, in order, with two literal vertical bars (||). A dash means
omit that component entirely. URL-encode once using the governed client.

| Selector | VO name | AdditionalViewCriteria | ParameterKeys, ordered | ParameterValues, ordered | DisplayAttributes, ordered |
|---|---|---|---|---|---|
| available_legislations | AvailableLegislationsVO | - | - | - | TerritoryShortName, TerritoryCode, CurrencyCode |
| payroll_relationship_rule | HrLookupsVO | findByLookupType | pLookupType | PAY_TMPLT_LEG_RULE_REHIRE | Meaning, LookupCode |
| deduction_card_tru_rule | HrLookupsVO | findByLookupType | pLookupType | ORA_PAY_DED_CARD_TRU_OPTIONS | Meaning, LookupCode |
| default_currency | DefaultCurrencyVO | - | pLegCode | selected legCode | CurrencyCode, Name |
| currency_choices | CurrenciesVO | - | - | - | CurrencyCode, Name |
| default_relationship_mappings | PayRelTypeMapCreateVO | - | - | - | RelationshipTypeName, RelationshipTypeId, ProcessInRun, RelTypeMapId, Meaning |
| payroll_relationship_types | PayrollRelationshipTypeCreateVO | findByLegCodeOrNull | pLegCode | selected legCode | RelationshipTypeName, RelationshipTypeId, ProcessInRun |
| system_person_types | SysPerTypeVO | - | pLegCode, pLookupType | selected legCode, SYSTEM_PERSON_TYPE | LookupCode, Meaning |

## Generic LOV Execution Rules

| Situation | What Happens |
|---|---|
| Selection prerequisite | Available legislations is the only Create lookup permitted before shared legCode resolution; installed classification is allowed only on unavailable outcome; all rule LOVs wait for successful selection, including selectors without a legCode bind |
| Proxy and authentication | Apply the same governed client, environment, session-only proxy preflight and secret redaction as the installed lookup on every call, including every page; never reuse captured credentials |
| Binding selected legCode | Use only the exact returned scalar code, reject finder delimiters/control characters in a bind value, and never add ParameterKeys to selectors that declare none |
| Decoding a generic row | Find the unique ResultKeyN equal to each required semantic key, then read ResultValueN with the same N, for N=1..40; never assume a fixed numbered slot; duplicate/missing required semantic keys fail |
| Display labels | Use named TerritoryShortName, Name, Meaning or RelationshipTypeName as specified by each resolver; top-level Meaning is usable only where explicitly declared; it is not a generic display field |
| Response shape | Require object/items array, count equal to page row count, boolean hasMore, positive integer limit and nonnegative integer offset; nonempty code/label fields must be strings; preserve ID values losslessly, rejecting missing, boolean or fractional IDs |
| Pagination | Complete every needed collection; keep selector and binds fixed and advance offset=response.offset+response.limit until hasMore=false; fail on empty continuing page, repeated offsets/identities or contradictory duplicate keys; a partial collection cannot validate absence or an option list |
| Matching | Trim outer whitespace and casefold labels/codes; do not translate, remove accents, repair encoding artifacts, guess codes or accept a partial match automatically; multiple exact candidates require disambiguation |
| Available choices | Present available legislation names/codes on Create entry; when one exact target was supplied, state it is available and proceed without asking again; when target is absent or uncertain, list available choices and stop before dependent LOVs |
| Invalid explicit option | Retain its invalid status and the complete relevant live choices for the input-validation node; never replace it with a default |
| Generic row identity | Use TerritoryCode for available legislation, LookupCode for rule/person LOVs, CurrencyCode for currencies, RelationshipTypeId for relationship choices, and the tuple (Meaning, RelationshipTypeId) for default mappings; repeated relationship IDs in different default rows are valid |
| Options-only requests | When requested_options is nonempty, run only those requested LOV resolvers after eligibility; skip unrelated rule/default/currency/mapping calls, returning resolved from their graph nodes without making a request; return the requested complete labels/codes and Process in Payroll where applicable; do not classify missing proposed values as invalid and do not select omission defaults for a pending explicit choice; CLHR.CREATE_OPTION_REQUEST returns those options before defaulting |
| Default mapping row | Use Meaning for System Person Type and RelationshipTypeName for Payroll Relationship Type; RelationshipTypeId belongs to the latter; resolve the former through the embedded default crosswalk; preserve the row pairing |
| Customized rows | Start from default rows unless user explicitly replaces all; retrieve only needed live person/relationship option collections; for every added row require both columns, and derive ProcessInRun from the chosen relationship row; retain unchanged valid values in partially edited rows |
| Process in Payroll | Map ProcessInRun Y to Yes and N to No for display; retain raw value as read-only evidence; unknown flag is contract error; this field is not a write parameter |
| Selection changes | Discard dependent lookup results, defaults, row mappings and prepared output whenever legCode or environment changes; restart with available-legislation resolution |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_default_system_person_code | A default mapping row supplies System Person Type Meaning | Embedded Default System Person Crosswalk in this file, explicitly supplied as the authority for default rows | Exact trimmed casefold Meaning; collapse repeated aliases only when all matched codes agree | That row's sysPersonType code; preserve its paired RelationshipTypeId | Missing or conflicting code blocks the row; never search an external attachment; explicit added/changed person types use live options instead |

## Installed Request Contract

| Component | Value | Source or Handling |
|---|---|---|
| Client | core.fusion-api.rest-api-client; scripts/fusion_rest_client.py | Read its SKILL.md and references/fusion-rest-api.md; no custom HTTP client |
| Endpoint | /hcmRestApi/resources/latest/installedLegislations | Fixed skill-owned relative path for Search, Delete resolution, Verify Delete and unavailable-Create classification; no caller-supplied path or resource version is required |
| Host | Configured restBaseUrl | Never reuse a captured environment host or send credentials to a different host |
| Resource route | /hcmRestApi/resources/latest/ | Required prefix for every task-owned HCM REST resource call; never select a browser-routed path or use one as fallback |
| Method | GET | No request body |
| REST-Framework-Version | 9 | Captured header; do not fall back to framework version 1 query syntax |
| Accept-Language | en | Keeps Meaning values consistent with the captured Yes/No contract |
| onlyData | true | Captured parameter |
| totalResults | true | Informational server count; not the pagination termination condition |
| orderBy | TerritoryShortName:asc | Pass decoded text; the client performs URL encoding |
| limit and initial offset | From ora_defaulting_rules.md | Exactly one value of each; do not copy duplicate limit parameters from copied requests |
| q | The single expression produced by Installed Query Construction, or absent | Pass as one raw --query argument; never pre-encode it or concatenate raw text into a URL |
| fields, finder, expand | Not sent | No extra lookup, projection, or finder is required by the observed Search contract |

## Installed Query Construction

Use the validated, trimmed input strings. For each string literal, replace every
apostrophe with two apostrophes before placing it inside single quotes. Keep
all field names and operators fixed; user text never becomes query grammar.
The client URL-encodes query parameters exactly once. Do not use semicolons to
join predicates in framework version 9.

| Supplied Filter | Predicate Template | Meaning |
|---|---|---|
| Legislation or Legislation Code | (UPPER(TerritoryShortName) LIKE UPPER('%{escaped_text}%') OR UPPER(TerritoryCode) LIKE UPPER('%{escaped_text}%')) | Case-insensitive contains match against either attribute; one grouped predicate |
| Legislation / TerritoryShortName | UPPER(TerritoryShortName) LIKE UPPER('%{escaped_name}%') | Explicit name-only contains search |
| Legislation Code / TerritoryCode | UPPER(TerritoryCode) LIKE UPPER('%{escaped_code}%') | Explicit code-only contains search |
| Predefined | Meaning='{predefined}' | Use the validated Yes or No literal; never query a field named Predefined |
| Implemented | ImplementedFlag='{implemented_literal}' | Yes maps to the string true; No maps to the string false; do not substitute InstalledFlag |
| More than one filter | Join present predicates with AND in the table order | The text OR remains parenthesized; no supplied constraint may be dropped |
| No filters | Omit q entirely | Blind Search, not q='', q=null, or an empty condition |

## Installed Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Starting the resolver | Use the declared governed client and Installed Request Contract only after readiness and the selected operation's pre-lookup scope gate succeed; the later Delete design check consumes the completed lookup; do not replay captured authentication or session state |
| Passing search text to the client | Build argument values as data; never evaluate a filter as shell, PowerShell, or Python code |
| Starting any primary or diagnostic traversal | Start at offset 0 with a fresh page/identity accumulator; do not mix pages or duplicate-detection state from different predicates |
| Preparing each request, including another page | Re-extract the hostname from restBaseUrl, add it to NO_PROXY and no_proxy for the current PowerShell session, and verify with Python that proxy_bypass=True and https_proxy_selected=False; otherwise return error before the call; do not modify configuration or profiles |
| A text criterion is present | Send its q predicate to Fusion; do not fetch an unfiltered collection and implement the search by discarding rows in the client; Delete identity checks operate on this filtered result only |
| A page is returned | Require HTTP success and the collection shape declared by the input/output contract; retain only the search result fields; do not persist raw responses, links, audit-user fields, or session material |
| Checking filtered rows | Check that every returned row satisfies every requested predicate; this is response verification, not replacement filtering; any violating row makes the result inconclusive instead of silently removing it |
| hasMore is true | Continue only the current query's result pages; keep the identical endpoint, q, headers, and orderBy; request next offset=response.offset+response.limit using the server's returned page size; do not broaden the query or fetch the unfiltered collection |
| hasMore is false | Finish after validating the last page; do not request another page merely to match an estimated totalResults |
| Pagination fails to advance | A repeated offset, repeated page identities, conflicting duplicate row, or an empty page with hasMore=true is an error; retain partial rows as incomplete and stop |
| A later page fails or the caller cancels or times out | Return error with complete=false and the last offset; partial rows do not establish absence or a complete result set |
| Primary query returns zero with two or more predicate groups | Run one diagnostic server query per predicate group through this same resolver, with the same environment and complete pagination; intersect the returned TerritoryCode sets in memory only to verify the zero result; do not treat the intersection as successful search output |
| Diagnostic intersection is nonempty, or a diagnostic query fails | Return error with SEARCH_INCONCLUSIVE; do not state that no matches exist or weaken the original query; this detects contradictory current-run filter results |
| Diagnostic intersection is empty and every diagnostic result is complete and consistent | Accept the primary zero as NO_MATCHES for the supplied criteria and the current user's visibility; these diagnostic calls do not replace the primary search |
| One predicate group or Blind Search returns zero | Accept NO_MATCHES only after successful complete pagination and no contradictory current-run evidence; a 404 or failed call is never an empty collection |
| Multiple rows match | Search returns every candidate with its business name and code; Delete and Verify Delete apply their additional exact-identity contract only after this complete filtered traversal |
| The service rejects q, UPPER, LIKE, a field, or the declared resource endpoint | Return error; do not fall back to an unfiltered call, a browser-routed or differently versioned endpoint, FSM, or a browser |
| Delete or Verify Delete: comparing an identifier | Compare strings after outer whitespace trimming and Unicode casefold; do not translate, remove accents, expand abbreviations, or infer an ISO code; preserve the exact returned code for the DAT |
| Delete: name only | Require exactly one returned row whose TerritoryShortName equals the supplied name under that comparison; a unique contains-only candidate still requires selection |
| Delete: code only | Require exactly one returned row whose TerritoryCode equals the supplied code under that comparison |
| Delete: both name and code | Query by code, then require the one exact-code row's TerritoryShortName to match the supplied name too; a disagreement is conflict, not permission to ignore either value |
| Delete: exactly one qualifying row | Return matched with its original TerritoryCode, TerritoryShortName, environment, original identifiers, and complete lookup evidence |
| Delete: no exact match and no candidates | Return no_matches with TARGET_NOT_FOUND; no DAT or upload is prepared, and no claim of a previously completed deletion is made |
| Delete: partial candidates or multiple exact matches | Return selection_required with each candidate's business name and code; ask for one exact displayed identity and restart resolution; never take the first row |
| Delete: phase is validate_artifact | Resolve the supplied selection again before approval and compare it with the exact code already present in the final archive; a conflict fails validation and does not modify the file |
| Verification after a successful load | Select by original code, not a new name; zero exact-code rows after complete retrieval is absent in the confirmed environment/access context; an exact row is present |
| Delete or Verify Delete: any lookup or response-integrity failure | Return error and complete=false; do not classify it as no_matches or absent |

Diagnostic queries are a bounded, declared part of this read-only resolver,
not a retry of a failed HTTP request. They run only for a completed, empty
multi-filter primary search. At most one diagnostic collection traversal is
performed for each supplied predicate group.

Delete and Verify Delete reuse the server-side contains query with one code-only
filter when code is supplied, otherwise a name-only filter. Their exact-identity
checks apply only to that complete filtered result and do not change Search.
Initialize offset and page size from the common defaults. Predefined and
Implemented retain their Search meaning; Fusion enforces the custom action's
business constraints during the approved load.

## Response Mapping

| Response Field | User-facing Field | Mapping |
|---|---|---|
| TerritoryShortName | Legislation | Preserve the returned display name |
| TerritoryCode | Legislation Code | Preserve the returned code; use it to distinguish candidates |
| Meaning | Predefined | Preserve Yes or No |
| ImplementedFlag | Implemented | String true becomes Yes; string false becomes No |
| Fully retrieved row count | Results | Count the verified rows, not the first page or estimated totalResults |
| No verified matches | Search message | No matches for the supplied filters in this environment with the current user's access; do not assert global nonexistence or permission to create |

## Search Contract Examples

These are query-construction cases, not assertions about current Fusion data.
The values are public territory names or synthetic strings. Expected q is
decoded; the governed client is responsible for encoding it for transport.

| Case | Search Text | Name | Code | Predefined | Implemented | Expected q |
|---|---|---|---|---|---|---|
| Blind | | | | | | OMIT |
| Shared text | Albania | | | | | (UPPER(TerritoryShortName) LIKE UPPER('%Albania%') OR UPPER(TerritoryCode) LIKE UPPER('%Albania%')) |
| Name only | | Albania | | | | UPPER(TerritoryShortName) LIKE UPPER('%Albania%') |
| Code only | | | AL | | | UPPER(TerritoryCode) LIKE UPPER('%AL%') |
| Predefined Yes | | | | Yes | | Meaning='Yes' |
| Predefined No | | | | No | | Meaning='No' |
| Implemented Yes | | | | | Yes | ImplementedFlag='true' |
| Implemented No | | | | | No | ImplementedFlag='false' |
| Both Yes | | | | Yes | Yes | Meaning='Yes' AND ImplementedFlag='true' |
| Yes and No | | | | Yes | No | Meaning='Yes' AND ImplementedFlag='false' |
| No and Yes | | | | No | Yes | Meaning='No' AND ImplementedFlag='true' |
| Both No | | | | No | No | Meaning='No' AND ImplementedFlag='false' |
| Full search | Albania | | | No | Yes | (UPPER(TerritoryShortName) LIKE UPPER('%Albania%') OR UPPER(TerritoryCode) LIKE UPPER('%Albania%')) AND Meaning='No' AND ImplementedFlag='true' |
| Explicit name and code | | Albania | AL | | | UPPER(TerritoryShortName) LIKE UPPER('%Albania%') AND UPPER(TerritoryCode) LIKE UPPER('%AL%') |
| Apostrophe literal | Test'Name | | | | | (UPPER(TerritoryShortName) LIKE UPPER('%Test''Name%') OR UPPER(TerritoryCode) LIKE UPPER('%Test''Name%')) |

## Prepared Create Mapping Contract

This is a logical field contract for the owning workflow's later serializer,
not a payload template or a registered Data Loader BO schema. Action names
do not establish filenames, DAT attributes, processing order or transactionality.

| Logical action | Parameter | Prepared value | Contract |
|---|---|---|---|
| upsertInstalledLegislation | legCode | Shared selected legCode | Same identity used by all sections; no independent selection |
| upsertLegislativeRules | legCode | Shared selected legCode | Required |
| upsertLegislativeRules | legRuleMap.I | Resolved Payroll Relationship Rule code | Preserve returned LookupCode |
| upsertLegislativeRules | legRuleMap.CALC_BREAK | Resolved Deduction Card TRU code | Equal to legRuleMap.GET_TU |
| upsertLegislativeRules | legRuleMap.GET_TU | Resolved Deduction Card TRU code | Equal to legRuleMap.CALC_BREAK |
| upsertLegislativeRules | legRuleMap.L | Validated tax_year_start_date | MM/DD |
| upsertDefCurrency | legCode | Shared selected legCode | Required |
| upsertDefCurrency | currencyCode | Resolved explicit or default currency code | Preserve chosen value and default_used marker |
| upsertPayRelationshipTypeMaps | legCode | Shared selected legCode | Required |
| upsertPayRelationshipTypeMaps | relTypeIds | RelationshipTypeId of each retained Payroll Relationship Type, in final row order | Paired by index with sysPersonType |
| upsertPayRelationshipTypeMaps | sysPersonType | System Person Type code of each corresponding retained row | Paired by index with relTypeIds |

## Default System Person Crosswalk

Embedded default-row aliases; this is not the live list of selectable person types.

| Meaning | SYSTEM_PERSON_TYPE |
|---|---|
| Sort by Employee Name | EMP |
| COLUMBIA COL SC (CON) | CON |
| Convention Centre | CON |
| Company director | FR_COMP_DIRECTOR |
| Weekly | PWK |
| Nonworker unpaid | NONW_UNPAID |
| Nonworker | NONW |
| External/Manual Payment | EMP |
| Update Name | CON |
| Continuing participation | CON |
| Nonworker Paid | NONW_PAID |
| Pensioner | PENSIONER |
| Applicant | APL |
| Applicants Only | APL |
| Obsolete - Applicant | APL |
| Benefit nonworker | BENNONWRKR |
| Contingent Workers | CWK |
| Employer action | EMP |
| Nonworker paid | NONW_PAID |
| Retiree | RETIREE |
| Contingent | CWK |
| Employment | EMP |
| Contact | CON |
| Pending Employee | PWK_EMP |
| Volunteer | VOLUNTEER |
| Benefit Nonworker | BENNONWRKR |
| Retirees | RETIREE |
| Worker-level budgeting | EMP |
| Employees | EMP |
| Employees Only | EMP |
| Ex-employee | EX_EMP |
| Ex-Contingent | EX_CWK |
| Ex-contingent Worker | EX_CWK |
| Ex-applicant | EX_APL |
| Enter applicant information | APL |
| Contingent Workers Only | CWK |
| Non Worker | NONW |
| Ex-contingent worker | EX_CWK |
| Trainee | FR_TRAINEE |
| PENSIONER | PENSIONER |
| Pending Worker | PWK |
| GSP Weekly Pay Rate | PWK |
| Pending Contingent Worker | PWK_CWK |
| Appraisee | EMP |
| Employer Initiated | EMP |
| Consulting | CON |
| Ex-Employee | EX_EMP |
| Obsolete - Ex-applicant | EX_APL |
| Nonworker Unpaid | NONW_UNPAID |
| Contingent Worker Candidate | ORA_CANDIDATE_CWK |
| Employee Candidate | ORA_CANDIDATE_EMP |
| Contingent Worker | CWK |
| Participant marital status | EMP |
| Employee | EMP |
| Enter employee information | EMP |
| Intern | ORA_PER_INTERN |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLHR.SEARCH | step | 6 | reference_lookup | matches->CLHR.COMPLETE;no_matches->CLHR.COMPLETE;multiple_matches->CLHR.COMPLETE;error->CLHR.ERROR | CLHR.ENFORCE_SEARCH_SCOPE | stop | Search only; run find_installed_legislations and all its applicable pages and diagnostics |
| CLHR.RESOLVE_DELETE_TARGET | step | 11 | reference_lookup | matched->CLHR.DELETE_DEFAULTS;no_matches->CLHR.ERROR;selection_required->CLHR.ERROR;conflict->CLHR.ERROR;error->CLHR.ERROR | CLHR.ENFORCE_DELETE_SCOPE | stop | Delete only; run resolve_installed_legislation_for_delete and retain the selected code/environment without constructing or loading a file |
| CLHR.VERIFY_DELETED | step | 21 | reference_lookup | absent->CLHR.DELETE_CONFIRMED;present->CLHR.DELETE_PRESENT;error->CLHR.ERROR | CLHR.ENFORCE_VERIFY_SCOPE | stop | Explicit Verify Delete only; run verify_installed_legislation_deleted after the loader-status prerequisites |
| CLHR.RESOLVE_CREATE_LEGISLATION | decision | 51 | reference_lookup | selected->CLHR.RESOLVE_CREATE_RULE_OPTIONS;choice_required->CLHR.CREATE_SELECTION_REQUIRED;unavailable->CLHR.CLASSIFY_UNAVAILABLE;error->CLHR.ERROR | CLHR.ENFORCE_CREATE_SCOPE | stop | Run resolve_available_legislation_for_create first; establish one shared selection or return choices |
| CLHR.CLASSIFY_UNAVAILABLE | decision | 52 | reference_lookup | classified->CLHR.CREATE_UNAVAILABLE;error->CLHR.ERROR | CLHR.RESOLVE_CREATE_LEGISLATION | stop | Run classify_unavailable_legislation only for a target absent from complete available results; classify installed versus unavailable |
| CLHR.RESOLVE_CREATE_RULE_OPTIONS | step | 53 | reference_lookup | resolved->CLHR.RESOLVE_CREATE_CURRENCY;error->CLHR.ERROR | CLHR.RESOLVE_CREATE_LEGISLATION | stop | For normal preparation run resolve_payroll_relationship_rule and resolve_deduction_card_tru_rule; options-only runs only requested rule resolvers or skips this node with resolved; collect choices and missing/invalid flags, no defaults |
| CLHR.RESOLVE_CREATE_CURRENCY | step | 54 | reference_lookup | resolved->CLHR.RESOLVE_CREATE_MAPPINGS;error->CLHR.ERROR | CLHR.RESOLVE_CREATE_RULE_OPTIONS | stop | For normal preparation use resolve_default_currency when currency omitted or resolve_currency_override when supplied; options-only runs just resolve_currency_override if currency was requested, otherwise skip with resolved |
| CLHR.RESOLVE_CREATE_MAPPINGS | step | 55 | reference_lookup | resolved->CLHR.CREATE_OPTION_REQUEST;error->CLHR.ERROR | CLHR.RESOLVE_CREATE_CURRENCY | stop | For normal preparation resolve needed default rows/crosswalk and live edited-row options; options-only runs only requested person/relationship LOVs without default mappings, otherwise skips with resolved; preserve ordered pairs and read-only ProcessInRun |
