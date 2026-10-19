# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope/baseline | Exact target and fresh synchronized role export |
| 2 | Seeded/reference state | Custom role and current enterprise role resolve |
| 3 | Implementation/children/use | Qualifications allowed and semantic removals safe |
| 4 | Package/preflight | Exact package ready for loader Task Hook validation; loader approval follows validation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PROLE.SCOPE | Task/target | Yes | Every request | Verify | Catalog/context | verify_project_role_scope | Prevent cross-target write | Supply target | Scope |
| PROLE.BASELINE | Synchronized current role | Yes | Update/import | Lookup | current_export | find_project_role | Safe identity/diff | Export all members | Baseline |
| PROLE.ENTERPRISE | Enterprise Role | Conditional | Association supplied | Lookup | Named live resolver | resolve_active_enterprise_role | Prevent invalid privilege association | Supply RoleCommonName (preferred) or exact RoleName | Canonical enterprise-role identity |
| PROLE.QUALIFICATION_CONTEXT | Target qualification selection | Conditional | Predefined or keyword child change | Lookup | Fresh same-target task export across all role parents; target LOV-mode evidence; supplied Manage Project Roles LOV evidence only for an unseen item or new section | resolve_project_qualification_context | Prove item/section eligibility under the target feature mode | Give the Requirements name. Supply selection evidence only if target data cannot establish the item/section or mode | Proven mode, item context and canonical section when applicable |
| PROLE.CHILDREN | PM flag/qualifications/translations | Conditional | Child change | Lookup | Current implementation/export | resolve_role_children | Prevent unsupported/lost children | Supply explicit rows | Children |
| PROLE.USE | Active use/access | Conditional | End-date/association/removal | Lookup | Target use evidence | resolve_role_use | Prevent access/resource disruption | Resolve affected uses | Counts |
| PROLE.PACKAGE | FSM contract | Yes | Import | Verify | Template/package | verify_project_role_package | Loader safety | Preserve checksum | Contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All dependencies ready | Yes |
| Missing artifact | Baseline/role catalog/PM flag/use/template absent | No |
| Conflict | Seeded role, invalid enterprise role, duplicate/unsupported child, active use | No |
| Unsupported | Delete/direct setup REST mutation | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROLE.RESOLVE_DEPENDENCIES | step | 6 | resolve_dependency | ready->PROLE.ENFORCE_DESIGN;missing->PROLE.RETURN_ISSUES;conflict->PROLE.RETURN_REFUSAL | PROLE.ROUTE_OPERATION | stop | Before preview/validation completes |
