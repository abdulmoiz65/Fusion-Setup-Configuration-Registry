# Learning Audience Dependency Readiness

The earlier Learning baseline assigns HCM Filtered Lists to HCM Tool. The
current catalog identifies that owning area as Learning Management HCM Tool
(ORA_LEARNING_MANAGEMENT_HCM_TOOL), separate from Learning Audience
(ORA_LEARNING_AUDIENCE); do not add its tasks to this skill.
The baseline's manual provider and unresolved REST resource (SOV-401) remain
historical evidence, not a live readiness check. Catalog membership alone does
not resolve the existing dependency contracts or authorize a new execution route.
Keep the existing resolver names and readiness gates below; lookup mechanics
belong exclusively to ora_reference_lookups.md.

Developer-approved correction (2026-09-24): the earlier blanket user-group
prerequisite does not apply to direct-person criteria. Evaluate the selected
operation's criteria in both managerCriteria and participantCriteria. A person
reference must still pass its documented Username or PersonId validation; no
provider readiness is inferred from that validation. Mixed criteria retain the
provider check for any filtered-list-dependent source. Unknown source semantics
must be clarified, not classified as Not applicable. This correction does not
change Manage Learning Audience Criteria or waive other execution gates.

The selected Learning rule planner checks task-wide reachable incomplete contracts,
not request-specific source applicability. A conditional Not applicable result
does not make the entire registry ready. Report any remaining planner gap
separately; do not erase unresolved contracts or treat this correction as a
registry-readiness override.

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | 1 | HCM Filtered Lists | Resolve authoritative readiness evidence before proposing audience-criteria configuration |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | 1 | HCM Filtered Lists, when applicable | Classify the requested criteria sources first; resolve provider readiness only for a filtered-list-dependent source. Direct-person ORA_PERSON criteria and requests without criteria do not require this provider |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | lac_filtered_lists | HCM Filtered Lists Foundation Skill | Yes | Every audience-criteria implementation request | Blocked | TBD: provider-owned readiness authority; baseline labels provider manual | verify_audience_filtered_list_provider | Taxonomy names this shared prerequisite | Obtain the HCM Tool provider contract and acceptable readiness evidence; a resource name alone does not satisfy it | TBD: evidence and acceptance mapping |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | lug_filtered_lists | HCM Filtered Lists Foundation Skill | Conditional | Any requested managerCriteria or participantCriteria source depends on HCM Filtered Lists, including mixed person and filtered-list criteria | Missing | TBD: provider-owned readiness authority for the selected filtered-list source | verify_user_group_filtered_list_provider | Only provider-dependent criteria require this shared prerequisite | Ask for the applicable HCM Tool provider identity, authoritative readiness source and acceptable evidence; preserve the run. If source semantics are unknown, ask which supported source is intended before evaluating readiness | TBD: evidence and acceptance mapping |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | Blocked | Provider authority, resolver or evidence contract is unresolved | No; complete the provider contract and recompile first |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Not applicable | No criteria are requested, or every requested managerCriteria and participantCriteria row is a direct-person ORA_PERSON reference with no filtered-list dependency | No filtered-list lookup; continue applicable person, visibility, duplicate, loader, privilege and approval checks only after the normal plan gate passes. This is not provider-ready evidence |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Missing | A requested source depends on HCM Filtered Lists and provider authority, resolver or evidence contract is unresolved | No affected lookup/create; ask for the applicable provider information, preserve completed work, and resume after it is supplied |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | Missing | The dependency of any requested criterion source is unknown | Ask for the source type and its authoritative semantics; do not infer Not applicable, invent a source code, or treat ORA_PERSON rows as exempting other rows |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA | Manage Learning Audience Criteria | LAC.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | ready->LAC.CHECK_DESIGN;blocked->LAC.HANDLE_ERROR | LAC.RESOLVE_REFERENCES | stop | Assess same-task provider evidence against the completed dependency contract |
| CUSTOM_MANAGE_USER_GROUPS | Manage User Groups | LUG.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | ready->LUG.CHECK_DESIGN;blocked->LUG.HANDLE_ERROR | LUG.RESOLVE_REFERENCES | stop | Assess source applicability across both criteria roles; Not applicable passes only this dependency for direct-person or no-criteria requests. Provider-dependent sources require completed readiness evidence; unknown sources return Missing |
