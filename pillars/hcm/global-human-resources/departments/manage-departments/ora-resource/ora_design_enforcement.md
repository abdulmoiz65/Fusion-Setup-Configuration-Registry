# Manage Departments Design Enforcement

## Purpose

Defines the mandatory Department design gates evaluated before preview or
routing. It does not perform lookups, apply defaults, or create missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact business record for read, edit, inactivation, or delete-effective-split; confirm zero exact duplicates for create |
| 2 | Validate context | Confirm effective context and recognized fields |
| 3 | Validate dependencies | Resolve each supplied Department Set, Location, and Action Reason through its declared resolver |
| 4 | Validate mutation scope | Require the base Organization row and only applicable child rows |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Read, edit, inactivate, or delete-effective-split | Blocking | find_manage_departments | Identity is absent, unresolved, or ambiguous | Supply one exact business identifier | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_departments | One or more exact matches already exist, or the uniqueness check is ambiguous | Supply a unique exact department identity | Input fix |
| EFF_SHAPE | An OrgInformation row is supplied | Blocking |  | The category, context discriminator, context value, or configured multirow unique key is missing or inconsistent | Correct the EFF row through input validation | Input fix |
| CONTEXT | A date-effective or contextual value is requested | Blocking | find_manage_departments | Required effective context is absent or invalid | Supply one supported effective context | Input fix |
| DEPARTMENT_SET | A Department Set is supplied | Blocking | resolve_department_set | Set identity is unresolved, ambiguous, or inconsistent | Resolve one exact set tuple | Lookup fix |
| LOCATION | A Location is supplied | Blocking | resolve_department_location | Location is unresolved, inactive, ineffective, or ambiguous | Resolve one exact effective Location | Lookup fix |
| ACTION_REASON | An Action Reason is supplied | Blocking | resolve_department_action_reason | Action Reason is unresolved or ambiguous | Resolve one exact current Action Reason | Lookup fix |
| DATE_EFFECTIVE_SPLIT_DELETE | delete-effective-split is requested | Blocking | resolve_department_delete_history | Source uses HDL DELETE, omits or misplaces `SET PURGE_FUTURE_CHANGES Y`, omits the resolved OrganizationId unique reference or an operation-required OrgUnitClassification association, would remove the logical first split, or does not exactly bound future splits to remove | Use the full generated Organization XLSX with one Data Loader Directives row, an Organization MERGE row with the resolved OrganizationId, confirmed retained EffectiveStartDate, and inclusive EffectiveEndDate, plus at least one operation-required OrgUnitClassification association; omit OrgInformation and non-key attributes | Source rebuild |
| DESIGN | A related organization value is used | Blocking |  | The value is inferred, copied, or not backed by one exact resolved reference | Supply or resolve one approved business value | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_departments | Read, edit, inactivate, delete-effective-split, create uniqueness check, or effective-context validation | Exact identity, uniqueness result, effective range, and current values | ora_reference_lookups.md |
| resolve_department_set | A Department Set is supplied | One internally consistent SetId, SetCode, and SetName tuple | ora_reference_lookups.md |
| resolve_department_location | A Location is supplied | One exact active and effective Location | ora_reference_lookups.md |
| resolve_department_action_reason | An Action Reason is supplied | One exact current Action Reason | ora_reference_lookups.md |
| resolve_department_delete_history | delete-effective-split | Confirmed retained start, inclusive deletion end, and preserved predecessor values | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEPT.DESIGN | decision | 6 | design_enforcement | passed->DEPT.ROUTE;not_required->DEPT.ROUTE;blocked->DEPT.ERROR | DEPT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
