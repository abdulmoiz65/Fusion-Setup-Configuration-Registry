# Manage Project Templates REST Contract Reference

## Purpose and Authority

Before executing any request described here, apply the offering's
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
through the selected task workflow. Resolve the core client/workflow's framework
version before constructing query parameters and verify its outgoing header;
this reference does not select a framework version or authorize execution.

This is the published REST contract reference for
`PJF_MANAGE_PROJECT_TEMPLATES`. It is static API/field reference material,
not an execution authority or runtime adapter. The task manifest declares
delegation requirements; its allowed ora-resource rule graph owns validation,
dependency, reference, design and error gates. The active workflow owns payload
preparation, approval and writes through the selected core executor.
The public authority is Oracle Project Management REST API, `Project Templates`:
`https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/api-project-templates.html`.
Use the target release's equivalent operation schema when it differs from that
published release. Do not derive a JSON payload from application-page labels.

For executable root create, intersect the versioned published POST contract
with fresh target operation metadata. Target metadata may narrow fields, types,
or lengths. Required fields beyond the published groups need fresh operation-specific
target POST evidence; generic describe required/mandatory flags and historical
runtime errors do not make currency or external task IDs mandatory. Neither generic `updatable` metadata nor a
runtime error authorizes a field absent from the published operation contract.
Oracle's generated schema uses `required`, `nullable`, `default`, dependency
hints, and prose alternatives inconsistently. Treat `nullable: false` as a
nullability rule, not by itself as proof that the client must send the field.
Collapse a documented name/ID required pair into one required representation.

## Root Resource Contract

| Surface | Published contract | Consultant rule |
|---|---|---|
| Template collection | GET or POST `/fscmRestApi/resources/11.13.18.05/projectTemplates` | GET is for current identity/baseline discovery. POST uses only the published root create schema. |
| Template item | GET or PATCH `/fscmRestApi/resources/11.13.18.05/projectTemplates/{projectTemplatesUniqID}` | `projectTemplatesUniqID` is a server-returned item key. Obtain the item URI from a fresh response `self` link; never construct it or replace it with `ProjectTemplateId`. |
| Root delete | No published DELETE | Unsupported. An end date is a PATCH only when `ProjectTemplateEndDate` is writable in the target schema. |

Collection reads must be fully paginated before concluding identity or absence.
For an item or post-create child operation, use fresh returned canonical links;
never substitute a numeric ProjectTemplateId for projectTemplatesUniqID. A
requested child read uses the documented collection/item path below and the
returned parent/child identity. An omitted response field is unknown evidence,
not proof that an existing value was preserved. The read-only acquisition
mechanics remain owned by ora_reference_lookups.md.

## Core Request Field Contract

| Canonical REST field | Recognized input label | Contract |
|---|---|---|
| `ProjectTemplateName` | `TemplateName` | Template name. It is a published create-required field. |
| `ProjectTemplateNumber` | `TemplateNumber` | Template number. Send only as the published create/update schema permits. |
| `ProjectTemplateDescription` | `Description` | Template description. |
| `BusinessUnitName` or `BusinessUnitId` | `BusinessUnit` | Supply one documented name/ID representation; do not send conflicting alternatives. A customer-supplied name is a valid executable value. |
| `ProjectUnitName` or `ProjectUnitId` | `ProjectUnit` | Supply one documented representation. The published root schema names `ProjectUnitName` as required while its example uses `ProjectUnitId`; interpret this as one required representation, not a literal name-only requirement. |
| `OwningOrganizationName` or `OwningOrganizationId` | `Organization` | Supply one documented name/ID representation. A supported name passes directly to Fusion POST. |
| `ProjectTypeName` or `ProjectTypeId` | `ProjectType` | Supply one documented name/ID representation. A supported name passes directly to Fusion POST. |
| `ProjectPlanType` or `ProjectPlanTypeId` | `ProjectPlanTypeName`, `PlanType`, `PlanTypeName` | Normalize a supplied plan-type name to canonical `ProjectPlanType`, or use `ProjectPlanTypeId` when an exact target ID was independently resolved. Supply one representation only. `ProjectPlanTypeName` is an input alias and must never be serialized. |
| `LegalEntityName` or `LegalEntityId` | `LegalEntity` | Supply one documented name/ID representation. Legal-entity eligibility is dependent on business-unit context and is validated by Fusion POST. |
| `InitialProjectStatus` | `InitialStatus`, `IntialStatus` | Initial project status name. `IntialStatus` is accepted only as an input-label correction and is shown as a normalization in the preview. |
| `InitialProjectStatusCode` | `InitialStatusCode` | Initial project status code. Do not invent a code from a supplied status name. |
| `ProjectTemplateStartDate` | `FromDate`, `StartDate` | ISO `YYYY-MM-DD` date only. |
| `ProjectTemplateEndDate` | `ToDate`, `EndDate` | ISO `YYYY-MM-DD` date only; use only when the target PATCH schema exposes it. |
| `ProjectStartDate` | exact canonical field only | Governing project schedule start for dated nested tasks; ISO `YYYY-MM-DD`. Do not derive it from template availability. |
| `ProjectEndDate` | exact canonical field only | Governing project schedule end for dated nested tasks; ISO `YYYY-MM-DD`. Do not derive it from template availability. |

All other root fields are accepted only when their exact canonical REST name is
present in the target operation schema. A display label, a value visible in an
application page, or a field returned read-only is not a writable-field contract.
In particular, do not infer a `Name` suffix from neighboring references:
`ProjectPlanTypeName` is not a Project Templates request attribute.

## Create Requirement Classification

| Classification | Requirement |
|---|---|
| Published root required | `ProjectTemplateName` and one `ProjectUnitName`/`ProjectUnitId` representation. Oracle's generated schema lists the name while its example uses the ID. |
| FSCR deterministic create identity | Nonblank `ProjectTemplateNumber`, even though Oracle's generated root `required` array omits it. |
| FSCR complete business context | One name/ID representation for business unit, project unit, owning organization, project type, and legal entity. This is a completeness overlay, not proof that Oracle's generated `required` array lists every field. |
| Target-operation required | Additional writable fields explicitly marked required/mandatory by fresh operation-specific target POST metadata; collapse documented name/ID alternatives. Generic describe/read/response required flags, audit fields, generated IDs and nullable=false do not establish create requirements. |
| Nested/direct Task prepared-payload required | TaskName and both cross-charge flags after evidenced inheritance. Nested task organization may remain omitted for Fusion derivation; supplied alternatives and fresh operation-specific requirements still validate. Direct-create organization requirements remain separate. |
| External task identifiers | Oracle requiredness remains operation-specific. FSCR nested-create preparation preserves supplied valid IDs and generates missing IDs under ora_defaulting_rules.md; supplied IDs remain nonblank and unique. Existing evidenced work-type prerequisites remain separate. |
| Schedule consistency | Validate supplied start/finish ordering. FSCR checks task dates against known project schedule bounds; task dates alone do not make optional project dates mandatory. |
| Defaults and project-type derivation | See the task's ora_defaulting_rules.md for omitted flags, task organization, asset-line mode and project-type-derived omissions. Currency may remain omitted unless fresh operation-specific POST metadata proves it required. |

## Published Child Resource Contract

`{template}` below means the canonical template item URI returned by REST. Do
not compose it from a numeric ID. A child item URI must likewise be taken from a
fresh child response `self` link.

| Child family | Collection relative to `{template}` | Child key in documented item path | Create | Read | Update | Delete |
|---|---|---|---|---|---|---|
| Project classifications | `/child/ProjectClassifications` | `ProjectClassificationId` | POST collection | GET collection/item | PATCH item | DELETE item |
| Project customers | `/child/ProjectCustomers` | `ProjectPartyId` | POST collection | GET collection/item | Not published | Not published |
| Project team members | `/child/ProjectTeamMembers` | `TeamMemberId` | POST collection | GET collection/item | PATCH item | DELETE item |
| Project transaction controls | `/child/ProjectTransactionControls` | `ProjectTransactionControlsUniqID` | POST collection | GET collection/item | Not published | Not published |
| Provider business units | `/child/ProviderBusinessUnits` | `BusinessUnitId` | POST collection | GET collection/item | Not published | DELETE item |
| Quick entries | `/child/QuickEntries` | `QuickEntryId` | POST collection | GET collection/item | Not published | Not published |
| Setup options | `/child/SetupOptions` | `OptionCode` | POST collection | GET collection/item | PATCH item | Not published |
| Tasks | `/child/Tasks` | `TaskId` | POST collection | GET collection/item | PATCH item | DELETE item |
| Task transaction controls | `/child/Tasks/{TaskId}/child/TaskTransactionControls` | `TaskTransactionControlsUniqID` | POST collection | GET collection/item | Not published | Not published |

For every child POST or PATCH, the exact body is the published operation-specific
JSON schema for that family and method. The skill must reject an unknown child
field, read-only field, or unsupported verb. It must not translate an
application label into a child JSON field unless the mapping is in this resource
or supplied by the target schema.

The root create schema also publishes nested child arrays for project
classifications, project customers, project team members, project transaction
controls, provider business units, quick entries, setup options, and tasks.
Use a nested array only when every field in that exact root-create child schema
is validated. Otherwise create the root first, re-read it, then use documented
direct child operations in the approved order. Do not assume that a nested child
array provides an incremental update or delete route.

For nested `Tasks`, the published root POST schema formally requires `TaskName`,
`TaskOrganizationId`, `CrossChargeLaborFlag`, and `CrossChargeNonLaborFlag`, while
the same contract documents `TaskOrganizationName` as the alternative to the ID.
Nested template create preserves an explicit task-organization representation, or
leaves both alternatives omitted for Fusion derivation. Successful target response
and canonical task readback supplied on 2026-10-14 evidence this behavior; the
published required array remains unchanged. Fresh operation-specific requirements
still apply. Direct task create retains explicit/evidenced organization preparation. For an
explicit name subject to a genuinely ID-only target operation, use a proven
standalone exact-match resolver; never use another template's contextual LOV.
ExternalTaskId remains optional in the published schema; FSCR now generates omitted
nested-create IDs under its defaulting policy. Preserve supplied IDs and parent relationships;
do not infer requiredness from generic describe or a historical failure.
TaskNumber, TaskStartDate and TaskFinishDate remain optional. If any task date
is supplied, validate its ISO format and supplied start/finish order. Task dates
do not independently make omitted project dates mandatory. Check known project
bounds as an FSCR consistency overlay; availability dates are not substitutes.
A zero-result collection GET cannot return a future template item or Tasks-child
link; their absence is not a create-route coverage failure.

REST boolean fields use JSON boolean literals. Human yes/no or Y/N input must be
normalized before preview; quoted `"Y"`/`"N"` values are not valid serialized
booleans even when a target might coerce them.

Before approval, validate the exact JSON with
`scripts/validate_project_template_payload.py` and fresh target operation
metadata. The immutable body and preview bind to prepared_payload_sha256;
retain the source payload and metadata hashes in the preparation record.
The validator enforces actual operation-required fields
and dated-task project schedule bounds. Fusion POST remains authoritative for
supplied reference eligibility.

## Reviewed 26C Operation Constraints

The local [request-constraint snapshot](project-template-operation-contracts.json)
records the reviewed POST/PATCH request fields, types, nullability, lengths,
explicit required arrays, nested references and source URL for each operation.
It contains request constraints only. The validator uses it independently of
target describe data, then applies narrower operation-specific target evidence.
Nullable=false rejects an explicit null; it does not require an omitted field.
Documented nullable fields may be explicitly cleared where the selected target
PATCH contract permits it. Omitted PATCH values remain unchanged.

| Surface | Reviewed request rule | Oracle 26C source |
|---|---|---|
| Root | POST/PATCH fields differ. Root POST does not publish the cost-code reference-set fields previously allowed by the skill. Currency/work type are absent from its required array; capitalization and asset-allocation omissions retain project-type derivation | [Root POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-post.html), [Root PATCH](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-patch.html) |
| Classifications | Category name/ID and class-code name/ID alternatives; percentages are 0..100. Category-specific sum requirements need target evidence. PATCH does not publish category reassignment | [Classification POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-projectclassifications-post.html) |
| Customers | Use one PartyId, PartyName or PartyNumber; CustomerId and ProjectPartyId are not request fields. Oracle prose swaps the name/number descriptions; preserve canonical field names and verify target eligibility | [Customer POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-projectcustomers-post.html) |
| Team members | PersonEmail/PersonId/PersonName and ProjectRoleName/ProjectRoleId are POST representations. Resource percentage/rate fields are documented; they do not authorize a ProjectResourceName field. PATCH omits person and role fields | [Team-member POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-projectteammembers-post.html), [Team-member PATCH](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-projectteammembers-teammemberid-patch.html) |
| Project/task controls | POST only as direct operations; documented code/hint alternatives remain strings. Person/job/organization prerequisites are explicit. StartDateActive derives from project start; do not invent a date or require every nullable=false field in the body | [Project-control POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-projecttransactioncontrols-post.html), [Task-control POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-tasks-taskid-child-tasktransactioncontrols-post.html) |
| Provider business units | One supported BU name/ID; direct POST/DELETE, no PATCH | [Provider-unit POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-providerbusinessunits-post.html) |
| Quick Entries | Ten documented FieldCode values. MandatoryFlag defaults false. Specification applies only to TEAM_MEMBER/CLASSIFICATION and is mandatory for those codes; preserve the target-valid role/category specification | [Quick-entry POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-quickentries-post.html) |
| Setup Options | POST accepts OptionName or OptionCode and DisplayFlag; direct PATCH accepts DisplayFlag only. No documented mapping proves that an arbitrary outline-display UI label is a setup-option code | [Setup-option POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-setupoptions-post.html), [Setup-option PATCH](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-setupoptions-optioncode-patch.html) |
| Tasks | Cross-charge booleans inherit project/parent-task values. Task organization has name/ID alternatives. Omitted nested task organization stays omitted for Fusion derivation and readback; direct-create preparation remains separate. ExternalTaskId is optional in Oracle's schema; FSCR fills omitted nested-create IDs by its declared defaulting policy. Target create evidence shows ExternalTaskId becoming the saved TaskNumber. Target PATCH evidence shows changing TaskNumber also changes ExternalTaskId. Preview both business values, do not promise independent preservation, and verify both fields after execution. TaskSequence/ParentTaskId/LowestLevelTask are not create fields. TaskId appears in the request schema without explaining caller assignment; FSCR blocks caller TaskId creation pending explicit target evidence | [Task POST](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-tasks-post.html), [Task PATCH](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-child-tasks-taskid-patch.html) |
| Nested operations | Root/task POST publish nested controls. Root PATCH publishes nested field schemas but does not establish row binding for this reviewed profile; nested PATCH remains blocked pending reviewed operation-specific binding evidence. Plan supported direct-child operations before approval instead. A customer nested PATCH has an empty schema; it authorizes no customer-field update | [Root PATCH](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/op-projecttemplates-projecttemplatesuniqid-patch.html) |

### Display Names for Code-Only Fields

These are explicit FSCR input aliases, not API fields. The reference-lookup
resource owns acquisition, exact matching, eligibility and ambiguity behavior.
Preserve the supplied name in resolution evidence, emit only the canonical code,
and validate that code against the documented field values. Existing API name
or hint alternatives pass directly without an invented ID/code resolver.

| Input alias | Canonical code field | Documented lookup type / evidence boundary |
|---|---|---|
| ProjectPriority / ProjectPriorityName | ProjectPriorityCode | PJF_PROJECT_PRIORITY_CODE is confirmed by user-supplied target response evidence on 2026-10-14, though not named in the Project Templates 26C field description. Confirm availability for each execution target |
| AssetAllocationMethod | AssetAllocationMethodCode | PJC_ASSET_ALLOCATION_METHOD, named in root POST description |
| CurrencyConvDateType | CurrencyConvDateTypeCode | PJF_DEF_RATE_DATE_CODE, named in root POST description |
| PercentCompleteCalculationMethod (task input) | PercentCompleteCalculationMethodCode | PJF_PERCENT_COMP_METHOD, named in task POST description |
| ProgressETCMethod (task input) | ProgressETCMethodCode | PJF_ETC_METHOD, named in task POST description |

The [common 26C lookup GET](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-standardlookups-lookuptype-child-lookupcodes-get.html)
documents lookup codes, meanings, string EnabledFlag, effective dates, q and
pagination. A route alone does not prove type availability or its path key.
The user-supplied response on 2026-10-14 confirms the literal
`PJF_PROJECT_PRIORITY_CODE` key through its collection self-link under
`/fscmRestApi/resources/11.13.18.05/standardLookups/`. For
`q=Meaning='High'&onlyData=true`, it contains one item with `Meaning=High`,
`LookupCode=HIGH`, `EnabledFlag=Y`, `StartDateActive=1951-01-01`,
`EndDateActive=null`, `count=1` and `hasMore=false`. This supports `High` to
`HIGH` resolution on 2026-10-14 for that target. This is user-provided evidence,
not an independently executed discovery call; the target host and audit fields
are deliberately excluded. Other targets, names and business dates still need
their own complete lookup evidence through the selected workflow.
Unregistered code-only display inputs, unsupported Quick Entry labels and
unproven outline mappings remain blocked; never uppercase a name into a code.

## Consultant Route Checks

| Check | What to confirm | Result if incomplete |
|---|---|---|
| Identity | One exact name/number match for mutation, all collection pages needed for a conclusive result, and returned canonical item URI. | Stop on zero or multiple matches for update, end-date, or child CUD. |
| Core create/update | Published method, operation-specific required/writable fields, supplied-reference representation, authenticated target read access, and read-back route. | Stop before preview on a contract/reference gap; do not require a probe write. |
| Child collection | Exact published method/path/key, target-supported method, required body fields, cardinality, duplicate rule, and read-back URI. | Stop before preview; disclose the unsupported child operation. |
| Composite/other surface | A documented REST operation covers every requested field and has a read-back route. | Stop; this skill has no alternate execution route. |
| Route continuity | The immutable operation list can complete and independently verify each requested change through REST. | Do not split the request with an undocumented route or change after approval. |

## Required Request-Specific Discovery

| Requested change | Required discovery before preview |
|---|---|
| Create or update core values | Exact target method, returned item/collection path, current writable and required attributes, reference representation, and response/read-back contract. Do not call another template's contextual LOV for a new-template create. |
| Child row change | Exact child path/method, returned parent and child URIs when the parent exists, published required fields, observed operation-specific runtime requirements, cardinality, duplicate rule, and independent reread path. |
| Copy, duplicate, or create from project/template | No published project-template REST copy operation is documented. Stop and report that this operation is unsupported. |
| Any named project/financial/reporting surface not in the child table | Exact published REST operation and read-back route. Otherwise stop and report the uncovered surface. |
| End-date or semantic change | `ProjectTemplateEndDate` PATCH support plus documented consumer/use evidence when available. Unknown consumer impact blocks semantic/end-date changes. |

## Non-REST Boundaries

| Request | Result |
|---|---|
| Delete a project template | Unsupported. Use an impact-validated end date when appropriate. |
| FSM export/import or CSV import | Unsupported for this task. |
| Duplicate, copy, or create from another template/project | Unsupported: no published project-template REST copy operation is documented. |
| A child method absent from the child contract table | Unsupported. Do not emulate it with a different verb or resource. |
| Partial REST create/update | Block. Do not claim a whole-template outcome from a partial core response. |
| Alternate execution path after approval or failure | Block. Keep the REST operation list immutable. |
