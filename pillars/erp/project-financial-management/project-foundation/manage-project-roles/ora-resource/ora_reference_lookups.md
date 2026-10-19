# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| find_project_role | Create/update/import | One fresh PJF_MANAGE_PROJECT_ROLES data export per validation package/run from shared.setup-export.task-level-export; PJF_PROJECT_ROLE.csv is the local baseline and its child members are joined to it | Exact ProjectRoleName; stable code where available | Exists, seeded state, dates, baseline, children | Zero=create only; one=update; ambiguity blocks |
| resolve_role_children | Qualification/translation supplied | The same one-per-package fresh PJF_MANAGE_PROJECT_ROLES data export, its qualification/translation CSV members, and PM implementation flag | Qualification: join to parent PJF_PROJECT_ROLE.csv by ProjectRoleName, then match resolved ContentItemId and Keyword. Translation: join by parent ProjectRoleName, then match Language | Current rows, duplicate state, implementation support | Block ambiguous/unsupported children |
| resolve_project_qualification_context | Qualification or keyword supplied/changed | Fresh same-target PJF_MANAGE_PROJECT_ROLES qualification export, joined to its parent role export, plus target template/feature-mode evidence; for a candidate absent from that export, same-target Manage Project Roles Requirements LOV selection evidence in setup_data_artifacts | Search all exported qualification rows, regardless of parent role. Match the resolved ContentItemId and ContentTypeId when those columns exist; otherwise require one canonical Name match after the active content-item lookup, one SectionName, and no competing eligible identity/section. Never assume the export contains ID/type columns until its headers are verified. One matching nonblank SectionName plus a current target package that retains that section supports reuse for a new role without asking the user for a screenshot; it is evidence of existing setup, so do not call it fresh UI selectability proof. A blank SectionName supports the sectionless LOV mode only if target template and feature-mode evidence prove sectionless serialization. For an unseen item or a new section, require target LOV evidence containing Name, ContentItemId, ContentTypeId, SectionName/SectionId when section-aware, target, task, capture date, and selectable state. Do not infer a new section from an HCM content type or generic profile section | Proven target serialization mode and canonical SectionName/SectionId when applicable; same-target item/section evidence and internal business-group context only when exposed | Zero or multiple eligible sections, conflicting mode/package evidence, stale/cross-target evidence, or inactive item blocks child preview. Ask only for missing target evidence or a choice among actual candidates; do not demand a screenshot when a unique exported item/section and current package prove reuse |
| resolve_role_use | End-date/association/removal | Project assignment, resource request, and access-impact evidence | Exact role ID | Use counts and affected consumers | Block missing/ambiguous/conflicting use evidence |
| verify_project_role_scope | Before validation | Catalog codes and target | Exact task/target | Verified scope | Block mismatch |
| verify_project_role_package | Import preparation or loader Task Hook validation | Target task CSV template/metadata and fresh export from shared.setup-export.task-level-export, plus exact prepared immutable package and its loader preflight facts | Exact task/target, conditional member set, headers, counts, checksum and CSV-to-XML wrapper. An observed populated export does not prove a blank template, child-only wrapper, keyword-only serialization or clear/removal semantics. The current Task Hook's own result is an output, never a prerequisite of this lookup | Verified contract and immutable artifact facts returned to loader preflight | Block unproven/changed/mixed package; preserve unchanged existing parent for child changes until a child-only wrapper is proved |

## Live Lookups

Run every live lookup through core.fusion-api.rest-api-client after the selected
workflow has validated task/target identity, catalog scope and required read
privileges. Load that client's references/fusion-rest-api.md, then invoke its
scripts/fusion_rest_client.py with the documented relative endpoint, --method GET,
repeated --query key=value arguments, and the same REST-Framework-Version header
resolved from the selected core workflow in the preflight above.
Use the existing core OAuth route; do not implement authentication or transport
in this task. Safely encode query values and retain sanitized response evidence
under the task's project workspace. Never persist credentials, Authorization
headers or token-cache contents. Stop on input, privilege, transport or response
failure; only the client's one cached-token refresh retry is permitted.

Before claiming absence or uniqueness, collect all result pages using the
server's returned limit and offset until hasMore=false, without adding a limit
parameter to the filtered enterprise-role requests. Nonadvancing pagination,
failed pages and conflicting duplicate identities cannot prove cardinality.
De-duplicate by the returned stable ID and cache completed results only for the
current run, target and authenticated identity. These read contracts authorize
no role or qualification mutation; writes retain the approved Data Loader route.

`PJF_PROJECT_ROLE.csv.RoleName` and `PJF_PROJECT_ROLE.csv.RoleCommonName` are two alternate lookup columns for the same HCM enterprise-role row. `RoleName` is matched through REST `RoleName LIKE '%value%'`; `RoleCommonName` is matched through REST `RoleCode = value`. When RoleCommonName is supplied, resolve by RoleCommonName first and use RoleName only when that code lookup returns zero eligible rows. A multi-row code result is an ambiguity blocker.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_active_enterprise_role | Enterprise Role supplied or changed | RoleCommonName (preferred) and/or RoleName | Use the workflow-resolved REST-Framework-Version header. GET /hcmRestApi/resources/11.13.18.05/rolesLOV with onlyData=true, fields=RoleId,RoleName,RoleCode,Description,JobRole and q=(RoleCode = '<RoleCommonName>') and (ActiveFlag = true) and ((JobRole = 'Y') or (AbstractRole = 'Y')). Only after zero code matches and supplied RoleName, or with name-only input, use q=(RoleName like '%<RoleName>%') with the same predicates. Do not send limit. Escape literal values before query serialization and URL encoding | RoleId, RoleName, RoleCode, Description, JobRole | Exactly one eligible code result wins; multiple code matches block without name fallback. Name fallback must also return one distinct eligible identity. Do not match descriptions or unverified translated/ordinary wording | Canonical RoleName for CSV RoleName, RoleCode for CSV RoleCommonName and internal RoleId | Block zero applicable matches, multiple identities or incomplete pagination |
| resolve_project_qualification_type | Predefined Requirements display name supplied, with optional type hint | Supplied type if any; otherwise IDs 103, 104, 106, 108, 109, 110 from the indexed project qualification VO | /hcmRestApi/resources/11.13.18.05/contentTypesLOV with q=ContentTypeId=<id>, fields=ContentTypeId,ContentTypeName,ContextName and onlyData=true | ContentTypeId, ContentTypeName, ContextName | Resolve an explicit type against the supported IDs; otherwise obtain the six target types and search the entered name across them. The Requirements LOV derives Type from the selected item. Use target-returned names, never a hardcoded localized label; target qualification-context agreement is checked after candidate resolution | Supported ContentTypeId and canonical target type metadata; not SectionName | Block unsupported/conflicting type or ambiguous eligible candidate; do not ask the user for a type before searching |
| resolve_active_qualification_requirement | Predefined Requirements Name or ContentItemId supplied | Entered display name or selected ID, resolved supported ContentTypeId and target current date | /hcmRestApi/resources/11.13.18.05/contentItemsLov with finder=findByWord;ContentTypeId=<id>,FilterAttributes=Name,SearchTerms=<normalized requirement>, fields=ContentItemId,Name,ContentTypeName,RatingModelId and onlyData=true. For the selected ID, verify membership with finder=findActiveContentItemByDate;ContentTypeId=<id>,DateFrom=<as-of date>,DateTo=<same date> and q=ContentItemId=<selected ID>, using the same fields | ContentItemId, Name, ContentTypeName, RatingModelId | Search once per distinct requirement/type and prefer an exact display-name match after normalization; verify every selected ID in the active finder on the target's current date. A word-search result alone proves neither activity nor project eligibility. Select only one exact eligible candidate or ask the user to choose among returned names/types; pass the resolved candidate to resolve_project_qualification_context | Canonical Name, ContentItemId, supported type, as-of evidence and RatingModelId; leave Keyword blank for this form | Block zero/inactive/unsupported candidates, incomplete pages or ambiguity; never convert an unresolved Name silently to a keyword |
| resolve_active_qualification_rating | Rating supplied after an eligible predefined item/context is resolved | Supplied rating identity/wording, resolved ContentItemId and RatingModelId; same target/authenticated context | /hcmRestApi/resources/11.13.18.05/ratingLevelsLOV with finder=findByContentItemId;ContentItemId=<resolved ID>, fields=RatingLevelId,RatingLevelCode,RatingShortDescr,RatingDescription,RatingModelId,RatingModelCode,RatingModelName,NumericRating and onlyData=true | Rating identity, short description, model identity and numeric rating | Collect the content-item-scoped set once. Resolve each supplied value to one member; wording/translation may suggest candidates but cannot override ambiguity. Require returned RatingModelId to agree with the selected item's model; a null/mismatched model blocks supplied ratings. Keep the same target/session qualification context; the public response does not expose BusinessGroupId or a rating active flag | Canonical RatingShortDescr mapped to the corresponding original RatingShortDescr1, 2, 3 or 4 CSV column; internal rating identity | Block keyword ratings, missing item/context/model, zero/multiple matches or model conflict. Never use a global rating set, invent BusinessGroupId, or claim a separate rating effective-state check |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| Child/enterprise-role group omitted | Preserve current values |
| Blank enterprise role supplied on update | Treat as explicit removal, not omission; require capability/use proof |
| Qualifications supplied while Project Management is not implemented | Block rather than discard rows |
| Role is seeded | Preserve without attempting mutation |
| Many input rows are validated | Export once for the validation package/run, then use PJF_PROJECT_ROLE.csv as the local parent baseline and join all child rows by ProjectRoleName; do not issue an export per row |
| Existing project-role qualification membership must be checked | Use the fresh task-level data export and resolve the child alternate key; no public read REST contract is declared for this membership |
| Business-object extract or GET exists | Do not treat it as setup-write authority |
| Blank template unproven | Keep import blocked |
| Requirement Name occurs in multiple content-item candidates | Suggest existing Name and ContentTypeName values; require explicit selection before active/context verification and ratings |
| A resolved ContentItemId is reused by multiple rows | Read its rating-level LOV once, cache the returned values for the run, and resolve all four rating columns locally from that same set |
| A batch contains repeated normalized requirement names | Cache search by requirement, content type, target, authenticated identity and as-of date; cache active checks by selected ID and the same context. Do not reuse a name resolution across distinct sections or types |
| Explicit keyword-only row | Preserve the supplied free text; skip content-type, content-item and rating lookups. Resolve target keyword SectionName/representation from qualification-context and package evidence; do not infer a localized Keyword label |
| Qualification section metadata from a generic HCM LOV | It is corroborating metadata only, not proof of Manage Project Roles selection. Indexed QualificationBySectionVO applies Project Resource Management implementation flags, PJR talent-section inclusion, active profile sections and content value-set/section joins. A generic content-type name or profile section cannot establish identical project eligibility |
| Enterprise Role supplied | Cache the code-first resolver by input mode and target/authenticated identity. RoleCode maps to CSV RoleCommonName; SCIM id is a GUID and cannot replace numeric RoleId |
| RoleCode or RoleName is placed in a rolesLOV query | Serialize as a single-quoted literal, escape embedded quote per the Fusion query contract before URL encoding, and escape LIKE wildcard characters. If the client's supported escaping cannot express the literal safely, block rather than broaden the search |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROLE.FIND_ROLE | step | 3 | reference_lookup | resolved->PROLE.RESOLVE_CHILDREN;failure->PROLE.RETURN_ISSUES | PROLE.APPLY_DEFAULTS | stop | Resolve role, enterprise role, and use state |
| PROLE.RESOLVE_CHILDREN | step | 4 | reference_lookup | resolved->PROLE.ROUTE_OPERATION;failure->PROLE.RETURN_ISSUES | PROLE.FIND_ROLE | stop | Resolve implementation flag and children; for predefined items resolve type, candidate, active state and target section context before ratings; for explicit keywords skip item/rating lookup |

## Source References and Evidence Limits

Reviewed 2026-10-12 for task `PJF_MANAGE_PROJECT_ROLES`. This maintenance used
the existing catalog identity and task resources, ADE Code Search and central
read-only source files for the two qualification VOs, and the user-supplied UI
reference. No live Fusion lookup, export or import occurred.

### Oracle Lookup Documentation

- [Content types LOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-contenttypeslov-get.html): type identity/name/context metadata.
- [Content items LOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-contentitemslov-get.html): supported word-search/type filters and active-date finder. A search hit alone does not establish project eligibility.
- [Rating levels LOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-ratinglevelslov-get.html): content-item-scoped finder and model/short-description fields. The response does not promise BusinessGroupId or a rating active flag.
- [Profile type sections LOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-profiletypesectionslov-get.html): separate section identity/name/context. This generic resource is not substituted for the project qualification LOV.
- [Roles LOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-roleslov-get.html): enterprise-role read contract; it does not authorize project-role setup writes.

### Indexed Qualification Evidence

Series: `FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64`. Paths below are relative to its
`fusionapps/` root, not files in this FSCR checkout. The two qualification VOs
were read in the central read-only checkout after ADE Code Search; other evidence
remains indexed snippets. Development-series behavior must be reconciled with
the target.

| Source | Returned indexed evidence | Use and limit |
|---|---|---|
| prj/components/projectsManagement/resourceManagement/common/publicView/src/oracle/apps/projects/resourceManagement/common/publicView/QualificationBySectionVO.xml | Line 44 restricts content types to 103,104,106,108,109,110; lines 47-59 apply PJR enterprise implementation and talent-section filters; line 61 uses person profile type 1; line 64 checks current-date item activity; line 65 requires active section; value-set and section joins follow | Explains why a generic HCM item/section pair does not prove Project Roles UI eligibility on its own |
| prj/components/projectsManagement/projectManagement/setup/protectedUiModelProjRole/src/oracle/apps/projects/projectManagement/setup/protectedUiModel/projRole/view/ProjRoleQualificationVO.xml | Lines 47-58 bind QualificationPVO and QualificationBySectionVO. LOV_RequirementName maps Name, ContentItemId, ContentTypeName and ContentTypeId; LOV_RequirementName1 also maps SectionId and SectionName (lines 133-203). The lovSwitcher expression near line 522 selects the section-aware LOV when isFeatureEnabled() is true. Lines 296-297 distinguish keyword display when ContentItemId is null | Requirements display name is sufficient user input for candidate search. Derive Type from the selected result and resolve the target's actual LOV mode before setting SectionName; do not ask for a LOV URL |
| prj/components/projectsManagement/resourceManagement/setup/publicModel/src/oracle/apps/projects/resourceManagement/setup/publicModel/entity/ProjRoleQualificationEO.xml | Lines 543/548 validate Keyword or ContentItemId presence | Keyword-only is supported by the entity; do not require a predefined Name for that form or auto-convert unresolved names |
| prj/components/projectsManagement/projectManagement/setup/protectedUiModelProjRole/src/oracle/apps/projects/projectManagement/setup/protectedUiModel/projRole/view/ProjRoleQualificationVORowImpl.java | Lines 216/221 describe entered requirements initially treated as keywords and changes from predefined requirements; line 298 clears Keyword | Do not duplicate a selected content-item name into Keyword; exact CSV representation remains a target package check |
| hcm/components/hcmCoreSetup/profiles/restModel/src/oracle/apps/hcm/profiles/restModel/lov/view/RatingLevelVO.xml | Lines 87/91 contain business-group association attributes; lines 548 and 623-626 declare findByContentItemId | Internal business-group attributes are not a public GET response contract. Keep target/session context and model validation; do not invent an exposed field or claim full UI parity |

For a requirement already used on another role, the fresh same-target task
export is reusable section evidence when it yields one exact item/type/section.
For an item absent from that export, the section-aware UI remains the authority
for a new section because no public Project Roles Requirements LOV GET endpoint
was established by this review. The UI view is an ADF binding, not a public REST
URL. The public HCM content-item lookup resolves and verifies item identity but
does not reproduce Project Resource Management section eligibility. The image
shows a Hindi value in the main table; it does not prove the current target's
item ID or section until a fresh export or target selection is inspected.
