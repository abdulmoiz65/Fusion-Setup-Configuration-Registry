# Manage Legal Jurisdictions Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Jurisdiction identity | Name, Territory or Geography, Legislative Category, Legal Entity Registration Code, Legal Reporting Unit Registration Code, Identifying Flag | Block before lookup and package generation | Supply one proposed jurisdiction definition | Every create or update request |  |
| Geography identity | One Territory selection identified by visible Territory/Geography Type/Name values, with optional Country refinement and as-of date | Block before remaining-LOV discovery and package generation | Complete addressGeographies identity discovery and applicable hierarchy enrichment, apply primary eligibility, preserve their eligible identities and coherent visible tuples, and resolve only through the Territory Resolution Gate | Every create or update request | resolve_jurisdiction_geography |
| Legal Entity Registration Code identity | One Legal Entity Registration Code | Block before package generation | Resolve the code from its documented standard lookup | Every create or update request | resolve_legal_entity_registration_code |
| Legal Reporting Unit Registration Code identity | One Legal Reporting Unit Registration Code | Block before package generation | Resolve the code from its documented standard lookup | Every create or update request | resolve_lru_registration_code |
| Legal Functions | Zero or more approved Legal Function values | Block only the function branch | Resolve each supplied function to an enabled internal FunctionCode before creating a child row | Legal Functions supplied | resolve_legal_jurisdiction_function_code |
| Current package baseline | Fresh successful same-target FSM task export metadata, CSV inventory, headers, and template fingerprint | Block before package generation | Export the task and record source evidence; use only metadata/template structure and never copy existing jurisdiction data rows | Every FSM package request | verify_jurisdiction_package_baseline |
| Territory discovery request | Optional Territory search text, optional Country/Geography Type/Name refinement, and as-of date; mode=discover_territories | With no search text, return the first bounded identity page. With search text, return no partial data until addressGeographies identity pagination and applicable enrichment complete, then deliver up to 50 inline rows and a linked complete Markdown table when additional rows exist | Select one returned Territory by its visible table values; this mode does not require any create fields | Display valid Territory choices before a create request | list_jurisdiction_territories |
| LOV discovery request | Territory and optional as-of date; mode=discover_lovs | Return no LOV data until Territory resolves and all required read-only endpoints are available | Supply or select a Territory; this mode does not require a Name, identifying choice, dates, or registration-code selections | Display all remaining valid choices together before a create request as four complete separate tables, each with a count and per-choice Markdown rows; tables above 50 rows require their complete linked Markdown list | resolve_jurisdiction_geography |
| Guided create request | Any subset of create fields | Do not discard supplied valid values or infer missing required values | When Territory is absent, show the first bounded identity page and request a Territory search term; Country is optional narrowing. When Territory is provided, search addressGeographies with the minimal identity projection and enrich without losing candidates. Apply primary eligibility before deduplicating coherent candidate tuples into the UI-style five-column Territory, Geography Type, Name, Name, Name table and require selection by visible row values, never an internal identifier. If more than one eligible candidate exists, do not nominate a row or ask for confirmation: show every row inline through 50, otherwise first 50 plus one complete Markdown table and total count. Do not issue a progress-only update. After Territory resolves, present all remaining required LOVs together. If Identifying Flag is absent, present the Y/N choice table. If either date is absent, prompt for optional `YYYY/MM/DD` values or explicit confirmation to leave it blank; Legal Functions remain optional | Iterative clarification for a create request | list_jurisdiction_territories |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Territory or Geography is supplied | Continue only when the Territory Resolution Gate has complete identity and applicable enrichment receipts and exactly one source identity resolves from the primary-eligible visible candidate set | Use the resolved source identity and selected hierarchy as evidence. Missing canonical carrier fields are recorded as a readiness warning and do not block package preparation or explicitly approved import submission. | resolve_jurisdiction_geography |
| Create is requested | Require the live name check. Require a complete non-conflicting geography/category check when canonical mapping is verified; otherwise exclude that check and identifying-impact verification as not_applicable warnings under the two-check policy | Persist the selected-hierarchy and duplicate-preflight evidence; missing canonical carrier fields remain a warning | find_legal_jurisdiction_existing |
| Legislative Category is supplied | Continue only when exactly one enabled LEGISLATIVE_CATEGORY code resolves | Use the internal lookup code; do not substitute a UI meaning without export evidence | resolve_legislative_category |
| Legal Entity Registration Code is supplied | Continue only when its enabled registration-code lookup resolves exactly | Use the internal lookup code; do not substitute a UI label without export evidence | resolve_legal_entity_registration_code |
| Legal Reporting Unit Registration Code is supplied | Continue only when its enabled registration-code lookup resolves exactly | Use the internal lookup code; do not substitute a UI label without export evidence | resolve_lru_registration_code |
| Create is requested | Reject a verified equivalent jurisdiction. Unavailable canonical mapping alone is handled by the two-check create policy; do not require proof of absence for those excluded checks | Reuse an equivalent definition; show differences and request an update-versus-new decision for a non-equivalent result | find_legal_jurisdiction_existing |
| End date or start-date change is requested | Continue only when active registrations are disproven and the effective-date policy passes | Retain the change as blocked when the required registration evidence is unavailable | verify_active_jurisdiction_registrations |

## Primary Territory Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Primary Territory and hierarchy | Require PrimaryGeographyFlag=true and the corresponding PrimaryGeographyLevel2Flag, PrimaryGeographyLevel3Flag, or PrimaryGeographyLevel4Flag=true for every populated displayed hierarchy level 2 through 4 on an addressGeographies candidate. Exclude explicit alternates before merging, counting, delivery, deduplication, and resolution; blank levels need no flag. | Every Territory choice or selected addressGeographies row | resolve_jurisdiction_geography |
| Missing or unknown primary flags | Re-read the complete documented flag projection; unresolved required flags block choice delivery and resolution. Do not infer eligibility, silently discard unknown rows, or report them as no matches. | Required primary flag is missing, null, or unrecognized | resolve_jurisdiction_geography |
| Alternate supplied by user | Deliver eligible primary choices and require a visible-row selection. Do not silently replace the hierarchy or reuse an excluded cached tuple as an import source. | User supplies a non-primary Territory or hierarchy variant | resolve_jurisdiction_geography |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Required fields | Reject blank Name, Territory/Geography, Legislative Category, Legal Entity Registration Code, Legal Reporting Unit Registration Code, or Identifying Flag | Every create or update request |  |
| Name and code lengths | Reject Name over 240 characters or Legislative Category and registration codes over 30 characters; never truncate | Values supplied |  |
| Identifying Flag | Accept Y or N only | Every create or update request |  |
| Missing Identifying Flag | Return the Y/N choice table and require an explicit selection; do not default from existing identifying jurisdictions | Every guided create request | find_legal_jurisdiction_existing |
| Effective dates | Reject Effective From later than Effective To | Both dates supplied |  |
| Optional effective dates | Accept neither date, Effective From only, Effective To only, or both dates when the current export/template permits omission | Every create request | verify_jurisdiction_package_baseline |
| Missing optional dates | Prompt for `YYYY/MM/DD` values or explicit confirmation that the omitted date(s) remain blank; do not synthesize a date | Every guided create request | verify_jurisdiction_package_baseline |
| Geography/category pair | Reject a verified Legislative Category already assigned to the same resolved Geography; if canonical mapping is unavailable for a valid create, record this check as not_applicable with warning, without a waiver | Create or mutable pre-save validation | find_legal_jurisdiction_existing |
| Name uniqueness | Reject a duplicate legal-jurisdiction Name | Create or rename request | find_legal_jurisdiction_existing |
| Immutable attributes | Reject a post-creation change to Name, Territory/Geography, or Legislative Category | Existing jurisdiction update | find_legal_jurisdiction_existing |
| System ownership | Reject user-supplied physical IDs, audit values, service-generated identifiers, or unproven technical codes | Every package request |  |
| Legal Functions child rows | For each supplied function, require one ORA_XLE_JURISDICTION_DATA row carrying the same selected parent geography transients, resolved FunctionCode, and `RequiredFlag` defaulting to `Y`, with explicit valid user input taking precedence; preserve a header-only child file when no function is supplied | Every FSM package request | resolve_legal_jurisdiction_function_code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LJ.TERRITORY_SELECTION_GATE | decision | 5 | validate_input | resolved->LJ.DISCOVER_LOVS;selection_required->LJ.RETURN_LOVS;choice_delivery_failed->LJ.HANDLE_ERROR;blocked->LJ.HANDLE_ERROR | LJ.DISCOVER_TERRITORIES | stop | Identity and applicable enrichment receipts and primary-filter evidence are complete and the eligible candidate set has been built; selection_required requires a complete five-column delivery receipt, not a single confirmation row |
| LJ.VALIDATE_INPUT | step | 10 | validate_input | valid->LJ.RESOLVE_REFERENCES;invalid->LJ.HANDLE_ERROR | LJ.DISCOVER_LOVS | stop | Before any lookup or FSM package preparation after the Territory gate and complete LOV discovery |
