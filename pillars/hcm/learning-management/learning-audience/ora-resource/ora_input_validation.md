# Learning Audience Input Validation

Shared functional-area resources for hcm.learning-management.learning-audience.
Each table row belongs only to its exact task code and task name. Runbooks own
intake, payload construction, processing, and writes. This package records
known source facts and unresolved contracts; neither task is execution-ready.

## Sources and Identity

- [Approved taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-taxonomy/); identity and membership reconciled against the [effective catalog](../../../../../knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json) on 2026-09-23: offering ORA_LEARNING_MANAGEMENT, functional area ORA_LEARNING_AUDIENCE, and the two unchanged CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA and CUSTOM_MANAGE_USER_GROUPS tasks. This catalog reconciliation is not a fresh retrieval of the live taxonomy page.
- Earlier [baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-guide-skill-baseline/), reviewed 2026-09-16: HCM Filtered Lists is the shared prerequisite. OLC-116680 and priority P1 are historical baseline metadata, not current provider-readiness evidence; see ora_dependency_readiness.md for ownership and unresolved contracts.
- The canonical repository identity is hcm.learning-management.learning-audience, derived from the effective catalog's Learning Management offering. Use this identity consistently in routing, dependency graphs, validation, and project state.
- For resource paths in this file, `{coreProductRestApiVersion}` means the value of `REST_API_VERSION` owned by `core/data-loader/scripts/rest_sample_data.py`. Resolve it from core.data-loader; do not define a task-local version literal.
- [WLF_LEARNING_ORGANIZATIONS_F](https://docs.oracle.com/en/cloud/saas/human-resources/oedmh/wlflearningorganizationsf-31279.html): storage structure for learning organizations.
- [WLF_HCM_LIST_ITEMS](https://docs.oracle.com/en/cloud/saas/human-resources/oedmh/wlfhcmlistitems-8690.html): extracted list items, not the criteria-definition schema or an API payload contract.
- Developer-supplied Postman request, reviewed 2026-09-16: Create Learning Item List, POST /hcmRestApi/resources/{coreProductRestApiVersion}/hcmLists, REST-Framework-Version: 9. It supplies seven string-valued fields and three filter forms. No response, schema, requiredness, size limits, lookup contract or permission evidence was supplied. This is request-shape evidence, not proof of successful creation or a complete Oracle API specification.
- The developer confirmed hcmLists as the core.data-loader business object, matching the supplied REST collection name. This name correction does not authorize a direct REST executor. Local skill authoring does not establish local validation authority.
- Developer-supplied learningOrganizations /describe response, reviewed 2026-09-21: versioned resource /hcmRestApi/resources/{coreProductRestApiVersion}/learningOrganizations. It establishes the REST attributes, required input flags, mutability, finders, advertised methods, child links and reconcile action recorded below. The source host is environment-specific and is intentionally not retained.
- Developer-supplied lookup identities, reviewed 2026-09-21: status uses ORA_WLF_LEARN_ORG_STATUS, visibilityESS uses ORA_WLF_ORG_ESS_VISIBILITY, and criteria sourceType uses ORA_WLF_ORG_PER_CRITERIA_TYPE. These names identify the authoritative lookup types but do not by themselves enumerate allowed codes or establish the lookup read contract.
- Developer-directed participant-person resolution, reviewed 2026-09-21: when a participant person is supplied as a Fusion Username instead of sourceId, resolve it through core.fusion-api.rest-api-client with an exact userAccounts.Username query. A unique returned PersonId becomes participantCriteria.sourceId and participantCriteria.sourceType is set to ORA_PERSON. Username is an account identifier; this contract does not authorize a fuzzy display-name search.
- Developer-supplied LearningOrgRelManageCriteriaE1 query, reviewed 2026-09-21: for CRITERIA_SOURCE_TYPE ORA_PERSON, CRITERIA_SOURCE_ID joins to HCM person_id and is used to derive display name, person number, email and department context. This is storage-mapping evidence only; it is not an executable SQL route or a Username resolver.
- Live Data Loader metadata generated learningOrganizations, managerCriteria and participantCriteria worksheets. That loader contract establishes import sections and loader linkage columns; it does not replace the REST /describe contract or make every REST child a registered loader section.
- Developer-directed create handling, reviewed 2026-09-21: for a new learningOrganizations Data Loader row, omit learningOrganizationId and learningOrganizationNumber because Fusion generates them, and do not require status. A returned or resolved learningOrganizationNumber may identify an existing group for later work, but it is not a caller-supplied create value.

## Source Scope

| Task Code | Task Name | Resource Name | Redwood Route | Catalog Support |
|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | /hcmLists | redwood/learning-criteria-lists/main/manage-learning-criteria-lists | Custom catalog entry; available Y; export/import N; CSV export/import N |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | /learningOrganizations | redwood/learning-resources/main/manage-user-groups | Custom catalog entry; available Y; export/import N; CSV export/import N |

The routes above are source references, not executable requests. REST Data
Loader metadata names hcmLists and learningOrganizations; registration still
requires verification through the selected Data Loader workflow. The baseline
requests registration and does not prove that it has occurred. The
learningOrganizations /describe response exposes managerCriteria and
participantCriteria as separate one-to-many child collections. It also exposes
managerPersonList, participantPersonList, whereUsed, and a nested
personListAttachment resource; those additional REST resources are not present
as sections in the supplied Data Loader template and must not be treated as
loader-supported sections without live loader metadata.

## REST Operation Contract

The actions below are capabilities advertised by the supplied /describe
response. They define validation boundaries only; they do not select a live
execution route or satisfy its identity, privilege, approval, concurrency, or
verification gates. Every advertised upsert action is POST with
`Upsert-Mode=true`.

For this task, create and update operations use core.data-loader by default.
Put POST or PATCH in the validated loader artifact's RestAction column. The task
metadata value `dataloader_import_mode: REST` identifies the Data Loader
transport and does not by itself authorize direct REST mutation. The only
exception is the documented existing-parent criteria-create fallback after the
Data Loader registration mismatch is proven and the user explicitly requests
it. That fallback uses the core Fusion REST client for one separately approved
managerCriteria or participantCriteria collection POST to the exact resolved
composite parent; it does not permit a root mutation or criterion PATCH without
an existing criteriaId.

| Task Code | Task Name | Resource | Relationship | Advertised Collection Actions | Advertised Item Actions | Execution Boundary |
|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | learningOrganizations | Root resource | GET; POST create; POST upsert | GET; PATCH; DELETE; POST reconcile | Registered template root; execute only through the selected core.data-loader workflow |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | managerCriteria | One-to-many child; ManagerRelationId maps to RelationId | GET; POST create; POST upsert | GET; PATCH; DELETE | Supplied Data Loader template section. Use core.data-loader by default; the documented registration-mismatch fallback permits one separately approved collection POST to the exact composite parent |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | participantCriteria | One-to-many child; ParticipantRelationId maps to RelationId | GET; POST create; POST upsert | GET; PATCH; DELETE | Supplied Data Loader template section. Use core.data-loader by default; the documented registration-mismatch fallback permits one separately approved collection POST to the exact composite parent |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | managerPersonList | Child resource | GET | GET; PATCH | Not present in the supplied Data Loader template; do not infer loader support |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | participantPersonList | Child resource | GET | GET; PATCH | Not present in the supplied Data Loader template; do not infer loader support |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | whereUsed | Child resource | GET; POST create; POST upsert | GET; PATCH; DELETE | Not present in the supplied Data Loader template; advertised REST actions are not an execution route |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | personListAttachment | Nested child of participantCriteria | GET; POST create; POST upsert | GET; PATCH; DELETE | Not present in the supplied Data Loader template; attachment handling requires its own documented workflow |

Release/build is optional context for both tasks. Do not ask for it as a
prerequisite; use authoritative capability evidence for feature-specific checks.
The core-owned REST API version is a technical routing value, not a requested
application release.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Supplied learning-item list fields | Name, Description, Criteria, Active, Subscriber, ObjectName, ListScope; all strings in the supplied create example | Do not silently drop, invent or default a supplied field; authoritative requiredness remains TBD | Validate field mapping and operation requirements through core.data-loader live metadata after project prerequisites pass | Creating a learning-item list from the developer-supplied request shape | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Criteria representation | Criteria is a JSON string whose decoded value is an object containing filters | Block on malformed JSON or a changed string/object representation; full supported grammar remains TBD | Preserve the supplied structure; obtain the provider grammar and validation authority before treating syntax checks as complete task validation | Creating a learning-item list with Criteria | TBD |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | User-group loader create fields | visibilityAdministrator and visibilityESS; title and description when supplied | Ask the user for each unresolved loader-required input by name and state its accepted form; preserve completed inputs and resume validation after the reply | Omit learningOrganizationId, learningOrganizationNumber and status for POST; Fusion supplies or manages them. Validate the remaining fields through core.data-loader live metadata | Creating a user group through core.data-loader |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Existing user-group identity | learningOrganizationId or learningOrganizationNumber; SysEffectiveDate is an optional finder input | Ask the user for learningOrganizationId or learningOrganizationNumber and the intended operation; preserve the current run and resume the same resolver after the reply | Run resolve_learning_user_group with the supplied identifier and operation intent | Updating, deleting, reconciling or reading children of an existing user group | resolve_learning_user_group |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Manager criteria create fields | managerCriteria section with sourceId and sourceType | Ask the user for the missing manager sourceId or sourceType; do not reuse participantCriteria or invent a relation identifier | Preserve the managerCriteria section and let the selected Data Loader workflow validate its live linkage fields | Creating manager criteria |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Participant criteria create fields | participantCriteria section with sourceId and sourceType; alternatively an exact Fusion Username or an explicitly identified PersonId as a pre-load person reference | Ask for the exact Username, a PersonId, or the missing sourceId and sourceType for a non-person criterion; preserve the participant role | Select the branch from user input: name/Username uses resolve_participant_person_by_username; PersonId uses validate_criteria_person_id. If both were independently supplied without an explicit selection, ask which to use; neither takes precedence and no conflict comparison is required. A resolver-derived PersonId is output, not a second user input. Non-person sources retain their own sourceType validation | Creating participant criteria |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Existing criteria identity | Resolved parent learningOrganizationId, exact child role, and criteriaId | Ask the user for the missing parent identifier, exact child role, or criteriaId; preserve the requested operation and resume after the reply | Run resolve_learning_user_group_criteria after resolving the parent group | Updating or deleting existing manager or participant criteria | resolve_learning_user_group_criteria |

## Field Validation

The learning-item list checks below describe the supplied request shape, not
global API requirements or exhaustive enums. Their authority remains unresolved
in the canonical Resolver cells. User-group REST checks come from the supplied
/describe response. Database columns remain background storage evidence and do
not override REST names, requiredness or mutability.

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Supplied field types | Preserve Name and Description as strings; preserve Active, Subscriber, ObjectName and ListScope as strings without coercion. Limits, requiredness and complete enums: TBD | Reviewing the supplied learning-item list create shape | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Supplied discriminator values | The example supplies Active Y, Subscriber ORA_WLF_SKILLS_LIB_TRAINING, ObjectName LEARNING_ITEMS and ListScope PUBLIC; these are supplied values, not defaults or an exhaustive allowed-value list | Reviewing the supplied learning-item list create shape | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Criteria JSON string | Decode the outer JSON, then parse the Criteria string once for inspection; retain Criteria as a string in the outgoing representation. Do not convert it to an object or apply blanket unescaping to string values | Reviewing the supplied Criteria representation | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Criteria filters shape | The supplied decoded object contains a filters array of objects with string name and operator fields. Preserve filter order and values; the example does not establish logical combination semantics or a complete filter schema | Reviewing the supplied Criteria representation | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Learning-item number filter | Supplied form: name learningItemNumber, operator is_not_one_of, terms an array of strings. Preserve every term and its order; do not infer that excluded terms must exist | When that supplied filter form is present | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Learning-item type filter | Supplied form: name learningItemType, operator is, terms an array containing ORA_COURSE. Do not infer other type codes, operators or cardinality rules | When that supplied filter form is present | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Learning-item creation-date filter | Supplied form: name learningItemCreationDate, operator is_not_range_between, from and to date strings in YYYY-MM-DD form. Preserve equal endpoints; inclusivity, timezone and equal-range semantics are TBD | When that supplied filter form is present | TBD |
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Embedded date preservation | Dates inside Criteria belong to the JSON string, not separate loader Date attributes; do not rewrite them merely to follow a loader column date format | Mapping Criteria to a confirmed string-valued loader attribute | TBD |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Root identifier handling | learningOrganizationId is a string-form BigInt with precision 18, is create-only, and has a default-value expression. Omit it for POST. Existing-record operations resolve ID or number through resolve_learning_user_group; never apply that lookup to a not-yet-created parent | Creating or identifying a user group |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Root create ownership | Although /describe marks learningOrganizationNumber and status inputRequired for the REST resource, the developer-directed Data Loader POST contract omits learningOrganizationId, learningOrganizationNumber and status. Do not ask the caller to invent them or place them in the create artifact; capture returned server values for later identity and verification | Creating a user group through core.data-loader |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Root visibility strings | visibilityAdministrator and visibilityESS are strings with precision 30 and allow changes. Validate them in the loader artifact for create or update | Creating or updating a user group through core.data-loader |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Administrator visibility value | visibilityAdministrator accepts ORA_PRIVATE or ORA_OPEN according to its /describe annotations; reject any other value before preview | Validating visibilityAdministrator |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Self-service visibility value | visibilityESS is LOV-backed by ORA_WLF_ORG_ESS_VISIBILITY. Resolve the supplied code or explicit business meaning through the core lookup route defined in ora_reference_lookups.md; require a uniquely matched enabled/effective code. Codes are runtime evidence, not hardcoded defaults | Validating visibilityESS | resolve_learning_organization_ess_visibility |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Status value | For POST omit status under the developer-directed Data Loader contract. Validate a supplied status for existing-record work through ORA_WLF_LEARN_ORG_STATUS; allowed codes and the authoritative read contract remain unresolved | Validating a supplied status for an existing user group | resolve_learning_organization_status |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Optional root values | title is a string up to 250 characters; description is a string up to 4000 characters; reconcilePriority is a string with precision 30; reconcileStartDate and reconcileEndDate are datetimes | When the corresponding optional value is supplied |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Root response-only values | Do not accept creationDate, lastModifiedDate, reconcileLastRunProcessId, reconcileLastRunProcessDate, processingStatus, statusMeaning, whereUsedCount, participantsCount, createdByDisplayName, lastModifiedByDisplayName, processingStatusMeaning, visibilityESSMeaning or visibilityAdministratorMeaning as caller-managed values; /describe marks them allowChanges never | Reviewing a request or loader mapping that supplies response fields |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Manager criteria required values | managerCriteria requires sourceId as a string-form BigInt with precision 18 and sourceType as a create-only string with precision and maximum length 30 | Creating managerCriteria |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Participant criteria required values | The final participantCriteria create row requires sourceId as a string-form BigInt with precision 18 and sourceType as a create-only string of maximum length 30. Resolve the supplied or user-selected name/Username, or validate the supplied or user-selected PersonId; do not select one automatically when both were independently supplied. Non-person sources follow their own mapping and lookup rules | Creating participantCriteria |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Criteria generated identifiers | criteriaId and createdById have default-value expressions. Omit generated identifiers for create; do not invoke existing-child resolution for a new row. Updating or deleting a criterion requires criteriaId and resolve_learning_user_group_criteria under the exact parent and role | Creating, updating or deleting a criterion |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Criteria source type | sourceType is required in final create rows and is create-only. For an explicitly identified person input, the declared mapping sets ORA_PERSON after Username or ID-only validation. Validate other user-supplied sourceType codes through the named lookup. Do not change sourceType through PATCH or silently recreate the criterion | Validating managerCriteria or participantCriteria | resolve_learning_organization_criteria_source_type |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Participant person Username mapping | The documented name resolver accepts exact Fusion Username, not a fuzzy display name; request the exact Username if needed. When name/Username is the supplied or user-selected input, resolve PersonId with ORA_PERSON and show the mapping in preview. Do not compare against another input or apply precedence. Never use UserId, PersonNumber, AssignmentId or Username as sourceId | A participantCriteria person's supplied or selected input is Fusion Username | resolve_participant_person_by_username |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Criteria optional writable values | sourceDisplayName is a string with precision 250; reportName and reportPath are strings with precision 255. Preserve them only when supplied and valid for the selected sourceType | Creating or updating either criteria child |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Criteria response-only values | Do not accept createdByDisplayName, sourceTypeMeaning, personDepartmentId, personDepartment or sourceNumber as caller-managed values; /describe marks them allowChanges never | Reviewing either criteria child |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Person-list collection boundary | managerPersonList and participantPersonList advertise collection GET but not collection create. Do not translate criteria or loader rows into person-list creates; item PATCH remains outside the selected Data Loader route unless a separate workflow documents it | A request attempts to create materialized manager or participant rows |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | REST and Data Loader effective dates | The supplied REST /describe attributes do not include EffectiveStartDate, EffectiveEndDate or effectiveOf, while the live Data Loader template does. Validate those loader columns only through core.data-loader live metadata and do not invent REST effective-date fields | Preparing or validating a Data Loader workbook |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Loader child linkage | The Data Loader template supplies learningOrganizationId and RestAction on managerCriteria and participantCriteria even though those are not child attributes in the REST /describe response. Preserve the live loader headers and let core.data-loader validate parent-child keys; do not copy loader-only columns into a direct REST body | Mapping or validating managerCriteria or participantCriteria loader sheets |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Existing effective-dated parent context | Preserve the exact returned `@context.key`. If a child-only load and a parent-PATCH-plus-child load both fail with object-level `Not Found`, while the numeric item route fails and the returned composite item route succeeds, classify a Data Loader registration mismatch and stop loader retries. Only on an explicit user request may the documented direct-child fallback proceed: use collection POST, not PATCH, because no criteriaId exists; re-run parent, person and duplicate resolution; then require approval for the exact environment, composite child path and JSON body | Creating managerCriteria or participantCriteria under an existing effective-dated user group after a demonstrated loader registration mismatch | resolve_learning_user_group |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Mutation route | Use core.data-loader for supported root and criteria creates or updates. The only direct REST mutation exception is an explicitly requested managerCriteria or participantCriteria collection POST after the existing-parent Data Loader registration mismatch is demonstrated as defined above. Root mutations and criterion PATCH or DELETE remain outside this fallback | Preparing a create or update |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | ID-only person validation | Validate decimal integer shape and precision without floating-point conversion, then resolve actual person identity through the named core-client resolver. Notify the user of invalid input or returned identity mismatch and request correction; never substitute another person. Unverified or inaccessible identity is not a confirmed invalid ID | A person criterion's supplied or selected input is PersonId/sourceId | validate_criteria_person_id |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Proposed criteria duplicates | Compare the final resolved source identity for every row in the same proposed parent and exact role, including rows within one new-parent request. Reject repeated create tuples or conflicting same-criteriaId updates; ask which row to skip/correct. Do not treat manager and participant roles as interchangeable | Preparing a criteria create or update |  |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Existing-parent criteria duplicates | Check the exact existing parent and role before preview; merge unchanged source fields for PATCH and exclude only the criterion being updated. A new parent uses in-request validation before create and returned-state verification afterward, not an existing-parent pre-create lookup | Preparing criteria changes under an existing parent | check_duplicate_learning_user_group_criteria |

The /describe response establishes only the default-value expressions stated
above; it does not reveal the generated values. Nullable database columns do
not establish API optionality, and no database-to-REST name transformations are
generated.

For criteria creation, WLF_HCM_LIST_ITEMS remains background storage evidence:
HCM_LIST_ITEM_ID is the primary key; HCM_LIST_ID and ITEM_ID are non-null
NUMBER(18); SOURCE_TYPE is VARCHAR2(30), ITEM_TYPE VARCHAR2(50), JOB_ID NUMBER(18),
and IS_PROCESSED VARCHAR2(1). These extracted-item columns are not additional
list-definition inputs, and their REST mapping is not a prerequisite to creating
the supplied list definition. No extracted membership is created by these rules.

## Task Nodes

Rule ID allocation is task-specific: LAC identifies Learning Audience Criteria;
LUG identifies Learning User Groups. Each task uses VALIDATE_INPUT (10),
RESOLVE_REFERENCES (20), CHECK_DEPENDENCIES (30), CHECK_DESIGN (40),
EXECUTION_GATE (50), RETURN_VALIDATED (60), HANDLE_ERROR (90), and RETURN_ISSUES
(100). Explicit task-scoped success terminals keep the graph self-contained.
These are authoring validation gates, not a Fusion write
sequence or an order between the two tasks.

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | LAC.VALIDATE_INPUT | step | 10 | validate_input | valid->LAC.RESOLVE_REFERENCES;invalid->LAC.HANDLE_ERROR | none | stop | Every criteria request after the input contract and validation authority are resolved |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | LUG.VALIDATE_INPUT | step | 10 | validate_input | valid->LUG.RESOLVE_REFERENCES;invalid->LUG.HANDLE_ERROR | none | stop | Every user-group request after the input contract and validation authority are resolved |
