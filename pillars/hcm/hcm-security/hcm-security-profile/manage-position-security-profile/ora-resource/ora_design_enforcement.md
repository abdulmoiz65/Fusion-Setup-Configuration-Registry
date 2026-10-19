# Position Security Profile Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce CSV-only mutation route | Use the current Fusion task template and the core.data-loader-authorized task-level CSV import workflow for every create or update; do not use direct REST mutation |
| 2 | Retrieve configuration | Retrieve the position security-specific profile option and enterprise configuration settings when area-of-responsibility or hierarchy security is selected |
| 3 | Evaluate conditional fields | Apply the documented scope and hierarchy conditionality before previewing a profile change |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| ScopeOfResponsibility is supplied | Error | get_position_security_configuration | SecureByAreasOfResponsibilityFlag is not true | Use scope of responsibility only for area-of-responsibility security | Yes |
| SecureByAreasOfResponsibilityFlag is true | Error | get_position_security_configuration | SecureByPositionHierarchyFlag, SecureByDepartmentFlag, or SecureByBusinessUnitFlag is also enabled | With area-of-responsibility security, retain only basic details and secure-by-position-list criteria; remove the incompatible criteria | Yes |
| HierarchyContent is supplied | Error | get_position_security_configuration | SecureByPositionHierarchyFlag is not true | Use hierarchy content only for position hierarchy security | Yes |
| HierarchyType is supplied | Error | get_position_security_configuration | The selected hierarchy type is unavailable under enterprise Position Hierarchy Configuration settings | Select only a hierarchy type made available by the retrieved enterprise configuration | Yes |
| A top position is selected | Error | get_position_security_configuration | The supplied top-position selection or position fields are inconsistent with the selected hierarchy configuration | Re-evaluate TopPositionSelection, TopPositionId, TopPositionName, TopPositionCode, and IncludeTopPositionFlag against the retrieved configuration | Yes |
| A profile is created or genuinely renamed | Error | find_position_security_profile_by_id; verify_position_security_profile_name_unique | A rename target cannot be retrieved by current ID with the supplied old Name, or the proposed new Name has one or more exact matches; a create has any exact proposed-Name match | Correct the old identity or provide an available new Name; treat an unchanged proposed Name as an unchanged-name update | Yes |
| A profile create or update is requested | Error | resolve_position_security_profile_csv_context | The requested mutation does not use a current task-template CSV package, immutable ZIP preview, exact approval, one task-level CSV import, and process-log verification | Use the CSV-only task workflow; direct REST POST, PATCH, PUT, and DELETE are not supported | Yes |
| A genuine rename has an available new Name | Blocker |  | The current template-backed contract does not prove parent and child update identity across the Name change | Stop with `rename CSV identity mapping unverified` before CSV preview or import; do not infer update keys from REST IDs or name-based GroupingKeys | No |
| SecureByDepartmentFlag, SecureByBusinessUnitFlag, or SecureByPositionHierarchyFlag is enabled | Warning | get_position_security_configuration | None | Suggest areas of responsibility as the preferred configuration approach | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| get_position_security_configuration | Area-of-responsibility or hierarchy security is selected | Position security-specific profile option and enterprise configuration setting values | ora_reference_lookups.md |
| find_position_security_profile_by_id | An existing profile is updated or renamed | Verified current ID and Name | ora_reference_lookups.md |
| verify_position_security_profile_name_unique | A profile is created or genuinely renamed | Proposed Name availability and exact-match count | ora_reference_lookups.md |
| resolve_position_security_profile_csv_context | A profile create or update is requested | Current template ViewInstanceName, GroupingKey, and parent-child CSV context | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.ENFORCE_SCOPE | decision | 40 | design_enforcement | compliant->POS.DONE;blocked->POS.RETURN_ISSUES | POS.APPLY_DEFAULTS | stop | A position security profile create or update is being prepared for preview or import |
