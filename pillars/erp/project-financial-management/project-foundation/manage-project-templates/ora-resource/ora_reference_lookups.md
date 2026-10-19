# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Live Lookups

| Resolver | Runs when | Source values | Match rule | Values to fill | If no match or many matches |
|---|---|---|---|---|---|
| find_project_template | Every request | Fresh paginated GET `/fscmRestApi/resources/11.13.18.05/projectTemplates` | Exact template name and number, or a previously returned canonical item URI | Exists, canonical item URI, returned core attributes, returned child links | Zero is valid only for create; one is required for mutation; many blocks. |
| resolve_template_item_uri | Update/end-date/child CUD | Returned template `self` link | One returned canonical URI only | `projectTemplatesUniqID`/item URI | Block a constructed URI or a numeric `ProjectTemplateId` substitute. |
| resolve_template_references | Supplied core reference or documented child reference | Target REST operation schema and supplied request value | Require one documented name, ID, or code representation and the target operation's required field shape. Preserve a supported customer-supplied name directly. Never call an existing template's contextual LOV to validate or convert a new template's value. | Canonical request representation | Block missing required representation, conflicting alternatives, unsupported field, or invalid local type/format. Fusion POST validates existence, status, and compatibility. |
| resolve_project_plan_type | Project plan type supplied | Published Project Templates create/update schema and supplied request value | Require exactly one canonical `ProjectPlanType` name or `ProjectPlanTypeId`; do not serialize `ProjectPlanTypeName`. | Canonical request pair: `ProjectPlanType` with the supplied name, or `ProjectPlanTypeId` with the supplied ID | Block conflicting alternatives or a field absent from the target operation schema. Fusion POST validates target eligibility; do not perform a contextual LOV or project-unit reporting lookup before submission. |
| resolve_required_reference_id | Exact operation/runtime contract requires an ID but the customer supplied its documented name | A target-proven standalone resource whose returned ID is confirmed to be in the required domain | Exact normalized name, active/effective result when exposed, and cardinality one; never use a Project Templates contextual child LOV | Name-to-ID mapping recorded in the customer-readable preview | Block zero/multiple matches, wrong ID domain, or absence of a proven standalone resolver. Do not infer equality with another organization/reference ID. |
| resolve_template_sections | Every child request | ../references/project-template-rest-contract.md, ../references/project-template-operation-contracts.json, exact target family/method schema, documented defaults/inheritance and returned links when a parent exists | Leave omitted nested task organization absent and verify the actual organization from canonical task readback. Preserve explicit overrides and direct-create evidenced organization preparation; use evidenced project/parent-task cross-charge values. Work type requiredness is operation-specific; nested-create omitted external IDs are prepared by the FSCR defaulting policy and verified from task readback. Root/nested/direct schemas remain distinct | Prepared child values, default/inheritance evidence, supplied identifier/date status and canonical URIs | Block unsupported family/verb, conflicting alternatives, unresolved inheritance, malformed identifiers, unknown response/UI fields or incomplete method schema |
| resolve_template_use | Existing semantic/end-date change | A documented target consumer/use REST resource explicitly supplied for this target | Exact returned template identity | Consumer count, protected semantics, evidence URI | Block when no documented consumer resource is available or evidence is absent/ambiguous/conflicting. |
| verify_template_route | Before preview/execution | Published method/path/schema, authenticated target GET, structurally valid reference representations, any operation-required ID mappings, and repository-required registration evidence before submission | Every requested core field and nested child action has an exact REST contract and read-back; a zero-match create does not require item/child links before POST | Atomic or ordered REST operation list, coverage, authorization checkpoint, checksum inputs | Stop preview on contract or operation-required-ID gaps; stop submission on missing required registration. Do not pre-resolve supported root names or use absence of zero-row GET links as a blocker. |
| verify_template_scope | Before validation | Catalog task code and target connection | Exact task and target | Verified scope | Block mismatch. |

Project priority uses this operation-specific lookup contract:

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_project_priority | Root create/update supplies ProjectPriority or ProjectPriorityName | Supplied display name, target-confirmed PJF_PROJECT_PRIORITY_CODE type/key, selected business date and complete target GET evidence | GET /fscmRestApi/resources/11.13.18.05/standardLookups/PJF_PROJECT_PRIORITY_CODE/child/lookupCodes with structured q=Meaning='<priority name>', only after target evidence confirms that literal parent key | Meaning, LookupCode, EnabledFlag, StartDateActive, EndDateActive; evidence lookupType | Exact Meaning; EnabledFlag Y; inclusive effective bounds with explicit null for open bounds; count all enabled/effective members before validating the nonblank code; exactly one member after all pages | ProjectPriorityCode; supplied Meaning, redacted request/code/eligibility/date/cardinality evidence and artifact SHA-256 | Zero/multiple matches, missing eligibility/code fields, unproven type/key, failed or incomplete acquisition block. Never hide malformed matches or guess a code |
| resolve_template_code_values | A registered code-only display alias is supplied | Alias/type mapping in REST reference; target-confirmed type/key, supplied name and business date | GET /fscmRestApi/resources/11.13.18.05/standardLookups/{confirmed LookupType}/child/lookupCodes with structured q=Meaning='<supplied name>' | Meaning, LookupCode, EnabledFlag, StartDateActive, EndDateActive; evidence lookupType | Exact name, EnabledFlag Y, inclusive explicit effective bounds, complete pages and one eligible member with a nonblank code. Type must match the documented field mapping | Canonical field code and redacted supplied-name/type/request/eligibility evidence | Block unproven type/key, zero/multiple members, malformed/incomplete evidence or incompatible code. Supported name/hint request attributes bypass conversion |

The selected workflow acquires this read through core.fusion-api.rest-api-client,
passing q as a repeated structured query option and escaping apostrophes in its
literal. Follow all pages; combine items into one complete evidence envelope with
hasMore=false. Supply the target business date explicitly. The local validator
does not make this GET: it consumes --priority-lookup-json and --effective-date.
High resolves to HIGH only when that is the unique enabled effective target row.
An explicitly supplied ProjectPriorityCode is preserved as a code; do not infer
that a display name is already its code.

The common 26C lookup GET contract documents the route, q, pagination and
eligibility fields, but Project Templates does not name the priority lookup
type. Confirm PJF_PROJECT_PRIORITY_CODE and its literal path key through the
active workflow's selected target read evidence before acquiring codes; if it
cannot be proven, priority-name resolution remains blocked. Never manufacture
a hash key. Evidence envelopes include lookupType, items and hasMore=false.
For other documented code-only aliases, --lookup-evidence-json maps the exact
prepared path (for example root.AssetAllocationMethodCode or
root.Tasks[0].ProgressETCMethodCode) to that envelope. Direct task paths start
with child. Use --effective-date for every display-name resolution. The local
script does not prove source freshness, environment identity or lookup-type
existence; those are workflow acquisition gates.

## Lookup Execution Rules

verify_template_route records the active workflow's operation classification and
selected executor. Read success and payload preflight do not authorize a write.
Every import/load enters core.data-loader and requires its selected adapter,
registration and immutable-artifact/Task Hook/approval evidence. A direct task
operation explicitly selected outside import scope uses the supported shared
REST client, while the consuming workflow verifies the approval-bound artifact
and persists sanitized receipts. Do not relabel an import, invent an adapter,
or require task-specific checksum/diagnostic options from the generic client.

| Situation | What happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| Core field or child group omitted on update | Preserve current value/rows; do not include it in PATCH. |
| Root create with child arrays | Validate the published nested POST schema and exact target requirements; work type remains optional unless operation-required. No parent or child link exists or is required before the atomic POST. |
| Duplicate/copy/create-from requested | Stop: no published project-template REST copy endpoint is available. |
| Root collection exists | It proves no child method or child field by implication; validate each requested child action independently. |
| A requested REST method/field/child is absent | Stop before preview; do not partially create a claimed complete template. |
| Setup option supplied | Validate its documented field shape and prerequisite child data before enabling or updating; Fusion validates supplied reference eligibility on POST. |
| Approved REST operation fails | Stop; no retry, compensation, or route fallback. |
| Fusion reports an invalid root attribute | Compare the rejected key with the published and target operation schemas. Correct the skill contract, discard the rejected preview, and require a newly checksummed preview and fresh approval; never retry the old body. |
| A new-template create is being prepared | Do not call an existing template's `/lov/ProjectTypes`, `/lov/ProjectUnits`, or `/lov/OwningOrganizations`; the parent template changes the effective context. |
| A failed POST reports one downstream field | Report the exact Fusion error and stop. Do not infer that other values passed or vary fields automatically. |
| A failed POST returns `ORA-01403` without a field | Treat it as a downstream internal lookup failure, not a safe retry signal. Preserve the sanitized correlation headers and UTC window, compare the exact operation context with an evidenced successful product test or target record, and correct only an identified missing lookup/default. If none is identified, require target log diagnostics. Any correction requires a new payload, checksum, and approval. |
| Supplied values have dependent context | Preserve their exact documented representations in the approved payload. Fusion evaluates the business-unit/project-unit/legal-entity/owner/type combination at execution time. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTMPL.FIND_TEMPLATE | step | 3 | reference_lookup | resolved->PTMPL.RESOLVE_SECTIONS;failure->PTMPL.RETURN_ISSUES | PTMPL.APPLY_DEFAULTS | stop | Resolve template identity/duplicate baseline and, for an existing parent, its returned canonical URI |
| PTMPL.RESOLVE_SECTIONS | step | 4 | reference_lookup | resolved->PTMPL.ROUTE_OPERATION;failure->PTMPL.RETURN_ISSUES | PTMPL.FIND_TEMPLATE | stop | Validate requested base representations, any exact operation-required ID conversion, child operations, and REST contracts |
