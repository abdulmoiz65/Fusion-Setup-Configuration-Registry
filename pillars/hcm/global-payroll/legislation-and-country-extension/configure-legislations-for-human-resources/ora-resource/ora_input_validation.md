# Configure Legislations for Human Resources Input Validation

This file owns input/output shape and required values. Fusion is the authority
for available legislations, installed records, and selectable options.
Query construction and field translation belong to ora_reference_lookups.md.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | One nonempty operation string from the invoking workflow | Ask which operation is intended; never infer a mutation | Normalize Search, Create, Delete, and Verify Delete; apply the Operation selection field rule | Always | |
| Delete execution intent and phase | execution_intent derived from the user request; phase derived from the invoking workflow | Apply the Execution intent and Execution phase field rules; do not ask the user for technical phase values | Keep preparation, Data Loader validation, and later verification distinct | Delete | |
| Search filters | Any subset of Legislation or Legislation Code, Legislation, Legislation Code, Predefined, Implemented | No filter is required | An empty filter set is valid; omission behavior belongs to ora_defaulting_rules.md | Search | |
| Delete target | legislation_name or legislation_code; accept the aliases below | Ask which legislation to delete in the user's language; return MISSING_TARGET | Reuse a supplied identifier; a name is sufficient input and is resolved by the lookup | Delete | |
| Deletion verification target | Exact previously selected legislation_code and its environment plus a successful load result with zero failed objects | Return MISSING_VERIFICATION_CONTEXT | Recover the selected target and load outcome from the same workflow; do not guess them from a ZIP name | Verify Delete | |
| Create legislation | One optional legislation_name and/or legislation_code, or request to list available legislations | Resolve available choices first, then ask for one name/code; do not ask dependent questions yet | Reuse supplied identifiers; one legislation per Create session | Create entry | resolve_available_legislation_for_create |
| Legislation Rules inputs | tax_year_start_date and deduction_card_tru_rule; optional default_currency, payroll_relationship_rule, payroll_relationship_mappings | Ask only for missing required business values after selection and option retrieval | Present valid choices with the question; preserve all supplied values | Create after successful selection | |
| Final archive context | phase=validate_artifact, exact final archive, retained selection context, and Data Loader preflight | Return MISSING_ARTIFACT_CONTEXT | Data Loader prepares the immutable artifact before selecting Task Hook | Task Hook validation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Filter names | Accept only the listed business filters and the aliases below; reject raw q, arbitrary field names, request headers, URLs, and write attributes as search filters | Search filters supplied | |
| Text values | Accept scalar strings; trim leading and trailing whitespace without altering internal spaces, punctuation, or case; reject arrays, objects, numbers, booleans, null bytes, and line/control characters | Any text filter supplied | |
| Empty text | Normalize a missing, null, empty, or whitespace-only optional text filter to absent | Text normalization | |
| Yes/No values | After trimming, accept exactly Yes or No; reject booleans, true, false, Y, N, and other spellings; a missing, null, empty, or whitespace-only optional flag is absent | Predefined or Implemented supplied | |
| Duplicate aliases | Merge identical normalized values for the same filter; reject conflicting values instead of taking the last one | The same filter is supplied more than once | |
| LIKE metacharacters | Reject percent and underscore in text for this contains-search contract; explain that user-supplied wildcard patterns are not supported; this is a client input restriction, not an Oracle attribute constraint | Installed-legislation filter/identifier text contains % or _; not Create LOV labels or codes | |
| Mixed filters | Preserve every distinct validated filter; never drop a filter to get a result | Two or more filters supplied | |
| Response collection | Require an object containing items as an array, count as a nonnegative integer equal to the page item count, hasMore as a boolean, limit as a positive integer, and offset as a nonnegative integer | Each installedLegislations GET response | |
| Response result fields | Require nonempty string TerritoryShortName and TerritoryCode, Meaning equal to Yes or No, and ImplementedFlag equal to string true or false; do not substitute similar fields or convert unknown values to No | Each installedLegislations result row | |
| Response totalResults | When present, require a nonnegative integer; pagination semantics belong to the lookup contract | Collection has totalResults | |
| Operation selection | CLHR.SELECT_OPERATION maps Search to search, Create to create, Delete to delete, Verify Delete to verify_delete, and other operations including Update/Edit to unsupported; RestAction never selects the branch | After input and readiness checks | |
| Execution intent | A request to prepare a deletion file selects Delete with execution_intent=prepare_only; an explicit request to delete in Fusion selects Delete with execution_intent=load; neither grants upload approval | Delete request normalization | |
| Execution phase | Use phase=prepare for Search or Delete preparation; Data Loader Task Hook data-load supplies phase=validate_artifact with the final archive and original selection context; do not infer artifact validation from a filename alone | Workflow context normalization | |
| Delete cardinality | Accept exactly one target per request; reject arrays, a list of targets, wildcard targets, or a blind deletion | Delete | |
| Delete identifiers | Trim scalar name/code inputs, reject control characters and DAT delimiters, and normalize blank identifiers to absent; require at least one; do not translate names or infer codes | Delete or Verify Delete | |
| Delete attribute input | Business input is a name/code; permit only the five declared DAT attributes in prepared data; reject extra filters or arbitrary action/header values | Delete | |
| Fixed values | Fill missing draft values using ora_defaulting_rules.md; reject conflicting supplied values rather than silently replacing them | Delete, phase=prepare | |
| Resolved identifiers | legCode and InstalledLegislationKey must both equal the exact code returned by resolve_installed_legislation_for_delete; never truncate or sanitize that code to make a DAT field valid | Delete contract check | resolve_installed_legislation_for_delete |
| DAT shape | Require UTF-8, one METADATA section for deleteInstalledLegislation and one MERGE record, with exactly five attributes and five values in this order: InstalledLegislationKey, legCode, Content-Type, REST-Framework-Version, RestAction; omit SourceRef fields; reject embedded delimiters, control characters, duplicate/unknown attributes, extra records, and placeholders | Delete contract check; validate prospective fields in phase=prepare and actual bytes in phase=validate_artifact | |
| DAT identity | The planned source basename and sole root ZIP member name must be deleteInstalledLegislation.dat; in phase=validate_artifact require that actual name and layout; reject suffixed DAT filenames even when the METADATA discriminator is correct | Delete contract check | |
| Artifact destination | A prepared DAT belongs under project/{project_id}/artifacts/pillars/hcm/global-payroll/legislation-and-country-extension/configure-legislations-for-human-resources/ in a distinct run or version folder; preserve the exact DAT basename and never overwrite another prepared deletion; the outer ZIP name may vary | Delete artifact preparation | |
| Resolved selection output | Retain the exact legCode, resolved_legislation_name, selected environment, original identifiers, and sanitized complete lookup evidence; bind any prepared DAT and loader continuation to that same selection | Delete after successful target resolution | resolve_installed_legislation_for_delete |
| Final artifact values | Compare the actual immutable archive's decoded values and member name with the selected code and fixed-value contract; no defaulting, normalization, rewriting, or additional row is allowed inside these bytes | Delete, phase=validate_artifact | |
| Create stage | Use phase=prepare_rules for this delivery; no DAT or load contract is implied by prepared values | Create | |
| Create input shape | Accept scalar name/code, currency name/code, rule Meaning labels, month/day or MM/DD, and ordered mapping-row edits; trim scalar text and treat null/blank optional text as absent, while an explicit empty mapping replacement stays empty; reject control characters, embedded DAT delimiters, raw URLs and arbitrary request parameters | Initial supplied input validation | |
| Shared selection | Require one resolved legislation name, exact legCode, original identifiers, selected environment and complete eligibility evidence; preserve this same selection across Legislation Rules, Element Classifications, Payment Types, Component Groups and Balance Dimensions | After available-legislation selection | resolve_available_legislation_for_create |
| Tax Year Start Date | Require integer month/day or unambiguous numeric MM/DD; month 1..12; day 1..31 for Jan/Mar/May/Jul/Aug/Oct/Dec, 1..30 for Apr/Jun/Sep/Nov and 1..29 for Feb; accept 02/29 because no year is supplied; normalize to two-digit MM/DD; reject nonexistent dates rather than roll them over; never infer January 1 from an empty input | After legislation selection | |
| Payroll Relationship Rule | Accept an exact displayed Meaning under trimmed case-insensitive comparison; an invalid supplied value is not an omission and is never defaulted | Rule value supplied | resolve_payroll_relationship_rule |
| Deduction Card - Tax Reporting Unit Association Rule | Required; accept an exact displayed Meaning; no default; return MISSING_CREATE_INPUTS with current options if absent or INVALID_CREATE_OPTION if unknown | After legislation selection | resolve_deduction_card_tru_rule |
| Currency input | Optional currency name and/or code; if both are supplied they must identify the same live LOV row; reject ambiguous or invalid explicit values instead of using the default | Currency override supplied | resolve_currency_override |
| Requested option lists | Distinguish a request to show/choose options from omission: retain requested_options for payroll rule, TRU rule, currency, System Person Type or Payroll Relationship Type; allow listing with no proposed value | Create supplied intent | |
| Mapping rows | Each final row has one System Person Type and one Payroll Relationship Type; reject a supplied writable Process in Payroll override; it is returned read-only data | Mapping draft | |
| Mapping edits | Distinguish omitted mapping input from explicit empty replacement; allow add, remove, edit or replace-all as requested; require row selection when the edited target is ambiguous | Mapping draft | |
| Mapping duplicates | Reject two final rows for the same System Person Type; the same Payroll Relationship Type may occur in several rows | Mapping draft | |
| Prepared arrays | Derive relTypeIds and sysPersonType together from final ordered rows; require equal lengths and nonempty scalar values per retained row; preserve each index pair after deletion or replacement; never sort the arrays independently | Prepared mapping output | |
| Shared legCode in outputs | All four logical upsert inputs use the exact resolved legCode; input changes cannot override it independently per section | Prepared Create output | |
| Missing rule inputs | After available selection and LOV discovery, ask Tax Year Start Date and missing TRU choice together; also report invalid explicit inputs and their valid choices; do not ask approval for omitted defaults | CLHR.VALIDATE_CREATE_RULE_INPUTS | |

The input-shape checks operate on the request and prepared artifact as specified
by the developer-approved contract. They do not establish record existence;
the named Fusion lookup is the authority for record identity.

Field Validation defines the DAT and selection-output contracts. The design
rules define the owning workflow's preparation and Data Loader handoff gates;
these rules are not a stored payload template or a task-local HTTP client.

## Input Aliases

| User Input | Canonical Filter | Value Contract |
|---|---|---|
| Legislation or Legislation Code / search_text | search_text | Shared name-or-code text |
| Legislation / Legislation Name / TerritoryShortName / legislation_name | legislation_name | Explicit name text |
| Legislation Code / TerritoryCode / legCode / legislation_code | legislation_code | Explicit code text |
| Predefined | predefined | Yes or No |
| Implemented | implemented | Yes or No |

## Validation Examples

| Input | Expected Result |
|---|---|
| Search with no filters | Valid |
| Predefined=No and Implemented=Yes | Valid |
| Predefined=true as a boolean | Invalid |
| Implemented=false as a string | Invalid; supply No |
| Unknown filter InstalledFlag | Invalid |
| Legislation and TerritoryShortName with conflicting values | Invalid |
| Text containing an apostrophe | Valid literal; escaping belongs to the lookup |
| Text containing % or _ | Invalid wildcard input |
| HTTP success with items missing or an invalid flag value | Response contract failure, not NO_MATCHES |
| Delete without a name or code | MISSING_TARGET; ask for the legislation name; no query or DAT |
| Delete with a supplied name | Do not ask for it again; resolve it before preparing a DAT |
| Delete with several targets or no identifier and only a Search flag | Reject bulk or blind deletion; no DAT |
| Delete with RestAction=DELETE or a nonmatching dummy key | Reject the conflicting contract value; do not silently repair it |
| Final archive omits a fixed value that task context could default | Reject the artifact; defaulting must not hide missing archive values |
| DAT member has a suffix while the outer ZIP name is descriptive | Reject the member name; the outer ZIP name is not the business-object discriminator |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLHR.VALIDATE_INPUT | step | 1 | validate_input | valid->CLHR.CHECK_READINESS;invalid->CLHR.ERROR | none | stop | Validate operation and supplied shapes only; Create may omit its target or rule inputs until available-legislation selection and options; Delete retains its required target; defer resolved-value checks to the selected branch |
| CLHR.SELECT_OPERATION | decision | 3 | evaluate_result | search->CLHR.SEARCH_DEFAULTS;create->CLHR.ENFORCE_CREATE_SCOPE;delete->CLHR.ENFORCE_DELETE_SCOPE;verify_delete->CLHR.ENFORCE_VERIFY_SCOPE;unsupported->CLHR.ERROR | CLHR.CHECK_READINESS | stop | Apply the Operation selection field rule to the normalized business operation; RestAction never selects a branch |
| CLHR.VALIDATE_DELETE_CONTRACT | step | 13 | validate_input | valid->CLHR.ENFORCE_DELETE_DESIGN;invalid->CLHR.ERROR | CLHR.DELETE_DEFAULTS | stop | Validate resolved values and prospective DAT shape in phase=prepare; in phase=validate_artifact inspect the actual final archive without changing its bytes |
| CLHR.VALIDATE_CREATE_RULE_INPUTS | step | 64 | validate_input | valid->CLHR.ENFORCE_CREATE_DESIGN;missing->CLHR.CREATE_INPUT_REQUIRED;invalid->CLHR.ERROR | CLHR.CREATE_DEFAULTS | stop | Validate required date and TRU choice, resolved explicit options and final paired-row output; report only missing or invalid business inputs |
| CLHR.CREATE_OPTION_REQUEST | decision | 56 | evaluate_result | choices_requested->CLHR.CREATE_OPTIONS_RETURNED;continue->CLHR.CREATE_DEFAULTS | CLHR.RESOLVE_CREATE_MAPPINGS | stop | If requested_options is nonempty, return its resolved choices and ask for the desired selection without applying omission defaults; otherwise continue preparation |
