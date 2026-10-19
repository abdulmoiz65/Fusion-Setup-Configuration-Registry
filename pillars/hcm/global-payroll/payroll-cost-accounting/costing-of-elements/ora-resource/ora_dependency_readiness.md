# Costing of Elements Dependency Readiness

Live Search supplies canonical identity. The operation resolvers supply LDG
structure, dated state, valid choices and account metadata. The user's request
supplies desired changes; core.data-loader supplies current HDL schemas.
Do not ask the user to repeat facts already resolved from these authorities.
For End Date, complete detail supplies the allocation, EL and every existing
LIV target, preserved CostInfo values and account comparison evidence. Value
LOV/KFF dependencies do not run, even for type D.
Zap uses the complete historical identity inventory and skips all write-value
dependencies. End Date/Zap status resumes use their retained context and
dedicated result branch; they do not re-enter preparation dependencies.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Shared identity | Discover LDG/eligibility and retain requested_operation. |
| 2 | State and scope | Resolve complete history and expanded detail; resolve structure only for operations rendering or validating it. Apply operation-specific scope rules. |
| 3 | Values | Resolve requested type/group/input choices and required account metadata. |
| 4 | Preparation | Apply defaults, check dependencies, retrieve touched templates and render DATs. End Date artifact_only stops with the locally checked ZIP; the normal handoff requires full loader validation and Task Hook. |
| 5 | Handoff | Obtain core.data-loader's exact-artifact approval once and submit through that workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| search_ldg | Selected LDG | Conditional | LDG text supplied | Lookup | Live LDG response | resolve_element_costing_ldg | Search requires its numeric selector. | Select only when ambiguous. | ldg_id;ldg_name |
| element_eligibility | Canonical target | Yes | Non-Search | Lookup | Complete Search | search_element_costing | Supplies EL user keys. | Do not re-enter resolved keys. | ElementCode;ElementEligibilityName;LegislativeDataGroupName;ElementLinkId |
| costing_structure | Cost Allocation flex assignment | Yes | Create/Update; Correct context validation | Lookup | Exact LDG detail | resolve_element_costing_structure | Defines IdFlexNum for this LDG. | Fix missing assignment when lookup proves it absent. | IdFlexNum |
| costing_history | Complete dated state | Yes | Create/Update/Correct/End Date/Zap | Lookup | Live PayCostSearchVO | query_element_costing_history | Establishes absence, selected interval or full logical Zap history. | Resolve malformed or ambiguous history. | complete_history |
| costing_detail | Full existing snapshot or absence | Yes | Create/Update/Correct/End Date/Zap | Lookup | Live genericCosting | read_element_costing_record | End Date needs allocation/EL/LIV state; Zap needs every history period's accounts and EL/LIV identities plus exclusivity evidence. | Resolve incomplete child collections before editing. | baseline;zap_targets |
| costing_type | Valid type | Conditional | A type is supplied or changed | Lookup | Live type LOV | resolve_element_costing_type | Maps label to code. | Choose one valid type. | CostableType |
| distribution_group | Valid LDG group | Conditional | Create/Update/Correct with Distributed type or explicit group | Lookup | Live distribution LOV | resolve_element_distribution_group | Supplies the canonical HDL group name. | Choose a returned group. | DistributionSetName |
| costed_inputs | Valid eligibility inputs | Conditional | Inputs supplied or changed | Lookup | Live input LOV | resolve_element_costed_input | Distinguishes link inputs from units/base inputs. | Choose a returned input name. | LinkInputName;LinkInputValueId |
| partial_kff | Runtime mapping | Conditional | Create/Update account values are rendered | Lookup | Runtime descriptor | resolve_element_costing_kff | Maps business labels without guessing columns. | Resolve metadata, not a manual SegmentN guess. | runtime_segments |
| segment_values | Valid component values | Conditional | Create/Update account values are rendered | Lookup | Runtime LOV contracts | validate_element_costing_segments | Validates codes and effective dates. | Supply only missing or invalid values. | validated_components |
| priority_accounts | Full account combination | Conditional | OVRRIDE rendered in Create/Update | Lookup | Full KFF and costAccounts | resolve_element_priority_account | Supplies a validated complete account. | Resolve a missing combination separately. | ConcatenatedSegment |
| loader_schema | Current template and keys | Yes | Before rendering | Lookup | core.data-loader | resolve_element_hdl_templates | Prevents obsolete or invented headers. | Retrieve automatically through the loader. | validated_schemas |
| submission_context | Project and loader prerequisites | Yes | Before import | Required | Routed project workflow and core.data-loader | | Schema retrieval alone does not initialize the project or activate its Run Book. | Complete the route's existing prerequisites; no task-local bypass or duplicate approval. | approved_preflight;task_validation_envelope |
| zap_delete_contract | DELETE keys, capability and component dependencies | Yes | Zap preparation | Required | Current core.data-loader validation | | The independent allocation, account and EL/LIV targets must all be supported. | Validate every included object and the source-specific key forms; metadata presence or ZIP ordering alone is insufficient. | zap_schema_validation;zap_dependency_validation |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup ready | Valid Search selectors/date. | Shared lookup phase for any operation. |
| Identity ready | Unique complete result. | Continue the original operation automatically. |
| Values ready | Applicable resolver facts and operation scope are valid. | Retrieve templates and prepare source; no upload yet. |
| End Date artifact prepared | Live baseline, bounded scope, ordinary schema and local shape pass; user requested artifact_only. | Return local DAT/ZIP only, with loader_validated=false. |
| Source ready | Loader and Task Hook pass for immutable bytes. | One loader approval gate. |
| Blocked | Missing/ambiguous business value, runtime evidence, source schema or project prerequisite. | Stop the dependent step with its actual missing item. |

Assignment-attribute eligibility creation remains outside this change. A request
to create a new eligibility or costing link requires its own authored source;
an existing selected regular eligibility needs no extra CostingLinkFlag change.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COE.SEARCH.CHECK_DEPENDENCIES | decision | 4 | resolve_dependency | ldg_text->COE.SEARCH.RESOLVE_LDG;direct->COE.SEARCH.ENFORCE_ROUTE;blocked->COE.HDL.HANDLE_ERROR | COE.SEARCH.APPLY_DEFAULTS | stop | Select LDG discovery or direct Search; defer HDL prerequisites. |
| COE.HDL.CHECK_DEPENDENCIES | decision | 22 | resolve_dependency | ready->COE.HDL.RESOLVE_TEMPLATES;blocked->COE.HDL.HANDLE_ERROR | COE.HDL.APPLY_DEFAULTS | stop | Require applicable resolved facts and business inputs without duplicate GETs; loader_schema is completed next. Check submission_context before any import handoff, not as a reason to block permitted metadata retrieval. |
| COE.ZAP.CHECK_DEPENDENCIES | decision | 32 | resolve_dependency | ready->COE.ZAP.RESOLVE_TEMPLATES;blocked->COE.HDL.HANDLE_ERROR | COE.ZAP.CHECK_SCOPE | stop | Require bound identity, complete history/detail and the full physical target inventory. Skip value/KFF/default dependencies. Resolve loader_schema next and finish zap_delete_contract plus submission_context before any execution approval; no additional GETs here. |
