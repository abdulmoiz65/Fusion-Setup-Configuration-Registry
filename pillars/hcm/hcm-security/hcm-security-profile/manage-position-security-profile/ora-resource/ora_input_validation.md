# Position Security Profile Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Existing profile identity | PositionSecurityProfileId and current exported/template-backed CSV context; current exact Name for a rename | Stop before validating or updating an existing profile | Retrieve the profile by ID; for a rename require its returned Name to equal the supplied old Name, then resolve parent and child CSV context | Validating or updating an existing profile | find_position_security_profile_by_id |
| Profile definition | Name, current task template, resolved reference values, and CSV context | Stop before creating a profile | Export the current task template, resolve references and CSV context, and prepare the profile in the template-backed CSV package | Creating a profile | resolve_position_security_profile_csv_context |
| Proposed profile Name | Name | Stop before creating or renaming a profile | Require zero exact proposed-Name matches for a create or genuine rename. A proposed Name equal to the verified current Name follows the unchanged-name update route. | Creating or renaming a profile | verify_position_security_profile_name_unique |
| CSV-only mutation package | Current task template, immutable ZIP preview, exact approval, and task-level import process-log verification | Stop before any create or update | Use the core.data-loader-authorized task-level CSV import workflow; do not construct or submit a direct REST mutation | Creating or updating a profile | resolve_position_security_profile_csv_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| SecureByAreasOfResponsibilityFlag is true | Responsibility type and scope must be evaluated for the selected area-of-responsibility configuration | Run the configuration lookup and enforce the documented conditional scope rule | get_position_security_configuration |
| SecureByPositionHierarchyFlag is true | Hierarchy type and hierarchy content must be evaluated against enterprise position hierarchy configuration | Run the configuration lookup and enforce the documented conditional hierarchy rule | get_position_security_configuration |
| SecureByPositionListFlag is true | The child positions collection may supply the specified position list | Validate the child position fields before using the list | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Boolean fields | EnabledFlag, ViewAllFlag, IncludeFuturePositionsFlag, SecureByAreasOfResponsibilityFlag, SecureByPositionHierarchyFlag, IncludeTopPositionFlag, SecureByDepartmentFlag, SecureByBusinessUnitFlag, and SecureByPositionListFlag accept true or false | A listed boolean is supplied | |
| Area-of-responsibility scope | ScopeOfResponsibility is valid only when SecureByAreasOfResponsibilityFlag is true | ScopeOfResponsibility is supplied | get_position_security_configuration |
| Hierarchy content | HierarchyContent is valid only when SecureByPositionHierarchyFlag is true | HierarchyContent is supplied | get_position_security_configuration |
| Position list choice | IncludeExclude accepts include or exclude; RemoveRow uses Y to remove a child position row | A positions child row is supplied | |
| Base profile fields | PositionSecurityProfileId is the unique identifier; Name and Description are the documented profile identity fields | A profile row is supplied | find_position_security_profile_by_id |
| Proposed profile Name | Zero exact proposed-Name matches are required for a create or genuine rename; an unchanged proposed Name is an update | Creating or renaming a profile | verify_position_security_profile_name_unique |
| Rename CSV identity mapping | Block with `rename CSV identity mapping unverified` before CSV preview or import; never infer update keys from REST IDs or name-based GroupingKeys | A genuine rename passes name availability |  |
| Flag lookup | EnabledFlag, IncludeFuturePositionsFlag, and IncludeTopPositionFlag must resolve through the YES_NO common lookup | A listed flag is supplied | resolve_yes_no_from_common_lookup |
| Position-list inclusion lookup | IncludeExclude must resolve through the INCLUDE_EXCLUDE common lookup | A position-list child row is supplied | resolve_include_exclude_from_common_lookup |
| Responsibility type identification | ResponsibilityType identifies the different kind of responsibility type for areas of assignments for a user | ResponsibilityType is supplied | resolve_responsibility_type_from_common_lookup |
| Scope of responsibility identification | ScopeOfResponsibility identifies the attribute or grouping of attributes from a user's areas of responsibility that defines secured access | ScopeOfResponsibility is supplied | resolve_scope_of_responsibility_from_common_lookup |
| Responsibility type lookup | ResponsibilityType is verified with lookupType PER_RESPONSIBILITY_TYPES and its Meaning is mapped to ResponsibilityTypeMeaning | ResponsibilityType is supplied | resolve_responsibility_type_from_common_lookup |
| Scope of responsibility lookup | ScopeOfResponsibility is verified with lookupType ORA_PER_PRSN_SEC_AOR_SCOPES and its Meaning is mapped to ScopeOfResponsibilityMeaning | ScopeOfResponsibility is supplied | resolve_scope_of_responsibility_from_common_lookup |
| Hierarchy type lookup | HierarchyType is verified with lookupType ORA_PER_POS_SEC_HRCHY_TYPE and its Meaning is mapped to HierarchyTypeMeaning | HierarchyType is supplied | resolve_hierarchy_type_from_common_lookup |
| Position hierarchy tree structure lookup | PosHierarchyTreeStructCode is verified with lookupType ORA_PER_POS_SEC_HRCHY_TYPE using the supplied lookup code | PosHierarchyTreeStructCode is supplied | resolve_position_hierarchy_tree_structure_from_common_lookup |
| Position hierarchy content lookup | PosHierarchyContent is verified with lookupType ORA_PER_SEC_POS_HIER_CONTENT using the supplied lookup code | PosHierarchyContent is supplied | resolve_position_hierarchy_content_from_common_lookup |
| Top-position selection lookup | TopPositionSelection is verified with lookupType PER_POS_SEC_PROF_TOP_POS_SEL and its Meaning is mapped to TopPositionSelectionMeaning | TopPositionSelection is supplied | resolve_top_position_selection_from_common_lookup |
| Area-of-responsibility fields | ResponsibilityType and ScopeOfResponsibility are the documented fields for area-of-responsibility security; their meaning fields map a display Meaning to the stored LookupCode | SecureByAreasOfResponsibilityFlag is true | get_position_security_configuration |
| Hierarchy fields | HierarchyType, PositionTreeCode or PositionTreeName, TopPositionSelection, HierarchyContent, TopPositionId or TopPositionName or TopPositionCode, TopPositionBusinessUnitName, and IncludeTopPositionFlag are the documented hierarchy attributes | SecureByPositionHierarchyFlag is true | get_position_security_configuration |
| Position Tree identity | When PositionTreeName is supplied without PosHierarchyTreeCode, resolve PosHierarchyTreeCode through hcmTreesLOV by exact TreeName. | PositionTreeName is supplied | resolve_position_tree_code_from_hcm_trees_lov |
| Top Position identity | When TopPositionName is supplied without TopPositionId, resolve TopPositionId through positionsLov; if the PositionName search returns multiple positions, require PositionCode. | TopPositionName is supplied | resolve_top_position_id_from_positions_lov |
| Organization-security fields | DepartmentSecurityProfileId or DepartmentSecurityProfileName and BusinessUnitSecurityProfileId or BusinessUnitSecurityProfileName are the documented organization-security attributes | SecureByDepartmentFlag or SecureByBusinessUnitFlag is true | |
| Business unit security profile identity | When BusinessUnitSecurityProfileName is supplied without BusinessUnitSecurityProfileId, resolve BusinessUnitSecurityProfileId from OrganizationSecurityProfileId through organizationSecurityProfilesLOV by exact Name. | BusinessUnitSecurityProfileName is supplied | resolve_business_unit_organization_security_profile_id |
| Department security profile identity | When DepartmentSecurityProfileName is supplied without DepartmentSecurityProfileId, resolve DepartmentSecurityProfileId from OrganizationSecurityProfileId through organizationSecurityProfilesLOV by exact Name. | DepartmentSecurityProfileName is supplied | resolve_department_organization_security_profile_id |
| Position-list fields | PositionId, PositionCode or PositionName, PositionBusinessUnitName, and IncludeExclude are the documented child position-list attributes. When PositionName is supplied without PositionId, resolve PositionId through positionsLov; if the name returns multiple positions, require PositionCode. | SecureByPositionListFlag is true | resolve_position_id_from_positions_lov |
| Parent CSV schema | PER_POSITION_SECURITY_PROFILES.csv supplies Name, ViewInstanceName, GroupingKey, BUOrgSecurityProfileName, DeptOrgSecurityProfileName, EnabledFlag, IncludeTopPositionFlag, TreeName, PosHierarchyTreeStructCode, SecureByBusinessUnitFlag, SecureByDepartmentFlag, SecureByPositionHierarchyFlag, SecureByPositionListFlag, TopPosSelection, ViewAllFlag, BusinessUnit, PositionCode, IncludeFuturePositionsFlag, Description, SecureByAor, PosHierarchyContent, BuOrgSecurityProfileId, DeptOrgSecurityProfileId, PosHierarchyTreeCode, PositionSecurityProfileId, and TopPositionId | Preparing a task CSV package | resolve_position_security_profile_csv_context |
| Position-list CSV schema | ORA_PER_POS_SEC_PROFILE_POSITIONS.csv supplies PER_POSITION_SECURITY_PROFILES.Name, PositionSecurityProfileName, PositionCode, ViewInstanceName, GroupingKey, IncludeExcludeFlag, BusinessUnit, PosSecProfilePositionId, PositionId, and PositionSecurityProfileId | SecureByPositionListFlag is true and child positions are included | resolve_position_security_profile_csv_context |
| AOR-scope CSV schema | ORA_POSITION_SECURITY_PROFILE_AOR_SCOPE.csv supplies PER_POSITION_SECURITY_PROFILES.Name, ResponsibilityType, ScopeOfResponsibility, PositionSecurityProfileName, ViewInstanceName, GroupingKey, GUID, PosSecProfAorScopeId, and PositionSecurityProfileId | SecureByAor is true and area-of-responsibility scope rows are included | resolve_position_security_profile_csv_context |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.VALIDATE_INPUT | decision | 10 | validate_input | new_profile->POS.VERIFY_PROFILE_NAME;existing_or_renamed_profile->POS.FIND_PROFILE;invalid->POS.RETURN_ISSUES | none | stop | A position security profile is being validated, created, or updated; a proposed Name equal to current Name is an unchanged-name update |
