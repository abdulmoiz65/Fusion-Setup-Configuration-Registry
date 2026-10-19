# Manage Organization Hierarchies and Classifications Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Controlled task scope | Target environment, requested operation, accountable owner, deployment window, impact, rollback expectation | Block planning | Obtain the missing customer decision or authorization | Every request | |
| Hierarchy decision | Desired hierarchy type and whether the current target value must be preserved or changed | Block hierarchy planning | Provide the desired hierarchy outcome | Every request | resolve_allowed_hierarchy_type |
| Classification decision | Complete desired selected-classification set with at least one value | Block change planning | Provide one or more desired classifications | Every request | resolve_available_org_classifications |
| Current baseline | Current target-visible hierarchy type, classifications, and applicable default hierarchy | Block update or import planning | Review the target task or fresh target export | Update, removal, replacement, or import | resolve_current_org_hierarchy_setup |
| Default hierarchy selection | Tree, active tree version, and starting organization | Block hierarchy change | Resolve one valid target combination | Organization or department hierarchy is selected | resolve_default_org_hierarchy |
| Exact import evidence | Fresh target template, current export, metadata, members, headers, translations, identity and operation behavior | Block package preparation | Supply or freshly export exact target-pod evidence | FSM import is requested | verify_org_hierarchy_fsm_package |
| Preview approval | Immutable preview and explicit approval bound to its checksum | Block import submission | Review and approve the unchanged preview | FSM import is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Current target state is missing for an update, removal, replacement, or import | Blocked | Reconcile the authorized target baseline | resolve_current_org_hierarchy_setup |
| Desired hierarchy type cannot be resolved to one valid value | Blocked | Provide a clearer hierarchy outcome | resolve_allowed_hierarchy_type |
| Desired classification set is empty or contains a value that cannot be resolved | Blocked | Provide at least one classification with clearer wording where needed | resolve_available_org_classifications |
| Organization or department hierarchy lacks a valid tree, active version, or starting organization | Blocked | Resolve one complete target combination | resolve_default_org_hierarchy |
| FSM import would replace a different existing hierarchy type or remove a classification | Unsupported for the proven contract | Return the affected operation as unsupported unless fresh target evidence proves a non-UI contract | resolve_current_org_hierarchy_setup |
| Exact target template or package metadata is missing | Blocked for import only | Continue assisted planning or acquire target evidence | verify_org_hierarchy_fsm_package |
| Required facts and route-specific evidence are complete | Satisfied | Continue to dependency readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Hierarchy type | Resolve the supplied hierarchy type to one valid value; do not substitute a report value or the internal first-visit default | Every request | resolve_allowed_hierarchy_type |
| Classification cardinality | Reject an empty desired selected-classification set | Every change | resolve_available_org_classifications |
| Classification membership | Resolve each supplied classification to one valid value and reject unresolved or ambiguous inputs | Every change | resolve_available_org_classifications |
| Default hierarchy completeness | Require tree, active version, and starting organization to resolve as one valid combination | Non-None hierarchy | resolve_default_org_hierarchy |
| Update omission | Treat an omitted hierarchy type or classification set as preserve-current, never as None or remove-all | Update | resolve_current_org_hierarchy_setup |
| Import mapping | Reject every field or package member that is not resolved from the exact target template | FSM import | verify_org_hierarchy_fsm_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OHCL.VALIDATE_INPUT | step | 1 | validate_input | valid->OHCL.RESOLVE_CURRENT_STATE;status_requested->OHCL.STATUS_REQUEST_GATE;invalid->OHCL.HANDLE_ERROR | none | stop | For preparation apply the required groups; for a later explicit status/results/verification request validate saved project, target, task and acceptance context without requiring a new hierarchy design or import |

## Refined Required Evidence

- **BP-010 — Required evidence:** Allow hierarchy type `None` only with documented rationale, compensating governance, accountable owner, approval, and a review of current transaction volume, project count, reporting needs, and reorganization risk.
