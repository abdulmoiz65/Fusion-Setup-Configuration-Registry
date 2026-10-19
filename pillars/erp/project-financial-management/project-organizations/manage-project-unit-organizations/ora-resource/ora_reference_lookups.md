# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

For load-status and post-load checks, a retained Data Loader receipt means the
registered append-only acceptance binding in the selected project, including the
server-issued Request ID, exact target, approved archive hash and approval reference.
Follow `ora_dependency_readiness.md#execution-persistence-and-resume-contract`; chat history alone is insufficient.
Missing request identity or durable binding blocks the later resume route.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_active_organization | PUORG.FIND_ORGANIZATION | Target, requested organization name, optional effective date, classification and location | GET {podBaseUrl}/hcmRestApi/resources/{version}/organizations through core.fusion-api.rest-api-client | OrganizationId, Name, ClassificationCode, optional returned ClassificationName, LocationId, EffectiveStartDate, EffectiveEndDate, Status | Discover version and describe first; q=Name='name'; optional ClassificationCode and LocationId only when queryable; group all pages by OrganizationId; retain organizations active on the applicable date; fetch every classification for a selected ID without narrowing filters | ActiveOrganizationMatches, SelectedOrganization, ClassificationsComplete, Classifications, DerivedAction | No active match derives CREATE_NEW. One eligible active match without active PRJ_PROJECT_UNIT derives USE_EXISTING_ORGANIZATION. An active PRJ_PROJECT_UNIT match stops as already defined. Multiple active organizations or eligible parent classifications require explicit selection by ID, classification, location and effective dates |
| resolve_organization_classification | PUORG.RESOLVE_EXISTING_CLASSIFICATION after an eligible existing organization and exact parent ClassificationCode are selected | Exact ClassificationCode from SelectedOrganization | GET {podBaseUrl}/hcmRestApi/resources/{version}/organizationClassificationsLOV | ClassificationCode, ClassificationName | Describe first; q=ClassificationCode='code' when supported, otherwise inspect all pages; require exactly one exact code match and retain its exact display label | ResolvedOrganizationClassification with exact ClassificationCode, ClassificationName and resolver EvidenceRef | Block missing or ambiguous matches, code mismatch, blank label, or disagreement with a ClassificationName returned for the selected organization |
| resolve_organization_location | ExistingLocation supplied | Location name | GET {podBaseUrl}/hcmRestApi/resources/{version}/locationsLov | LocationId, LocationName, ActiveStatus | Describe first; q=LocationName='name' when supported; exact active match | SelectedLocation and LocationId narrowing filter | Require user selection for multiple eligible locations; no silent first match |
| verify_project_unit_after_load | PUORG.VERIFY_POST_LOAD after PUORG.LOAD_COMPLETION_GATE proves terminal success | Target, exact organization name, DerivedAction, effective date, requested Project Unit Code, durable Data Loader receipt, and terminal status evidence | GET {podBaseUrl}/hcmRestApi/resources/{version}/organizations by exact name; follow the selected organization's returned extraInformation child link through core.fusion-api.rest-api-client | OrganizationId, Name, ClassificationCode, ClassificationName, Status, EffectiveStartDate, EffectiveEndDate; OrgInformationContext, SequenceNumber, projectUnitCode | Discover metadata first and inspect all pages; confirm an active PRJ_PROJECT_UNIT classification on the effective date and a PRJ_PU_ATTRIBUTES row with SequenceNumber 1 and the exact requested Project Unit Code | PostLoadClassificationVerified, PostLoadAttributesVerified, VerifiedOrganizationId, VerificationEvidenceRef | No match, ambiguity, missing classification, missing EFF row, or code mismatch is a failed verification; preserve the durable receipt and stop without resubmitting the load |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_project_unit_setup_scope | Before external lookup | Project target, catalog flags, task PJF_MANAGE_PROJECT_UNIT_ORGANIZATIONS, functional area ORA_PJF_PROJ_ORG, offering PJF_PROJ_MNG | Exact target and catalog; workflow client identity, privilege and metadata prerequisites pass | Verified scope and target | Stop on mismatch or missing execution route |
| resolve_project_unit_member_linkage | Before generation | Selected name/classification and effective dates or new name | Existing: exact returned Name plus existing ClassificationName; new: name plus Project Unit Classification; identical dates across rows | Parent linkage proof | Block missing or mismatched references; OrganizationId is evidence only |
| verify_project_unit_package_contract | Before preview | ZIP, action, generated DAT and request/evidence | Offline validator passes with expected action; regenerate from evidence and compare exact payload; only Organization.dat at ZIP root | Validated rows, payload match and SHA-256 checksum | Block structural errors or mismatch to approved identity/evidence |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| Before any live request | Active project workflow must select this read-only lookup step and core.fusion-api.rest-api-client; verify identity, privileges, catalog, metadata and diagnostics destination first. Missing route/client or metadata is a blocker |
| Query construction | Use client query parameters for URL encoding of q; escape literals using discovered query grammar. Do not interpolate unsafe quotes or invent queryable fields, REST framework version, pod host or child URL |
| Optional filters | Resolve location and classification first. Narrowing filters cannot prove absence of Project Unit classification |
| Routing and eligibility evidence | Search before choosing an action. Fetch all classifications for a selected OrganizationId without classification/location narrowing, with pagination and relevant effective dates; derive CREATE_NEW or USE_EXISTING_ORGANIZATION, or stop as already defined or selection required; normalize status and retain REST date provenance for HDL normalization |
| Existing anchor identity | After USE_EXISTING_ORGANIZATION selection, resolve the exact selected ClassificationCode through organizationClassificationsLOV. Only then bind the selected REST EffectiveStartDate, exact Name, exact returned ClassificationCode and exact LOV ClassificationName to the first Organization MERGE anchor; never substitute PRJ_PROJECT_UNIT or Project Unit Classification in that anchor |
| Supplied code | Do not run a cross-Project-Unit uniqueness search. No invented business regex applies. ORA_PJF_CHAR_150_OPTIONAL is the supplied tenant value-set finding; validate through the configured mechanism when available |
| Evidence persistence | Persist redacted target, collection time, provenance, scope/completeness, selections, matches and diagnostics under project workspace. Never record credentials or sensitive raw tenant payloads in tracked files |
| Data Loader monitoring boundary | Accepted initiation ends the submission request without status or post-load reads. Only a later explicit status request selects core.data-loader monitoring for the same target-bound accepted request ID. Follow Core's complete status/count/diagnostic contract; nonterminal status or timeout returns In Progress and waits for another explicit request, never resubmits or starts automatic polling |
| Post-load verification | Run only after PUORG.LOAD_COMPLETION_GATE proves terminal success with a durable receipt. Require both verified outputs from verify_project_unit_after_load before reporting task success; never treat initiation or terminal loader status alone as configuration success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUORG.FIND_ORGANIZATION | step | 2 | reference_lookup | resolved->PUORG.ROUTE_OPERATION;failure->PUORG.RETURN_ISSUES | PUORG.VALIDATE_INPUT | stop | Search exact name, resolve optional filters, fetch unfiltered classifications as needed, and return routing evidence |
| PUORG.ROUTE_OPERATION | decision | 3 | evaluate_result | create_new->PUORG.APPLY_DEFAULTS;use_existing_organization->PUORG.RESOLVE_EXISTING_CLASSIFICATION;already_project_unit->PUORG.RETURN_ALREADY_PROJECT_UNIT;selection_required->PUORG.RETURN_ISSUES;failure->PUORG.RETURN_ISSUES | PUORG.FIND_ORGANIZATION | stop | Derive exactly one action from complete organization-search evidence; never use a user-selected action |
| PUORG.RESOLVE_EXISTING_CLASSIFICATION | step | 4 | reference_lookup | resolved->PUORG.APPLY_DEFAULTS;failure->PUORG.RETURN_ISSUES | PUORG.ROUTE_OPERATION | stop | USE_EXISTING_ORGANIZATION only: resolve the exact selected returned ClassificationCode to one organizationClassificationsLOV display label before defaults or HDL generation |
| PUORG.VERIFY_POST_LOAD | step | 11 | reference_lookup | created_verified->PUORG.RETURN_CREATED;existing_verified->PUORG.RETURN_EXISTING_DEFINED;mismatch->PUORG.RETURN_ISSUES;failure->PUORG.RETURN_ISSUES | PUORG.LOAD_COMPLETION_GATE | stop | After terminal Data Loader success, confirm active classification and sequence-1 Project Unit attributes for every archive row before task success |
