# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect identity/seeded roles | Only one allowed custom role changes |
| 2 | Validate dates/reference | Effective range and optional enterprise role are valid |
| 3 | Validate children | PM implementation, qualifications, and translations reconcile explicitly |
| 4 | Protect active use/access | End-date, association, and removals are safe |
| 5 | Protect package | Exact FSM diff and immutable artifact ready for loader preflight; submission approval is owned by core.data-loader |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create/update | Blocker | find_project_role | Duplicate/ambiguous/seeded role | Correct identity or preserve | Yes |
| Enterprise Role | Blocker | resolve_active_enterprise_role | Zero/many/inactive/duty-role match | Supply enough context to resolve one current job or abstract role | Yes |
| Predefined requirement | Blocker | resolve_active_qualification_requirement | Inactive or unsupported item, missing target selection context, no candidate, or unselected ambiguity | Select an eligible target requirement; word search alone is insufficient | Yes |
| Qualification section/context | Blocker | resolve_project_qualification_context | No exact same-target item/type/section match in the fresh export, no proven target selection for a new section, uncertain LOV mode, or section guessed from content type | Reuse the exact item/section found under any role in the task export; otherwise obtain the target Requirements LOV selection. Ask for a choice if multiple sections remain | Yes |
| Rating level | Blocker | resolve_active_qualification_rating | Requirement context missing, no match, or ambiguous value in that requirement's rating set | Resolve the parent requirement first, then supply enough context to disambiguate the rating | Yes |
| Qualifications | Blocker | resolve_role_children | PM not implemented, duplicate/invalid rows | Enable capability or correct rows | Yes |
| End-date/association/removal | Blocker | resolve_role_use | Missing evidence or unsafe assignment/request/access impact | Resolve use or preserve | Yes |
| Delete/direct REST | Blocker |  | No supported setup contract | Use supported update/end-date/FSM | No |
| Import preparation | Blocker | verify_project_role_package | Target contract or immutable artifact invalid | Regenerate and revalidate before loader approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_project_role | Create/update | Baseline/seeded state | ora_reference_lookups.md |
| resolve_active_enterprise_role | Association supplied | RoleId, RoleName, RoleCode, active state, job/abstract eligibility | ora_reference_lookups.md |
| resolve_project_qualification_type | Predefined requirement supplied | Supported target type identity and metadata | ora_reference_lookups.md |
| resolve_active_qualification_requirement | Predefined requirement supplied | Content item identity, canonical name, supported type and active-on-target-date evidence | ora_reference_lookups.md |
| resolve_project_qualification_context | Qualification or keyword change | Target LOV mode, exact item/section from any matching exported role or new target selection; no fabricated business-group identifier | ora_reference_lookups.md |
| resolve_active_qualification_rating | Rating level supplied | Content-item-scoped membership, canonical short description and matching rating model | ora_reference_lookups.md |
| resolve_role_children | Child change | PM flag/current children | ora_reference_lookups.md |
| resolve_role_use | Destructive semantic change | Use/access impact | ora_reference_lookups.md |
| verify_project_role_package | Import | Contract/checksum | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROLE.ENFORCE_DESIGN | decision | 7 | design_enforcement | pass->PROLE.EXECUTION_GATE;blocked->PROLE.RETURN_REFUSAL;failure->PROLE.RETURN_ISSUES | PROLE.RESOLVE_DEPENDENCIES | stop | Before handing validated preparation to the loader's approval workflow |

## Design Source Reference

Source reviewed 2026-10-10 for PJF_MANAGE_PROJECT_ROLES.

- [Create Project Roles, 26C](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapfm/create-project-roles.html): predefined-role protection, optional enterprise-role association, and qualification/keyword scope. The equivalent 26D URL could not be retrieved; 26C is the latest successfully retrieved page for this topic, not proof of every target release.
