# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| check_project_status_operation_scope | Before external lookup and again after current baseline resolution | Normalized request and optional current same-target baseline | Run scripts/check_operation_scope.py under the local contract below; separate source identity from requested changes and compare complete lifecycle sets | Scope status, reason, proposed complete append set; task_validation_complete=false and import_authorized=false | Explicit/implicit unsupported changes refuse; malformed shape returns issues; missing baseline proceeds to the declared lookup only, never to a write |
| find_project_status | Create/update/import or named read | Complete same-target identity response from lookup_project_status_identities plus available native parent/child export | Map StatusObjectCode to StatusType and StatusClassificationCode to ProjectSystemStatusCode; match exact object/name across classifications or verify a supplied stored code against the requested object | Exists, stored code, current display name, baseline, children and identity coverage | Zero permits create only with complete absence evidence; one permits update only; ambiguity blocks. Named reads may return available LOV fields with missing native details disclosed |
| resolve_status_capabilities | Every change | Local object/classification catalogs, Field Editability table, requested fields, and supplied baseline predefined/use flags | Resolve one object and one classification; require addable only for creation; check lifecycle and field capabilities separately for existing rows | Canonical StatusType and ProjectSystemStatusCode, create permission, field editability and warnings | Reject ambiguity, forbidden create or unsupported field; do not reject an existing lifecycle merely because creation is disabled; no external catalog query |
| resolve_status_graph | Initial/lifecycle/workflow/end-date changes | Verified identity/code map from lookup_project_status_identities, local classification catalog, supplied native transitions, workflow codes and use evidence | U and workflow target exact statuses of the same object. S targets a classification code of the parent object and uses the separate native bridge below, not a custom status in that classification | Business targets, stored codes, native child keys, lifecycle edges, date/use findings and deferred checks | Reject ambiguous/missing requested targets and unavailable native bridges. Disclose missing downstream mappings separately; no undeclared external lookup |
| resolve_status_controls | Project or impact-detail controls requested; PROJECT creation | Current same-target controls and object-scoped action catalog; documented standard matrix only for PROJECT create under prefer-current-else-standard | PROJECT create uses exact classification-code source rows when available; only an excluded source parent permits standard-source configuration. Use scripts/resolve_project_controls.py for native evidence. Derive AllowOverridesFlag and CopyToUserStatusFlag separately. Existing updates require current flags | Complete control rows, selected policy, controls_basis, inheritance_verified and preview disclosures | Exact-inheritance missing rows, inconsistent evidence, unsupported scope or missing update values blocks. Standard mode must not substitute a custom status or invent CR_DTL codes |
| resolve_progress_weight | PROGRESS creation | Supplied selected classification's predefined progress status | Exact PROGRESS/classification; copy its ProjectStatusWeight | Inherited weight | Block missing or ambiguous weight; no universal numeric default |
| verify_project_status_scope | Before validation | Catalog codes and target | Exact task/target | Verified scope | Block mismatch |
| verify_project_status_package | Before import | Template/export and generated package | Exact conditional member set, headers, counts, checksum | Verified contract | Block unproven/changed/mixed package |

## Local Operation Scope Guard

Run the pure local guard with `python3 scripts/check_operation_scope.py --input <scope-input.json>` from this task folder. The JSON root contains request and an optional baseline. No output file is required; retain the returned JSON in the normal project validation record. The guard does not establish provenance, complete identity, editability, references, native serialization or package readiness.

Construct a scope input fragment, not a copy of transport/configuration options. For non-create requests, only the request fields listed below are accepted (the create-only NextAllowableStatusFlag is excluded). Put scalar edits inside changes and lifecycle targets/intent outside changes. A misplaced mutation field returns an input issue rather than silently bypassing the scope checks. StatusType always identifies the source object; it cannot be changed through changes.

| Input | Required Shape | Handling |
|---|---|---|
| request.operation | Canonical operation string | Read/create/update/validate/export/import/end_date continue to task checks; explicit rename/clear/delete/remove_lifecycle/replace_lifecycle refuse before external lookup |
| request.StatusType and request.ProjectStatusName | Existing source identity when supplied | Keep the old name here; a different changes.ProjectStatusName is an unsupported rename, not a new ordinary update |
| request.changes | Object of explicit changed native parent fields | For existing rows, empty string or null is a clear request and refuses. False is an explicit value, not missing input. Omitted fields remain outside the requested diff |
| request.clear_fields | Optional list of field-name strings | Nonempty means unsupported persisted clear |
| request.NextAllowableStatusFlag | Optional canonical create value | The normal task defaults still apply; the guard itself never defaults fields |
| request.LifecycleTargets | Optional unique list of resolved code strings | Use status codes in U and classification codes in S; resolve their scope and native bridges separately through resolve_status_graph |
| request.lifecycle_intent | append or replace, with an explicit target list | Append returns the union of current and new targets. Replace may continue only when it removes no current target; dropping an old target refuses |
| baseline | Optional object with resolved StatusType/ProjectStatusName; lifecycle checks also require NextAllowableStatusFlag and complete LifecycleTargets | Identity mismatch or malformed/incomplete collections fail closed. Any mode change with existing children refuses; do not reinterpret old rows |

| Scope Status / Exit | Task Graph Mapping | Next Action |
|---|---|---|
| eligible_for_task_validation / 0 | valid at input; resolved after baseline | Continue ordinary task checks. This is not a ready import or successful write |
| invalid / 1 | invalid at input; failure after baseline | Return exact input/evidence issue |
| unsupported / 2 | unsupported to PSTATUS.RETURN_REFUSAL at either gate | Retain intent and explain the named unsupported mechanism; do not query UI or another pod |
| needs_baseline / 3 | valid at input only, to resolve identity/baseline; failure if unresolved at the later gate | Resolve current evidence through the declared workflow; do not default or build a package yet |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| lookup_project_status_identities | Named status read, create/update identity coverage or lifecycle/workflow target resolution; skip whole-task export/template-only operations | Selected environment and requested object/name/classification or stored code; a complete current same-target response may be supplied | GET /fscmRestApi/resources/11.13.18.05/projectStatusesLOV/describe, then GET /fscmRestApi/resources/11.13.18.05/projectStatusesLOV?onlyData=true&limit=500&offset=0 through core.fusion-api.rest-api-client; follow every page while hasMore is true | ProjectStatusCode, ProjectStatusName, StatusObjectCode, StatusClassificationCode, StartDateActive, EndDateActive, WorkflowEnabledFlag | Confirm live read-only schema and expected fields; consume the unfiltered collection for absence/code coverage. Match object/name or supplied stored code exactly for statuses and exact classification code for S targets. Never use an active-date finder or classification filter as a complete inventory | Current object/name/code map, dates, boolean workflow flag, all-page coverage and target provenance | An incomplete page, auth failure, unexpected schema or ambiguous match blocks affected writes. No match proves absence only within complete unfiltered coverage. No other pod or setup UI fallback |

The endpoint is read-only: source registration disables create/update/delete and the verified describe exposes only GET. It does not supply action controls, PredefinedFlag, current-use state, NextAllowableStatusFlag or workflow outcome fields; obtain those from the declared native export/current evidence, preserving known seed exclusions. WorkflowEnabledFlag is a boolean readback of EnableBpFlag; map false to N and true to Y. Never send PATCH/POST/DELETE to this LOV.

## Classification-Control Evidence Contract

For PROJECT creation, resolve the classification's source status by exact stored code, not its display label or a custom status with the same classification. A renamed source status remains the same source. When using native rows, join their parent object/name to the complete LOV identity map and prove that the parent's ProjectStatusCode equals the classification code. Require one complete control set with unique object-scoped ActionCode values and verified EnabledFlag, SortOrder and StatusType. The helper requires all seven supported PROJECT actions before claiming verified inheritance; partial current rows block and must not be filled from the standard matrix. Supplied evidence must identify the target, capture time, classification source code and complete scope.

The UI copies ActionCode, SortOrder, StatusType and EnabledFlag from controls whose source status code equals the selected classification code, then derives AllowOverridesFlag and CopyToUserStatusFlag. Native migration exports can filter unmodified seeded rows. The declared setupTaskCSVExports contract has no seed-inclusion attribute; do not invent one or assume a filter criterion restores excluded seed rows.

No live non-UI control lookup is currently declared here. Under `exact-inheritance`, unavailable current classification controls still block as `workflow_gap` / `catalog_or_metadata_mismatch`. The standard matrix is not evidence of current target values. Under the default PROJECT create policy `prefer-current-else-standard`, it is an explicit configuration source when the exact classification identity exists but its source parent is excluded from the export. Persist `controls_basis: standard_source` and `inheritance_verified: false`; show the affected names, all values and the current-inheritance limitation before exact Data Loader approval. Do not use this policy for updates, PROGRESS weight, CR_DTL or any other object, and do not suppress malformed or conflicting supplied evidence. Current controls take precedence whenever available. UI inspection remains an explicitly requested authoring activity, never a consultant prerequisite.

### Local PROJECT Create Resolver

Run `scripts/resolve_project_controls.py` from this task folder after the declared identity read and native export when resolving native classification-control evidence. Separately supplied complete verified current classification controls take precedence over a helper standard-source proposal; retain their provenance and apply the same source-code and integrity checks. Its inputs must come from the selected environment with recorded capture times and unfiltered/all-page identity coverage. The helper checks pagination markers, any supplied count, exact identities, native source matching and row integrity; the calling workflow remains responsible for provenance, freshness, full native package validity and the other status-field rules. For multi-page lookups supply the verified aggregate with integer offset 0, hasMore false and every item; if count is supplied, set it to the aggregate item count. Retain original page receipts in the project evidence. Do not relabel a filtered or incomplete response as complete.

Normalized request JSON is an object with `operation: create` and a nonempty `statuses` list. Every row contains `StatusType: PROJECT`, exact `ProjectStatusName` and canonical `ProjectSystemStatusCode`. Other normalized parent fields stay in the calling blueprint. Optional `AllActionsAllow` accepts a boolean or Y/N, Yes/No, true/false; alternatively `ActionControls` is a list of objects containing only `ActionCode` and `Allow`. These inputs change AllowOverridesFlag, never EnabledFlag. CLOSED Allow overrides remain protected. Labels such as "Summarize project data" must first resolve to STATUS_REPORTING using this resource; they are not ActionCode values.

```bash
python3 pillars/erp/project-financial-management/project-foundation/manage-project-statuses/scripts/resolve_project_controls.py \
  --requests-file <normalized-create-request.json> \
  --identities-json <complete-current-projectStatusesLOV.json> \
  --current-export <same-target-native-export.zip> \
  --environment <selected-environment> \
  --policy prefer-current-else-standard \
  --output <project-workspace>/controls-resolution.json
```

Use `--policy exact-inheritance` when explicitly requested. A blocked result or nonzero exit must stop package preparation; successful rows in a partially blocked batch are not approval for a partial import. The result includes native control-field values and input hashes but is not itself a native package. Keep policy, basis, warnings and hashes in the blueprint/preview, not invented CSV columns. Fill remaining native headers using the established new-row/template contract, keep both parent passes and metadata unchanged, and pass the assembled package through Task Hook and Data Loader approval. Standard source values must be checked against the approved values in independent post-import readback; a matching readback establishes configured-value success, not proof of the prior UI defaults.

The helper validates requested action names, Allow values and protected CLOSED overrides before resolving inheritance. Missing exact current controls produces blocker_type workflow_gap with failure_class catalog_or_metadata_mismatch and controls_request_validation passed; conflicting current rows produce evidence_conflict. Invalid control input produces input_validation and controls_request_validation failed. This narrow validation result never covers parent dates, other status fields, provenance or import approval. Preserve every per-status error and stop the whole batch when any error exists.

Reuse a supplied response only when its environment, capture time, unfiltered scope, schema fields and complete pagination are verified. Otherwise obtain current data through the selected core REST workflow. Persist business artifacts and sanitized provenance through the project managers; keep raw pod data and credentials outside the portable skill.

## Status Object Capability Catalog

This task-local catalog is the sole authority for status-object and status-type validation. It includes only values exposed by the Manage Project Statuses Status Objects table; `PROGRAM` is excluded because it is seed-only and not exposed by that table.

| Status Object Code | Meaning | Initial Status Allowed | Lifecycle Edit Allowed | Control Actions Allowed | Workflow Allowed |
|---|---|---|---|---|---|
| ACTION | Action | No | No | No | No |
| ACTION_DETAIL | Action Detail | No | No | No | No |
| BILL_TRANSACTION | Bill Transaction | No | No | No | No |
| CHANGE_REQUEST | Change Request | No | Yes | No | Yes |
| CR_DTL | Change Request impact detail | No | Yes | Yes | No |
| GATE | Gate | No | Yes | No | No |
| MILESTONE | Milestone | No | No | No | Yes |
| PJT_PROJECT_TASK | Project Task | No | Yes | No | No |
| PROGRESS | Progress | No | No | No | No |
| PROJECT | Project | Yes | Yes | Yes | Yes |
| SOV | Schedule of Values | Yes | Yes | No | Yes |
| SOV_LINE | Schedule of Values Line | No | No | No | No |

## Valid Addable Status Object and Status Type Values

These pairs permit creation. Existing-status changes use the separate field and lifecycle checks below; creation permission does not grant every field edit.

| Status Object Code | Status Type Code | Meaning |
|---|---|---|
| CHANGE_REQUEST | NEW | New (draft) |
| CHANGE_REQUEST | SUBMITTED | Submitted for review or approval |
| CR_DTL | APPROVED | Approved change-request impact detail; ready for change-order consolidation |
| CR_DTL | PENDING | Pending approval |
| CR_DTL | REJECTED | Rejected |
| GATE | CLOSED | Stakeholder review stopping point |
| PJT_PROJECT_TASK | COMPLETE | Complete |
| PJT_PROJECT_TASK | IN_PROGRESS | In progress |
| PJT_PROJECT_TASK | NOT_STARTED | Not started |
| PROGRESS | PROGRESS_STAT_AT_RISK | At risk; minor issues |
| PROGRESS | PROGRESS_STAT_IN_TROUBLE | In trouble; major issues |
| PROGRESS | PROGRESS_STAT_ON_TRACK | On track; proceeding as planned |
| PROJECT | ACTIVE | Active |
| PROJECT | CLOSED | Closed |
| PROJECT | DRAFT | Draft |
| PROJECT | PENDING_CLOSE | Pending close |
| PROJECT | SUBMITTED | Submitted |

## Valid but Not Addable Status Object and Status Type Values

These pairs are recognized but disallow new-status creation. Existing lifecycle or field updates are assessed independently; do not substitute another object or classification.

| Status Object Code | Status Type Code | Meaning |
|---|---|---|
| ACTION | FAILURE | Failure |
| ACTION | PARTIAL_SUCCESS | Partial Success |
| ACTION | SUCCESS | Success |
| ACTION_DETAIL | FAILURE | Failure |
| ACTION_DETAIL | NOT_ALLOWED | Not Allowed |
| ACTION_DETAIL | SUCCESS | Success |
| BILL_TRANSACTION | ACTION_PENDING | Action pending; action is not complete |
| BILL_TRANSACTION | BILLED | Billed |
| BILL_TRANSACTION | ERROR | Error; billing-blocking exception |
| BILL_TRANSACTION | INSUFFICIENT_FUNDS | Insufficient funds; contract hard limit reached |
| BILL_TRANSACTION | IN_PROGRESS | In progress; included in an incomplete invoice or credit memo |
| BILL_TRANSACTION | NON_BILLABLE | Nonbillable |
| BILL_TRANSACTION | ON_HOLD | On hold; temporarily withheld from billing |
| BILL_TRANSACTION | READY | Ready to bill |
| CHANGE_REQUEST | APPROVED | Approved; ready for change-order consolidation |
| CHANGE_REQUEST | CANCELED | Canceled |
| CHANGE_REQUEST | CLOSED | Closed; expected progression completed, with no further action |
| CHANGE_REQUEST | REJECTED | Rejected |
| GATE | IN_REVIEW | In review by project stakeholders |
| GATE | OPEN | Open; stakeholders approved results and project continues |
| GATE | TERMINATED | Terminated; stakeholders disapproved results and project ends |
| MILESTONE | COMPLETE | Complete |
| MILESTONE | IN_PROGRESS | In progress |
| MILESTONE | NOT_STARTED | Not started |
| MILESTONE | REJECTED | Rejected |
| MILESTONE | SUBMITTED | Completion approval requested |
| SOV | ACTIVE | Active; ready for progress capture |
| SOV | APPROVE_ACTIVATION | Pending Activation Approval |
| SOV | APPROVE_CLOSURE | Pending Closure Approval |
| SOV | APPROVE_REACTIVATION | Pending Reactivation Approval |
| SOV | APPROVE_REOPENING | Pending Reopening Approval |
| SOV | CLOSED | Closed for further progress capture |
| SOV | DRAFT | Draft; never active and open for updates |
| SOV | UNDER_REVISION | Under Revision; previously active and being revised |
| SOV_LINE | CLOSED | Closed for further progress capture |

## Invalid Values

| Value Category | Invalid Value | Required Handling |
|---|---|---|
| Status object | PROGRAM | Reject: it is seed-only and absent from this task's Status Objects table. |
| Status object | Any code absent from the Status Object Capability Catalog | Reject: do not infer, partially match, or query an external source. |
| Status type | Any object/type pair absent from both status-type catalogs | Reject: do not infer, partially match, or substitute a different object or type. |
| Create operation | Any pair in Valid but Not Addable Status Object and Status Type Values | Reject creation of the exact pair; do not reject permitted edits to an existing status solely for this reason. |
| Lifecycle operation | An object whose Lifecycle Edit Allowed flag is No | Reject the operation regardless of creation permission. |

## Shared Local LOVs

| LOV | Code | Meaning |
|---|---|---|
| Next Allowable Status | A | All |
| Next Allowable Status | N | None |
| Next Allowable Status | S | Status Classification |
| Next Allowable Status | U | Status |
| Boolean Flag | Y | Yes |
| Boolean Flag | N | No |

| LOV | Valid Value |
|---|---|
| Project Control Action | ADJUST_TXNS |
| Project Control Action | CAPITALIZE |
| Project Control Action | CAPITALIZED_INTEREST |
| Project Control Action | GENERATE_BURDEN |
| Project Control Action | NEW_TXNS |
| Project Control Action | PGRS_REPORT_TEAM_MEMBER |
| Project Control Action | STATUS_REPORTING |
| CR_DTL Control Action | UPDATE_IMPACT_DETAILS |

PROJECT action codes must not be applied to CR_DTL. UPDATE_IMPACT_DETAILS means Update Impact Details in Change Order and is associated with the Approved impact-detail status; require the selected target's actual control row before an update.

## Project Classification Control Defaults

This is the maintained standard-source matrix consumed by the local create resolver. Prefer current exact classification controls when available; under the standard create policy these rows are proposed explicit values, with current inheritance unverified. Changes to a source control's AllowOverridesFlag do not change the new status's derived Allow default; the UI copies EnabledFlag separately. Do not infer either flag from an exported custom status.

The EnabledFlag values below are not the UI Allow checkbox. New PROJECT controls default AllowOverridesFlag to N for DRAFT/CLOSED and Y otherwise, independently of their inherited EnabledFlag. The enhanced editor's EnabledBool reads AllowOverridesFlag and writes the same flag; an editable Allow change must preserve EnabledFlag, CopyToUserStatusFlag and SortOrder.

| Action Code | UI Meaning | Sort Order | ACTIVE EnabledFlag | DRAFT/CLOSED EnabledFlag | SUBMITTED EnabledFlag | PENDING_CLOSE EnabledFlag |
|---|---|---|---|---|---|---|
| NEW_TXNS | Create new transactions | 1 | Y | N | Y | N |
| ADJUST_TXNS | Adjust transactions | 2 | Y | N | N | N |
| CAPITALIZE | Capitalize assets | 5 | Y | N | N | N |
| STATUS_REPORTING | Summarize project data | 6 | Y | N | N | N |
| CAPITALIZED_INTEREST | Capitalized interest | 20 | Y | N | N | N |
| GENERATE_BURDEN | Create burden transactions | 25 | Y | N | Y | Y |
| PGRS_REPORT_TEAM_MEMBER | Progress reporting by team members | 30 | Y | N | Y | Y |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| Child group omitted | Preserve baseline in the proposed FSCR diff; omitted CSV-member preservation is not an established loader guarantee |
| Next type changes | Show removed/added graph edges and require warning confirmation |
| Workflow target is workflow-enabled | Use the declared identity lookup's boolean flag and supplied native outcome edges; disclose unavailable downstream mappings as deferred to Fusion service validation |
| Transactional status-change API exists | Do not treat it as setup-write authority |
| Blank template unproven | Keep import blocked |
| A new status is requested | Resolve object and classification locally and require the pair to be addable; do not use create permission as an existing-status edit gate. |
| A lifecycle target is requested | Resolve U as a same-object status and S as a parent-object classification with a separate native code bridge. Add permission is not a target gate. Use only the declared read-only identity route and native artifacts; no ad hoc pod or database query |

## Field Editability

| Scope | Consultant Configuration | Restriction |
|---|---|---|
| Status objects and classifications | Select existing entries | Predefined catalogs and capability flags are not consultant editable |
| PROJECT | Name, description, dates, Initial, next-allowable type, lifecycle, supported Allow flags and workflow outcomes | Predefined classification is protected; the seeded Active project status cannot be end-dated. In-use status restricts classification, start date and workflow changes; do not block permitted name, description, end date or lifecycle changes solely because it is used |
| CHANGE_REQUEST | Existing name, description, dates and lifecycle; custom creation for NEW/SUBMITTED only | Enable Workflow can be edited only for SUBMITTED; required outcome targets apply there |
| CR_DTL | Existing name, description, dates, lifecycle and existing action Allow flags | No workflow or Initial; UPDATE_IMPACT_DETAILS belongs to Approved impact-detail controls, not Project controls |
| PROGRESS | Custom name, description, dates; inherited weight | Predefined progress statuses are protected; no Initial, workflow, lifecycle or project controls |
| MILESTONE/SUBMITTED | Enable Workflow on the existing Completion approval requested status | Sole milestone edit exception; preserve fixed outcomes; no custom creation |
| Other MILESTONE classifications | Read existing status | No editable workflow exception or custom creation |
| ACTION, ACTION_DETAIL, BILL_TRANSACTION, SOV_LINE | Read existing status | No custom creation or general field editing |
| GATE, PJT_PROJECT_TASK, SOV | Use declared lifecycle capability on an existing row when its stored type is S/U | Enhanced editor presents general status fields as read-only; do not infer editable names/dates/workflow from object-level capability flags. GATE and PJT_PROJECT_TASK creation allowed by their catalog still requires a verified creation-field route |
| PROJECT/CLOSED controls | Read existing Allow values | Allow checkbox disabled; do not bypass it through CSV |
| Action control AllowOverridesFlag | Editable Allow switch for supported existing control rows | PROJECT/CLOSED checkbox is disabled; DRAFT's default N does not make its checkbox read-only |
| Project control EnabledFlag, CopyToUserStatusFlag and SortOrder | Inherit or preserve | Not the user-editable Allow switch. A correction to a value written by a failed validation test requires its verified original baseline and a separate exact repair preview |

## Object and Classification Field Matrix

This matrix applies to every classification in the two local catalogs. Object-level capabilities indicate which features exist; they do not override field read-only rules, actual control rows, in-use restrictions or native import limits.

| Status Object | Classifications | Next Allowable Status Type | Lifecycle Targets | Action Allow | Enable Workflow | Accepted / Rejected Outcomes |
|---|---|---|---|---|---|---|
| PROJECT | ACTIVE, CLOSED, DRAFT, PENDING_CLOSE, SUBMITTED | A/N/S/U editable where status fields are permitted | S classifications; U exact same-object statuses; preserve/removal checks apply | Seven inherited actions; CLOSED protected, other classifications editable | Editable where not in use and Initial=N | Both exact same-object status codes required when enabled; preserve when omitted |
| CHANGE_REQUEST | APPROVED, CANCELED, CLOSED, NEW, REJECTED, SUBMITTED | A/N/S/U independently of add permission | S/U on existing status; native S bridge can be unavailable | No controls | SUBMITTED only; other classifications preserve | Editable only with supported enabled workflow; resolve actual status codes rather than classification codes |
| CR_DTL | APPROVED, PENDING, REJECTED | A/N/S/U independently of add permission | S/U on existing status; native S bridge can be unavailable | Actual existing UPDATE_IMPACT_DETAILS row only; no invented seven-action inheritance on create | No | Preserve; reject requested workflow changes |
| GATE | CLOSED, IN_REVIEW, OPEN, TERMINATED | Read-only in enhanced editor; preserve current value including legacy Y | Existing S/U collections only when represented and encodable; do not convert Y to expose a table | No | No | Preserve |
| PJT_PROJECT_TASK | COMPLETE, IN_PROGRESS, NOT_STARTED | Read-only in enhanced editor; preserve current value including legacy Y | Existing S/U collections only when represented and encodable; do not convert Y | No | No | Preserve |
| SOV | ACTIVE, APPROVE_ACTIVATION, APPROVE_CLOSURE, APPROVE_REACTIVATION, APPROVE_REOPENING, CLOSED, DRAFT, UNDER_REVISION | Read-only in enhanced editor | Existing S/U collections subject to exact native bridge; capability alone is not an import contract | No | Existing seeded workflow is read-only; do not reset it to N | Fixed stored outcomes are read-only; preserve SOV-prefixed codes |
| MILESTONE | COMPLETE, IN_PROGRESS, NOT_STARTED, REJECTED, SUBMITTED | No; preserve N | No | No | Only the existing MS_SUBMITTED status permits a toggle; other classifications read-only | MS_SUBMITTED preserves MS_COMPLETE / MS_REJECTED, including when workflow is disabled; selectors read-only |
| PROGRESS | PROGRESS_STAT_AT_RISK, PROGRESS_STAT_IN_TROUBLE, PROGRESS_STAT_ON_TRACK | No requested lifecycle change | No | No | No; an underlying enable-update expression does not override the hidden object capability | Preserve |
| ACTION | FAILURE, PARTIAL_SUCCESS, SUCCESS | No | No | No | No | Preserve |
| ACTION_DETAIL | FAILURE, NOT_ALLOWED, SUCCESS | No | No | No | No | Preserve |
| BILL_TRANSACTION | ACTION_PENDING, BILLED, ERROR, INSUFFICIENT_FUNDS, IN_PROGRESS, NON_BILLABLE, ON_HOLD, READY | No | No | No | No | Preserve |
| SOV_LINE | CLOSED | No | No | No | No | Preserve |

There are 12 exposed objects and 52 object/classification pairs. PROGRAM and its three classifications are seed-only and remain outside this task. A baseline snapshot may carry protected fields and legacy values unchanged; that is not a request to configure those fields.

## Lifecycle Target and Native CSV Bridge

| Selected Type | Business Target | Stored NextAllowableStatusCode | Native PJF_NEXT_ALLOW_STATUSES.csv Target | Verification |
|---|---|---|---|---|
| A (All) | Any status | No explicit target list required | No new lifecycle children | Confirm parent flag A; do not hide a requested removal of existing children |
| N (None) | No outgoing transition | No explicit target list required | No new lifecycle children | Confirm parent flag N; dropping existing children from CSV is not a clear |
| U (Status) | Exact status name of the parent object | Target's verified ProjectStatusCode | Target ProjectStatusName and StatusType, with the source parent in PJF_PROJECT_STATUSES.* columns | Require exact same-object identity; readback target name/code set must equal the approved set |
| S (Status Classification) | Classification code C of the parent object | C itself, not the code of a custom status in that classification | Find the unique current status identity whose ProjectStatusCode is exactly C, then use that identity's ProjectStatusName and StatusObjectCode as the CSV target name/type | This row is a transport bridge, not the business target. Its object may differ from the parent. Verify parent-object classification C separately and prove bridge code equals C |
| Existing legacy value such as Y | Existing product-managed behavior | Preserve baseline | Preserve exact existing rows; do not construct new S/U rows by guessing | No invented normalization or claim that the enhanced lifecycle selector supports Y |

The migration service excludes NextAllowableStatusCode from the CSV and resolves target ProjectStatusName plus StatusType back to ProjectStatusCode. The enhanced S-mode selector instead stores ProjectSystemStatusCode; U stores ProjectStatusCode. These are different code domains. DefaultProjectStatusCode can be null and is not a universal CSV bridge.

For example, PROJECT/S with Draft targets DRAFT. Resolve the current identity whose stored code is DRAFT; its display name may have been renamed. Never pick FSCR_Draft merely because its classification is DRAFT. In CHANGE_REQUEST/S, classification CLOSED can require the global code CLOSED bridge rather than CR_CLOSED. If no status identity has code C, this CSV route cannot safely encode that classification. Report the exact unsupported bridge; do not substitute a prefixed seeded status code or a custom status. This limitation is particularly material for several CHANGE_REQUEST, CR_DTL and SOV classification codes.

## Workflow Target Mapping

| Situation | What Happens |
|---|---|
| Accepted/rejected target supplied by name | Resolve exact object/name through the current identity map; populate BpSuccessStatusCode/BpFailureStatusCode with ProjectStatusCode in both parent representations |
| Target supplied as a stored code | Verify that code resolves to the requested same-object identity; do not accept a classification-code shortcut |
| Outcome target has the same label under another object | Ignore the other object's match; never substitute PROJECT Active for SOV Active |
| Target will be newly created in this batch | A generated workflow code cannot be predicted from its name. Create the target through an approved stage, read its actual code, then prepare a separately approved workflow update; do not invent a code or silently disable the requested workflow |
| Enable Workflow omitted on update | Preserve flag and both outcome codes; no create defaults are applied |
| Enable Workflow explicitly No | Apply the requested flag only where permitted. An explicit clear or UI-equivalent clearing of stored outcomes needs verified null semantics; otherwise disclose retained outcomes and do not claim full UI-equivalent disable |
| Existing MS_SUBMITTED | Preserve fixed MS_COMPLETE and MS_REJECTED; disabling workflow does not reset these mappings |
| Existing SOV approval status | Preserve its enabled workflow and fixed SOV outcome codes; do not treat the general object capability as permission to edit them |
| BpelProcess or BpelItemType present in native rows | Preserve existing values; the UI Workflow Attributes request owns accepted/rejected outcomes, not a new workflow-process configuration. Do not invent process names from the status label |

## Native FSM Field and Member Contract

| UI/Input Name | Native Field or Member | Handling |
|---|---|---|
| Status Object | StatusType | Select from the local object catalog |
| Status Classification | ProjectSystemStatusCode | Select within the object; not part of the name uniqueness key |
| Status | ProjectStatusName | StatusType plus name is the alternate identity; keep exact spelling |
| From Date / To Date | StartDateActive / EndDateActive | Require start on create; use the acquired target format, not FromDate/ToDate as invented CSV headers |
| Initial Status / Enable Workflow | StartingStatusFlag / EnableBpFlag | Y/N |
| Next Allowable Status Type | NextAllowableStatusFlag | A=All, N=None, U=Status, S=Status Classification |
| Workflow outcomes | BpSuccessStatusCode / BpFailureStatusCode | UI labels display names but store status codes; require the selected channel's verified identity mapping, never put a display name into a code field blindly |
| Parent pass without lifecycle type | PJF_STATUS_LIST.csv | Includes controls and translations; omits NextAllowableStatusFlag |
| Parent pass with lifecycle type | PJF_PROJECT_STATUSES.csv | Includes NextAllowableStatusFlag and next-allowable rows |
| Lifecycle children | PJF_NEXT_ALLOW_STATUSES.csv | Parent columns PJF_PROJECT_STATUSES.ProjectStatusName and PJF_PROJECT_STATUSES.StatusType identify the source; target columns ProjectStatusName and StatusType use the exact U identity or verified S transport bridge. Never reverse parent and target columns |
| Action controls | PJF_PROJECT_STATUS_CONTROLS.csv | Parent columns PJF_STATUS_LIST.ProjectStatusName and PJF_STATUS_LIST.StatusType; Allow maps to AllowOverridesFlag. Preserve the separate EnabledFlag, CopyToUserStatusFlag and SortOrder |
| Translations | PJF_STATUS_LIST_TRANSLATION.csv | Parent object/name plus Language, SourceLang, translated name and description; preserve target-supported languages |
| ZIP metadata | ASM_SETUP_CSV_METADATA.xml | Preserve target-owned metadata and node ordering; header/schema presence does not prove mutation semantics |

The native template and data package must agree on task, target, members and headers. Standard exports can exclude unmodified seeded records; they are not automatically complete inventories or use-state reports. Blank/null clearing, rename, deletion and child replacement require separate verification before import. Plain CSV dates observed in the acquired native data use yyyy/MM/dd; confirm against each target template.

Oracle's FSM CSV guidance states that import does not delete records in the target. Removing a status or child row from a package is therefore not a deletion instruction. Keep child-removal checks blocked rather than treating a smaller exported collection as a replacement. This public contract does not establish this task's blank/null semantics or a separate explicit deletion action.

For rename, the native alternate identity is the existing object/name. A package containing only a new name has no proven mapping back to the old identity. Do not present that package as a rename, or report success merely because the new name appears after import; independently distinguish an update from a newly created status.

## Sources

- [Oracle Fusion Cloud Project Management 26D: Manage Project Statuses](https://docs.oracle.com/en/cloud/saas/project-management/26d/oapex/how-project-status-components-work-together.html)
- [Oracle Fusion Cloud REST API: Setup Task CSV Imports](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/api-setup-task-csv-imports.html)
- [Oracle Fusion Cloud Applications 26D: Using Functional Setup Manager, Manage Setup Using CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26d/oafsm/using-functional-setup-manager.pdf)

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSTATUS.LOOKUP_IDENTITIES | step | 2 | reference_lookup | resolved->PSTATUS.FIND_STATUS;not_required->PSTATUS.FIND_STATUS;failure->PSTATUS.RETURN_ISSUES | PSTATUS.VALIDATE_INPUT | stop | Run lookup_project_status_identities for named reads, write identity coverage and lifecycle/workflow targets, or consume its verified supplied current response; whole-task export/template-only requests require no extra lookup |
| PSTATUS.FIND_STATUS | step | 3 | evaluate_result | resolved->PSTATUS.APPLY_DEFAULTS;failure->PSTATUS.RETURN_ISSUES;unsupported->PSTATUS.RETURN_REFUSAL | PSTATUS.LOOKUP_IDENTITIES | stop | Resolve current identity/baseline and rerun check_project_status_operation_scope for existing changes before defaults; implicit rename/clear/child removal refuses, unresolved required baseline returns issues; whole-task reads skip per-status matching |
| PSTATUS.RESOLVE_GRAPH | step | 5 | evaluate_result | resolved->PSTATUS.ROUTE_OPERATION;failure->PSTATUS.RETURN_ISSUES | PSTATUS.APPLY_DEFAULTS | stop | Evaluate lifecycle mode, exact native bridge, both workflow outcome codes, complete requested action set and use evidence; disclose deferred downstream checks |
