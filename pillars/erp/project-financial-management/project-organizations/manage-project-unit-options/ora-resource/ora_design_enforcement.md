# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect project-unit identity | Apply options only to one existing classified project unit |
| 2 | Validate reference sharing | Use one default set resolved through resolve_reference_set and keep separate set assignments outside this task |
| 3 | Validate numbering | Enforce method-dependent fields, target feature ownership, and nonconflicting automatic sequence |
| 4 | Validate business-unit relationships | Pass additions to Fusion for import-time eligibility validation; remove only unused, deletable combinations |
| 5 | Validate reporting setup | Keep commitment inclusion, status, and allocation basis internally consistent |
| 6 | Protect package and approval | Preserve same-task member contracts and require immutable preview approval |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any write | Blocker | find_project_unit_options | Project unit is absent, ambiguous, or not classified | Complete project-unit organization setup and export current options | Yes |
| General properties | Blocker | resolve_reference_set | Required Default Set is missing or the resolver cannot establish one valid set | Resolve the requested set through the current-target lookup and retain its canonical SetCode | Yes |
| Manual numbering | Blocker |  | NumberType is missing or not Numeric/Alphanumeric | Supply the supported type | Yes |
| Automatic numbering | Blocker | find_project_unit_options | NextNumber is absent, not positive, or conflicts with another determinant | Supply a valid nonconflicting first number | Yes |
| Related-BU addition | Validation disclosure | resolve_project_business_units | Name is blank or duplicated | Preserve exact valid names in the immutable preview; Fusion validates relationship eligibility during import | Yes |
| Related-BU removal | Blocker | resolve_project_business_units | Relationship is nondeletable or used by a project/template | Preserve the association | No |
| Reporting setup | Blocker | find_project_unit_options | The project unit has no complete `PJF_REPORTING_SETUP` row, or an included commitment lacks Approved/All status, or an excluded commitment supplies one | Prepare a complete row using explicit intent and eligible UI defaults from ora_defaulting_rules.md; disclose origins in the approval preview and verify its import by fresh export | Yes |
| Set assignment change | Blocker |  | The request belongs to Manage Project Unit Set Assignments | Route separately | No |
| Import preview | Blocker | verify_project_unit_options_package | Required members/headers are missing, altered, or mixed with another task | Regenerate from validated task template | Yes |
| Direct REST write | Blocker |  | No exact writable composite option contract exists | Use FSM CSV with preview and approval | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_project_unit_options | Every write or import | Identity, current options, relationships, reporting, numbering | ora_reference_lookups.md |
| resolve_reference_set | Default set supplied or row created | Canonical SetCode and SetName from the current-target set resolver | ora_reference_lookups.md |
| resolve_project_business_units | Relationships change | Exact addition names; usage/deletability evidence for removals | ora_reference_lookups.md |
| verify_project_unit_options_package | Import preview or numbering feature decision | Contracts, checksum, feature status, allowed basis | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUOPT.ENFORCE_DESIGN | decision | 8 | design_enforcement | pass->PUOPT.EXECUTION_GATE;blocked->PUOPT.RETURN_REFUSAL;failure->PUOPT.RETURN_ISSUES | PUOPT.RESOLVE_DEPENDENCIES | stop | Before validation completes or any import preview is approved |
## Related Business Unit Validation

Fusion owns Project Accounting eligibility validation for an addition. Package validation must retain the exact requested name, and a failed load must retain Fusion's diagnostic rather than triggering an automatic retry.
